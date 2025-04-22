import heapq

action_set: set[str] = {
    "CREATE_ACCOUNT",
    "DEPOSIT",
    "PAY",
    "TOP_ACTIVITY",
    "TRANSFER",
    "TRANSFER_EXP",
    "ACCEPT_TRANSFER",
    "GET_BALANCE",
    "MERGE_ACCOUNT",
}

HOUR24_IN_MS = 86_400_000

def process_queries(queries: list[list[str]]) -> list[str]:
    res: list[str] = []

    timed_q: list[(int, str, list[str])] = []
    for q in queries:
        heapq.heappush(timed_q, (int(q[1]), q[0], q[2:]))

    class Balance:
        def __init__(self, amount: int, time_at: int):
            self.amount = amount
            self.time_at = time_at
        
        def mayOk(self, now_time: int):
            return now_time > self.time_at

    # balances: dict[str, int] = {}
    timed_balance: dict[str, list[Balance]] = {}
    activities: dict[str, int] = {}

    class Transfer:
        def __init__(self, src_acc: str, tar_acc: str, amount: int, dead_time: int):
            self.src_acc = src_acc
            self.tar_acc = tar_acc
            self.amount = amount
            self.dead_time = dead_time
            self.status = "PENDING"

        def isOk(self, now_time: int):
            return now_time < self.dead_time

        def isPending(self):
            return self.status == "PENDING"
        
        def isDone(self):
            return self.status == "DONE"
        
        def isFailed(self):
            return self.status == "FAILED"
        
        def setDone(self):
            self.status = "DONE"

        def setFailed(self):
            self.status = "FAILED"
        
    transfers: dict[str, Transfer] = {}
    t_basename = "transfer"
    t_count = 1

    while len(timed_q) > 0:
        q = heapq.heappop(timed_q)
        timestamp = q[0]
        action = q[1]
        data = q[2]

        if action not in action_set:
            raise Exception(f"action [{action}] not in the list")

        if action == "CREATE_ACCOUNT":
            account_name = data[0]
            # if account_name in balances:
            if account_name in timed_balance:
                res.append("false")
                continue
            # balances[account_name] = 0
            timed_balance[account_name] = []
            activities[account_name] = 0
            res.append("true")            

        elif action == "DEPOSIT":
            account_name, amount = data[0], int(data[1])
            # if account_name not in balances:
            if account_name not in timed_balance:
                res.append("")
                continue
            # balances[account_name] += amount
            prev_balance = 0
            if len(timed_balance[account_name]) > 0:
                prev_balance = timed_balance[account_name][-1].amount
            timed_balance[account_name].append(
                Balance(prev_balance+amount, timestamp),
            )
            activities[account_name] += amount
            # res.append(balances[account_name])
            res.append(timed_balance[account_name][-1].amount)

        elif action == "PAY":
            account_name, amount = data[0], int(data[1])
            # if account_name not in balances:
            if account_name not in timed_balance:
                res.append("")
                continue
            # if balances[account_name] < amount:
            curr_amount = 0
            if len(timed_balance[account_name]) > 0:
                curr_amount = timed_balance[account_name][-1].amount
            if curr_amount < amount:
                res.append("")
                continue
            # balances[account_name] -= amount
            curr_amount -= amount
            timed_balance[account_name].append(Balance(curr_amount, timestamp))
            activities[account_name] += amount
            # res.append(balances[account_name])
            res.append(timed_balance[account_name][-1].amount)

        elif action == "TOP_ACTIVITY":
            n = int(data[0])
            filtered_activities = sorted(
                activities.items(),
                key= lambda act : (-act[1], act[0]),
            )[:n]
            res_str = ", ".join([f"{act[0]}({act[1]})" for act in filtered_activities])
            res.append(res_str)

        elif action == "TRANSFER":
            src_acc, tar_acc, amount = data[0], data[1], int(data[2])
            if src_acc not in timed_balance:
                res.append("")
                continue
            if tar_acc not in timed_balance:
                res.append("")
                continue
            if src_acc == tar_acc:
                res.append("")
                continue
            src_amount = 0
            if len(timed_balance[src_acc]) > 0:
                src_amount = timed_balance[src_acc][-1].amount
            # if balances[src_acc] < amount:
            if src_amount < amount:
                res.append("")
                continue
            # balances[src_acc] -= amount
            src_amount -= amount
            timed_balance[src_acc].append(Balance(src_amount, timestamp))
            t_name = t_basename + str(t_count)
            t_count += 1
            transfers[t_name] = Transfer(src_acc, tar_acc, amount, timestamp+HOUR24_IN_MS)
            # exp
            heapq.heappush(timed_q, (timestamp+HOUR24_IN_MS, "TRANSFER_EXP", [t_name]))
            res.append(t_name)

        # MY
        elif action == "TRANSFER_EXP":
            transfer_id = data[0]
            t = transfers[transfer_id]
            if t.isDone() or t.isFailed():
                continue
            curr_balance = 0
            if len(timed_balance[t.src_acc]) > 0:
                curr_balance = timed_balance[t.src_acc][-1].amount
            curr_balance += t.amount
            # balances[t.src_acc] += t.amount
            timed_balance[t.src_acc].append(Balance(curr_balance, timestamp))
            t.setFailed()

        elif action == "ACCEPT_TRANSFER":
            account_name, transfer_id = data[0], data[1]
            if account_name not in timed_balance:
                res.append("false")
                continue
            if transfer_id not in transfers:
                res.append("false")
                continue
            t = transfers[transfer_id]
            if t.tar_acc != account_name:
                res.append("false")
                continue
            if not t.isOk(timestamp):
                res.append("false")
                continue
            if not t.isPending():
                res.append("false")
                continue

            # balances[account_name] += t.amount
            curr_balance = timed_balance[account_name][-1].amount
            curr_balance += t.amount
            timed_balance[account_name].append(Balance(curr_balance, timestamp))
            t.setDone()
            res.append("true")

        elif action == "GET_BALANCE":
            account_name, time_at = data[0], int(data[1])
            if account_name not in timed_balance:
                res.append("")
                continue
            t_bals = timed_balance[account_name]
            for tb in t_bals:
                if not tb.mayOk(time_at):
                    continue
                res.append(tb.amount)
                break
            res.append("")


    return res

queries = [
    ["CREATE_ACCOUNT",  "1",                     "account1"],
    ["CREATE_ACCOUNT",  "2",                     "account2"],
    ["DEPOSIT",         "3",                     "account1",     "2000"],
    ["DEPOSIT",         "4",                     "account2",     "3000"],
    ["TRANSFER",        "5",                     "account1",     "account2", "5000"],
    ["TRANSFER",        "16",                    "account1",     "account2", "1000"],
    ["ACCEPT_TRANSFER", "20",                    "account1",     "transfer1"],
    ["ACCEPT_TRANSFER", "21",                    "non-existing", "transfer1"],
    ["ACCEPT_TRANSFER", "22",                    "account1",     "transfer2"],
    ["ACCEPT_TRANSFER", "25",                    "account2",     "transfer1"],
    ["ACCEPT_TRANSFER", "30",                    "account2",     "transfer1"],
    ["TRANSFER",        "40",                    "account1",     "account2", "1000"],
    ["GET_BALANCE",     "100",                   "account1",     "100"],
    ["GET_BALANCE",     "101",                   "account2",     "100"],
    ["ACCEPT_TRANSFER", str (45 + HOUR24_IN_MS), "account2",     "transfer2"],
    ["TRANSFER",        str (50 + HOUR24_IN_MS), "account1",     "account1", "1000"],
]

results = process_queries(queries)
for idx in range(len(queries)):
    print(f"Query {idx + 1}: {results[idx]}")

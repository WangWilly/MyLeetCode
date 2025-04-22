import heapq

action_set: set[str] = {
    "CREATE_ACCOUNT",
    "DEPOSIT",
    "PAY",
    "TOP_ACTIVITY",
}

def process_queries(queries: list[list[str]]) -> list[str]:
    res: list[str] = []

    timed_q: list[(int, str, list[str])] = []
    for q in queries:
        heapq.heappush(timed_q, (int(q[1]), q[0], q[2:]))

    balances: dict[str, int] = {}
    activities: dict[str, int] = {}

    while len(timed_q) > 0:
        q = heapq.heappop(timed_q)
        timestamp = q[0]
        action = q[1]
        data = q[2]

        if action not in action_set:
            raise Exception(f"action [{action}] not in the list")

        if action == "CREATE_ACCOUNT":
            account_name = data[0]
            if account_name in balances:
                res.append("false")
                continue
            balances[account_name] = 0
            activities[account_name] = 0
            res.append("true")            

        elif action == "DEPOSIT":
            account_name, amount = data[0], int(data[1])
            if account_name not in balances:
                res.append("")
                continue
            balances[account_name] += amount
            activities[account_name] += amount
            res.append(balances[account_name])

        elif action == "PAY":
            account_name, amount = data[0], int(data[1])
            if account_name not in balances:
                res.append("")
                continue
            if balances[account_name] < amount:
                res.append("")
                continue
            balances[account_name] -= amount
            activities[account_name] += amount
            res.append(balances[account_name])

        elif action == "TOP_ACTIVITY":
            n = int(data[0])
            filtered_activities = sorted(
                activities.items(),
                key= lambda act : (-act[1], act[0]),
            )[:n]
            res_str = ", ".join([f"{act[0]}({act[1]})" for act in filtered_activities])
            res.append(res_str)

    return res

queries = [
    ["CREATE_ACCOUNT", "1",        "account1"],
    ["CREATE_ACCOUNT", "2",        "account2"],
    ["CREATE_ACCOUNT", "3",        "account3"],
    ["DEPOSIT",        "4",        "account1", "2000"],
    ["DEPOSIT",        "5",        "account2", "3000"],
    ["DEPOSIT",        "6",        "account3", "4000"],
    ['TOP_ACTIVITY',   "7",        "3"],
    ["PAY",            "8",        "account1", "1500"],
    ["PAY",            "9",        "account2", "250"],
    ["DEPOSIT",        "10",       "account3", "250"],
    ['TOP_ACTIVITY',   "11",       "3"],
]

results = process_queries(queries)
for idx in range(len(queries)):
    print(f"Query {idx + 1}: {results[idx]}")

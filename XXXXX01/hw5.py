import heapq

################################################################################
# merge

ACTION_CREATE_ACCOUNT  = "CREATE_ACCOUNT"
ACTION_DEPOSIT         = "DEPOSIT"
ACTION_PAY             = "PAY"
ACTION_PAY_CASHBACK    = "PAY_CASHBACK"
ACTION_TOP_ACTIVITY    = "TOP_ACTIVITY"
ACTION_TRANSFER        = "TRANSFER"
ACTION_ACCEPT_TRANSFER = "ACCEPT_TRANSFER"
ACTION_TRANSFER_EXP    = "ACCEPT_TRANSFER_EXP"
ACTION_MERGE_ACCOUNT   = "MERGE_ACCOUNT"

action_set: set[str] = {
    ACTION_CREATE_ACCOUNT,
    ACTION_DEPOSIT,
    ACTION_PAY,
    ACTION_PAY_CASHBACK,
    ACTION_TOP_ACTIVITY,
    ACTION_TRANSFER,
    ACTION_ACCEPT_TRANSFER,
    ACTION_TRANSFER_EXP,
    ACTION_MERGE_ACCOUNT,
}

################################################################################

class Transfer:
    def __init__(self, sender: str, receiver: str, amount: int, timestamp: int):
        self.sender    = sender
        self.receiver  = receiver
        self.amount    = amount
        self.timestamp = timestamp
        self.status    = "PENDING"

transfer_id_base = "transfer"
MILLISECONDS_IN_1_DAY = EXPIRATION_MS = 86_400_000  # 24 hours in milliseconds

################################################################################

def process_queries(queries: list[list[str]]) -> list[str]:
    time_order_queries: list[list[str]] = []
    for q in queries:
        action = q[0]
        timestamp = int(q[1])
        data = q[2:]
        heapq.heappush(time_order_queries, (timestamp, action, data))

    accounts: dict[str, int] = {}
    results: list[str] = []
    transaction_sums: dict[str, int] = {}

    cashback_percentage = 0.01

    transfers: dict[str, Transfer] = {}
    transfer_count = 1

    while len(time_order_queries) > 0:
        q = heapq.heappop(time_order_queries)
        timestamp = q[0]
        action = q[1]
        data: list[str] = q[2]

        if action not in action_set:
            raise ValueError(f"Invalid action: {action}")

        if action == ACTION_CREATE_ACCOUNT:
            account_id = data[0]
            if account_id in accounts:
                results.append("false")
                continue
            accounts[account_id] = 0
            transaction_sums[account_id] = 0
            results.append("true")

        elif action == ACTION_DEPOSIT:
            account_id = data[0]
            amount = int(data[1])
            if account_id not in accounts:
                results.append("")
                continue
            accounts[account_id] += amount
            transaction_sums[account_id] += amount
            results.append(str(accounts[account_id]))

        elif action == ACTION_PAY:
            account_id = data[0]
            amount = int(data[1])
            if account_id not in accounts or accounts[account_id] < amount:
                results.append("")
                continue
            accounts[account_id] -= amount
            transaction_sums[account_id] += amount

            heapq.heappush(time_order_queries, (timestamp+MILLISECONDS_IN_1_DAY, ACTION_PAY_CASHBACK, (account_id, int(amount * cashback_percentage))))

            results.append(str(accounts[account_id]))

        elif action == ACTION_PAY_CASHBACK:
            account_id = data[0]
            amount: int = data[1]
            if account_id not in accounts:
                results.append("")
                continue
            accounts[account_id] += amount

        elif action == ACTION_TOP_ACTIVITY:
            n = int(data[0])
            sorted_accounts = sorted(
                transaction_sums.items(),
                key=lambda item: (-item[1], item[0])
            )
            top_accounts = sorted_accounts[:n]
            formatted = ", ".join([f"{acc}({val})" for acc, val in top_accounts])
            results.append(formatted)

        elif action == ACTION_TRANSFER:
            src_account = data[0]
            target_account = data[1]
            amount = int(data[2])

            if src_account == target_account or src_account not in accounts or accounts[src_account] < amount:
                results.append("")
                continue

            accounts[src_account] -= amount
            transfer_uniq_id = f"{transfer_id_base}{transfer_count}"
            transfers[transfer_uniq_id] = Transfer(sender=src_account, receiver=target_account, amount=amount, timestamp=timestamp)
            transfer_count += 1

            # reject
            heapq.heappush(time_order_queries, (timestamp+EXPIRATION_MS, ACTION_TRANSFER_EXP, [transfer_uniq_id]))

            # print(accounts)
            results.append(transfer_uniq_id)
        
        elif action == ACTION_TRANSFER_EXP:
            transfer_uniq_id = data[0]
            if transfer_uniq_id not in transfers:
                continue

            transfer = transfers[transfer_uniq_id]
            if transfer.status == "SUCCESS":
                continue
            transfer.status = "FAILED"
            src_account = transfer.sender
            accounts[src_account] += transfer.amount
            # print(accounts)

        elif action == ACTION_ACCEPT_TRANSFER:
            account_id = data[0]
            transfer_id = data[1]

            if transfer_id not in transfers:
                results.append("false")
                continue

            transfer = transfers[transfer_id]
            if transfer.status != "PENDING":
                results.append("false")
                continue
            if account_id != transfer.receiver:
                results.append("false")
                continue
            if timestamp >= transfer.timestamp + EXPIRATION_MS:
                results.append("false")
                continue

            accounts[account_id] += transfer.amount
            transfer.status = "SUCCESS"
            # print(accounts)
            results.append("true")

        elif action == ACTION_MERGE_ACCOUNT:
            to_account = data[0]
            from_account = data[1]
            if to_account not in accounts or from_account not in accounts or to_account == from_account:
                results.append("")
                continue
            accounts[to_account] += accounts[from_account]
            transaction_sums[to_account] += transaction_sums[from_account]
            del accounts[from_account]
            del transaction_sums[from_account]

            results.append(accounts[to_account])

            # TODO: for tranfer in transfers:


    return results


# Example usage
queries = [
    ["CREATE_ACCOUNT", "1",        "account1"],
    ["CREATE_ACCOUNT", "2",        "account1"],
    ["CREATE_ACCOUNT", "3",        "account2"],
    ["DEPOSIT",        "4",        "non-existing", "2700"],
    ["DEPOSIT",        "5",        "account1",     "2700"],
    ["PAY",            "6",        "non-existing", "2700"],
    ["PAY",            "7",        "account1",     "2701"],
    ["PAY",            "8",        "account1",     "200"],
    ["DEPOSIT",        "9",        "account2",     "3000"],
    ["DEPOSIT",        "86400009", "account1",     "0"],    # check cashback
    ["MERGE_ACCOUNT",  "86400010", "account1",     "account2"],
]

results = process_queries(queries)
for idx in range(len(queries)):
    print(f"Query {idx + 1}: {results[idx]}")

################################################################################
# top activity

ACTION_CREATE_ACCOUNT = "CREATE_ACCOUNT"
ACTION_DEPOSIT = "DEPOSIT"
ACTION_PAY = "PAY"
ACTION_TOP_ACTIVITY = "TOP_ACTIVITY"

action_set: set[str] = {
    ACTION_CREATE_ACCOUNT,
    ACTION_DEPOSIT,
    ACTION_PAY,
    ACTION_TOP_ACTIVITY,
}

def process_queries(queries: list[list[str]]) -> list[str]:
    accounts: dict[str, int] = {}
    results: list[str] = []
    transaction_sums: dict[str, int] = {}

    for query in queries:
        action = query[0]

        if action not in action_set:
            raise ValueError(f"Invalid action: {action}")

        if action == ACTION_CREATE_ACCOUNT:
            account_id = query[2]
            if account_id in accounts:
                results.append("false")
                continue
            accounts[account_id] = 0
            transaction_sums[account_id] = 0
            results.append("true")

        elif action == ACTION_DEPOSIT:
            account_id = query[2]
            amount = int(query[3])
            if account_id not in accounts:
                results.append("")
                continue
            accounts[account_id] += amount
            transaction_sums[account_id] += amount
            results.append(str(accounts[account_id]))

        elif action == ACTION_PAY:
            account_id = query[2]
            amount = int(query[3])
            if account_id not in accounts or accounts[account_id] < amount:
                results.append("")
                continue
            accounts[account_id] -= amount
            transaction_sums[account_id] += amount
            results.append(str(accounts[account_id]))

        elif action == ACTION_TOP_ACTIVITY:
            n = int(query[2])
            sorted_accounts = sorted(
                transaction_sums.items(),
                key=lambda item: (-item[1], item[0])
            )
            top_accounts = sorted_accounts[:n]
            formatted = ", ".join([f"{acc}({val})" for acc, val in top_accounts])
            results.append(formatted)

    return results


# Example usage
# queries = [
#     ["CREATE_ACCOUNT", "1", "account1"],
#     ["CREATE_ACCOUNT", "2", "account2"],
#     ["DEPOSIT", "3", "account1", "2000"],
#     ["DEPOSIT", "4", "account2", "3000"],
#     ["TRANSFER", "5", "account1", "account2", "5000"],
#     ["TRANSFER", "16", "account1", "account2", "1000"],
#     ["ACCEPT_TRANSFER", "20", "account1", "transfer1"],
#     ["ACCEPT_TRANSFER", "21", "non-existing", "transfer1"], ["ACCEPT_TRANSFER", "22", "account1", "transfer2"], ["ACCEPT_TRANSFER", "25", "account2", "transfer1"],
#     ["ACCEPT_TRANSFER", "30", "account2", "transfer1"],
#     ["TRANSFER", "40", "account1", "account2", "1000"],
#     ["ACCEPT_TRANSFER", str (45 + MILLISECONDS_IN_1_DAY), "account2", "transfer2"], ["TRANSFER", str (50 + MILLISECONDS_IN_1_DAY), "account1", "account1", "1000"],
# ]
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

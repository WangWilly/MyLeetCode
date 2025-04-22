
action_set: set[str] = {
    "CREATE_ACCOUNT",
    "DEPOSIT",
    "PAY",
}

def process_queries(queries: list[list[str]]) -> list[str]:
    accounts: dict[str, int] = {}
    results: list[str] = []

    for query in queries:
        action, data = query[0], query[1:]

        if action not in action_set:
            raise ValueError(f"Invalid action: {action}")

        if action == "CREATE_ACCOUNT":
            account_id = data[0]
            timestamp = int(data[1])
            if account_id in accounts:
                results.append("false")
                continue
            accounts[account_id] = 0
            results.append("true")

        elif action == "DEPOSIT":
            account_id = data[0]
            timestamp = int(data[1])
            amount = int(data[2])
            if account_id not in accounts:
                results.append("")
                continue
            accounts[account_id] += amount
            results.append(str(accounts[account_id]))

        elif action == "PAY":
            account_id = data[0]
            timestamp = int(data[1])
            amount = int(data[2])
            if account_id not in accounts or accounts[account_id] < amount:
                results.append("")
                continue
            accounts[account_id] -= amount
            results.append(str(accounts[account_id]))

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
    ["CREATE_ACCOUNT", "2",        "account1"],
    ["CREATE_ACCOUNT", "3",        "account2"],
    ["DEPOSIT",        "4",        "non-existing", "2700"],
    ["DEPOSIT",        "5",        "account1",     "2700"],
    ["PAY",            "6",        "non-existing", "2700"],
    ["PAY",            "7",        "account1",     "2701"],
    ["PAY",            "8",        "account1",     "200"],
    # ["DEPOSIT",        "86400008", "account1",     "0"],    # check cashback
]

results = process_queries(queries)
for idx in range(len(queries)):
    print(f"Query {idx + 1}: {results[idx]}")

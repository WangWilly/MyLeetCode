# aHR0cDovLzUyMDE5My54eXovRGlzY3V6LzFwb2ludDNhY3Jlcy90aHJlYWQtZDk4ODkzNy0xLTEuaHRtbA==
# aHR0cDovLzUyMDE5My54eXovRGlzY3V6LzFwb2ludDNhY3Jlcy90aHJlYWQtNjIwNTc0ZC0xLTEuaHRtbA==
# http://52O193.xyz/Discuz/1point3acres/thread-537225f-1-1.html

import heapq

action_set: set[str] = {
    "CREATE_ACCOUNT",
    "DEPOSIT",
    "PAY",
}

def process_queries(queries: list[list[str]]) -> list[str]:
    res: list[str] = []

    timed_q: list[(int, str, list[str])] = []
    for q in queries:
        heapq.heappush(timed_q, (int(q[1]), q[0], q[2:]))

    balances: dict[str, int] = {}

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
            res.append("true")            

        elif action == "DEPOSIT":
            account_name, amount = data[0], int(data[1])
            if account_name not in balances:
                res.append("")
                continue
            balances[account_name] += amount
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
            res.append(balances[account_name])


    return res

queries = [
    ["CREATE_ACCOUNT", "1",        "account1"],
    ["CREATE_ACCOUNT", "2",        "account1"],
    ["CREATE_ACCOUNT", "3",        "account2"],
    ["DEPOSIT",        "4",        "non-existing", "2700"],
    ["DEPOSIT",        "5",        "account1",     "2700"],
    ["PAY",            "6",        "non-existing", "2700"],
    ["PAY",            "7",        "account1",     "2701"],
    ["PAY",            "8",        "account1",     "200"],
]

results = process_queries(queries)
for idx in range(len(queries)):
    print(f"Query {idx + 1}: {results[idx]}")


action_set: set[str] = {
    "SET",
    "GET",
    "DELETE",
    "SCAN",
}

def process_queries(queries: list[list[str]]) -> list[str]:
    res: list[str] = []

    state: dict[str, dict[str, str]] = {}

    for q in queries:
        action, data = q[0], q[1:]

        if action not in action_set:
            raise Exception(f"action not in list: {action}")
        
        if action == "SET":
            key, field, val = data[0], data[1], data[2]
            if key not in state:
                state[key] = {field: val}
                res.append("")
                continue
            state[key][field] = val
            res.append("")
        
        elif action == "GET":
            key, field = data[0], data[1]
            if key not in state:
                res.append("")
                continue
            if field not in state[key]:
                res.append("")
                continue
            res.append(state[key][field])
        
        elif action == "DELETE":
            key, field = data[0], data[1]
            if key not in state:
                res.append("false")
                continue
            if field not in state[key]:
                res.append("false")
                continue
            del state[key][field]
            res.append("true")
        
        elif action == "SCAN":
            key, prefix = data[0], data[1]
            if key not in state:
                res.append("")
                continue
            key_prefix_states = sorted(
                filter(lambda s : prefix == s[0][:len(prefix)], state[key].items()),
                key=lambda s : s[1]
            )
            res_str = ", ".join(f"{s[0]}({s[1]})" for s in key_prefix_states)
            res.append(res_str)
        
    return res

queries = [
    ["SET", "A", "BC", "E"],
    ["SET", "A", "BD", "F"],
    ["SET", "A", "C", "G"],
    ["SCAN", "A", "B"],
    ["SCAN", "A", ""],
    ["SCAN", "B", "B"],
]

results = process_queries(queries=queries)
for qidx in range(len(queries)):
    print(f"Query {qidx+1}: {results[qidx]}")

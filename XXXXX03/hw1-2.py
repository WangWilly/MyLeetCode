# aHR0cDovLzUyMDE5My54eXovRGlzY3V6LzFwb2ludDNhY3Jlcy90aHJlYWQtMDk0OWI2Yi0xLTEuaHRtbA==
# TODO: aHR0cDovLzUyMDE5My54eXovRGlzY3V6LzFwb2ludDNhY3Jlcy90aHJlYWQtMmUyMmU3YS0xLTEuaHRtbA==

action_set: set[str] = {
    "SET",
    "GET",
    "DELETE",
    "COMP_AND_SET",
    "COMP_AND_DEL",
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
        
        elif action == "COMP_AND_SET":
            key, field = data[0], data[1]
            expected_val, new_val = data[2], data[3]
            if key not in state:
                res.append("")
                continue
            if field not in state[key]:
                res.append("")
                continue
            old_val = state[key][field]
            if expected_val != old_val:
                res.append("")
                continue
            state[key][field] = new_val
            res.append("")

        elif action == "COMP_AND_DEL":
            key, field = data[0], data[1]
            expected_val = data[2]
            if key not in state:
                res.append("false")
                continue
            if field not in state[key]:
                res.append("false")
                continue
            old_val = state[key][field]
            if expected_val != old_val:
                res.append("false")
                continue
            del state[key][field]
            res.append("true")

    return res

queries = [
    ["SET", "A", "B", "E"],
    ["SET", "A", "C", "F"],
    ["GET", "A", "B"],
    ["GET", "A", "D"],
    ["DELETE", "A", "B"],
    ["DELETE", "A", "D"],
]

results = process_queries(queries=queries)
for qidx in range(len(queries)):
    print(f"Query {qidx+1}: {results[qidx]}")

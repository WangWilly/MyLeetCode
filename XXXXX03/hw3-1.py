
action_set: set[str] = {
    "SET",
    "GET",
    "DELETE",
    "SCAN",
    "SET_AT",
    "GET_AT",
    "DELETE_AT",
    "SCAN_AT",
}

def process_queries(queries: list[list[str]]) -> list[str]:
    res: list[str] = []

    state: dict[str, dict[str, str]] = {}

    class TtlValue:
        def __init__(self, val: str, timestamp: int, ttl: int):
            self.val = val
            self.ttl = ttl
            self.dead_time = timestamp + ttl
        
        def isOk(self, curr: int):
            if self.ttl == 0:
                return True
            return not curr >= self.dead_time

    ttl_state: dict[str, dict[str, TtlValue]] = {}

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
        
        elif action == "SET_AT":
            key, field, val = data[0], data[1], data[2]
            timestamp, ttl = int(data[3]), int(data[4])

            instan = TtlValue(val, timestamp, ttl)
            if key not in ttl_state:
                ttl_state[key] = {field: instan}
                res.append("")
                continue
            ttl_state[key][field] = instan
            res.append("")

        elif action == "GET_AT":
            key, field = data[0], data[1]
            timestamp = int(data[2])
            if key not in ttl_state:
                res.append("")
                continue
            if field not in ttl_state[key]:
                res.append("")
                continue
            if not ttl_state[key][field].isOk(timestamp):
                res.append("")
                continue
            res.append(ttl_state[key][field].val)
        
        elif action == "DELETE_AT":
            key, field = data[0], data[1]
            timestamp = int(data[2])
            if key not in ttl_state:
                res.append("false")
                continue
            if field not in ttl_state[key]:
                res.append("false")
                continue
            if not ttl_state[key][field].isOk(timestamp):
                res.append("false")
                continue
            del ttl_state[key][field]
            res.append("true")
        
        elif action == "SCAN_AT":
            key, prefix = data[0], data[1]
            timestamp = int(data[2])
            if key not in ttl_state:
                res.append("")
                continue
            key_prefix_states = sorted(
                filter(lambda s : prefix == s[0][:len(prefix)] and s[1].isOk(timestamp), ttl_state[key].items()),
                key=lambda s : s[1].val
            )
            res_str = ", ".join(f"{s[0]}({s[1].val})" for s in key_prefix_states)
            res.append(res_str)

    return res


# queries = [
#     ["SET_AT", "A", "BC", "E", "1", "9"],
#     ["SET_AT", "A", "BC", "E", "5", "10"],
#     ["SET_AT", "A", "BD", "F", "5", "0"],
#     ["SCAN_AT" , "A", "B", "14"],
#     ["SCAN_AT" , "A", "B", "15"],
# ]
queries = [
    ["SET", "A", "BC", "E"],
    ["SET", "A", "BD", "F"],
    ["SET", "A", "C", "G"],
    ["SCAN", "A", "B"],
    ["SCAN", "A", ""],
    ["SCAN", "B", "B"],
    ["SET_AT", "A", "B", "C", "1", "0"],
    ["SET_AT", "X", "Y", "Z", "2", "15"],
    ["GET_AT", "X", "Y", "3"],
    ["SET_AT", "A", "D", "E", "4", "10"],
    ["SCAN_AT", "A", "", "13"],
    ["SCAN_AT", "X", "", "16"],
    ["SCAN_AT", "X", "", "17"],
]

results = process_queries(queries=queries)
for qidx in range(len(queries)):
    print(f"Query {qidx+1}: {results[qidx]}")

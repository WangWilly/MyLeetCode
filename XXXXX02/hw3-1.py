ACTION_ADD_FILE = "ADD_FILE"
ACTION_GET_FILE_SIZE = "GET_FILE_SIZE"
ACTION_MOVE_FILE = "MOVE_FILE"
ACTION_GET_LARGEST_N = "GET_LARGEST_N"
ACTION_GET_VERSION = "GET_VERSION"
ACTION_DELETE_VERSION = "DELETE_VERSION"

action_set: set[str] = {
    ACTION_ADD_FILE,
    ACTION_GET_FILE_SIZE,
    ACTION_MOVE_FILE,
    ACTION_GET_LARGEST_N,
    ACTION_GET_VERSION,
    ACTION_DELETE_VERSION,
}

def process_queries(queries: list[list[str]]) -> list[str]:
    res: list[str] = []

    file_sizes: dict[str, list[int]] = {}

    for q in queries:
        action, data = q[0], q[1:]

        if action not in action_set:
            raise Exception("action not found")

        if action == ACTION_ADD_FILE:
            file_name, new_file_size = data[0], int(data[1])

            if file_name in file_sizes:
                file_sizes[file_name].append(new_file_size)
                res.append("overwritten")
                continue
            file_sizes[file_name] = [new_file_size]
            res.append("created")

        elif action == ACTION_GET_FILE_SIZE:
            file_name = data[0]

            if file_name not in file_sizes:
                res.append("")
                continue
            res.append(file_sizes[file_name][-1])

        elif action == ACTION_MOVE_FILE:
            name_from, name_to = data[0], data[1]

            if name_from not in file_sizes:
                res.append("false")
                continue
            if name_to in file_sizes:
                res.append("false")
                continue
            file_sizes[name_to] = file_sizes[name_from]
            del file_sizes[name_from]

            res.append("true")

        elif action == ACTION_GET_LARGEST_N:
            prefix, n = data[0], int(data[1])
            files = sorted(
                filter(lambda file: prefix == file[0][:len(prefix)], file_sizes.items()), 
                key=lambda file: (-file[1][-1], file[0]),
            )[:n]

            display: str = ",".join([f"{f[0]}({f[1][-1]})" for f in files])
            res.append(display)

        elif action == ACTION_GET_VERSION:
            file_name, version = data[0], int(data[1]) - 1
            if file_name not in file_sizes or version >= len(file_sizes[file_name]):
                res.append("")
                continue
            res.append(file_sizes[file_name][version])

        elif action == ACTION_DELETE_VERSION:
            file_name, version = data[0], int(data[1]) - 1
            if file_name not in file_sizes or version >= len(file_sizes[file_name]):
                res.append("false")
                continue
            file_sizes[file_name].pop(version)
            res.append("true")

    return res

queries = [
    ["ADD_FILE",       "/file-a.txt", "6"],
    ["ADD_FILE",       "/file-a.txt", "3"],
    ["GET_VERSION",    "/file-a.txt", "2"],
    ["GET_VERSION",    "/file-a.txt", "4"],
    ["GET_VERSION",    "/file-a.txt", "1"],
    ["DELETE_VERSION", "/file-a.txt", "1"],
    ["GET_VERSION",    "/file-a.txt", "1"],
]

results = process_queries(queries=queries)
for ridx in range(len(results)):
    print(f"Query{ridx+1}: {results[ridx]}")

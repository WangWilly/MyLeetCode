# aHR0cHM6Ly9sZWV0Y29kZS5jb20vcGxheWdyb3VuZC9nODc5d2htUw==

ACTION_ADD_FILE = "ADD_FILE"
ACTION_GET_FILE_SIZE = "GET_FILE_SIZE"
ACTION_MOVE_FILE = "MOVE_FILE"

action_set: set[str] = {
    ACTION_ADD_FILE,
    ACTION_GET_FILE_SIZE,
    ACTION_MOVE_FILE,
}

def process_queries(queries: list[list[str]]) -> list[str]:
    res: list[str] = []

    file_sizes: dict[str, int] = {}

    for q in queries:
        action, data = q[0], q[1:]

        if action not in action_set:
            raise Exception("action not found")

        if action == ACTION_ADD_FILE:
            file_name, new_file_size = data[0], int(data[1])

            if file_name in file_sizes:
                file_sizes[file_name] = new_file_size
                res.append("overwritten")
                continue
            file_sizes[file_name] = new_file_size
            res.append("created")

        elif action == ACTION_GET_FILE_SIZE:
            file_name = data[0]

            if file_name not in file_sizes:
                res.append("")
                continue
            res.append(file_sizes[file_name])

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

    return res

queries = [
    ["ADD_FILE",      "/file-a.txt",             "4"],
    ["ADD_FILE",      "/file-a.txt",             "8"],
    ["ADD_FILE",      "/dir-a/dir-c/file-b.txt", "10"],
    ["ADD_FILE",      "/dir-a/dir-c/file-c.txt", "20"],
    ["ADD_FILE",      "/dir-b/file-f.txt",       "3"],
    ["GET_FILE_SIZE", "/file-a.txt"],
    ["GET_FILE_SIZE", "/file-c.txt"],
    ["MOVE_FILE",     "/dir-b/file-f.txt", "/dir-c/file-f.txt"],
    ["MOVE_FILE",     "/dir-b/file-a.txt", "/dir-c/file-f.txt"],
    ["MOVE_FILE",     "/file-a.txt",       "/dir-b/file-f.txt"],
]

results = process_queries(queries=queries)
for ridx in range(len(results)):
    print(f"Query{ridx+1}: {results[ridx]}")

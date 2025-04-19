ACTION_ADD_FILE = "ADD_FILE"
ACTION_GET_FILE_SIZE = "GET_FILE_SIZE"
ACTION_MOVE_FILE = "MOVE_FILE"
ACTION_GET_LARGEST_N = "GET_LARGEST_N"
ACTION_ADD_USER = "ADD_USER"
ACTION_ADD_FILE_BY = "ADD_FILE_BY"
ACTION_MERGE_USER = "MERGE_USER"

action_set: set[str] = {
    ACTION_ADD_FILE,
    ACTION_GET_FILE_SIZE,
    ACTION_MOVE_FILE,
    ACTION_GET_LARGEST_N,
    ACTION_ADD_USER,
    ACTION_ADD_FILE_BY,
    ACTION_MERGE_USER,
}

def process_queries(queries: list[list[str]]) -> list[str]:
    res: list[str] = []

    class File:
        def __init__(self, owner: str, size: int):
            self.owner = owner
            self.size = size

    # file_sizes: dict[str, int] = {}
    all_files: dict[str, File] = {}

    class User:
        def __init__(self, capacity: int):
            self.capacity = capacity
            self.curr_cap = 0
            self.my_file_size: dict[str, int] = {}

        def add_file(self, file_id: str, size: int) -> bool:
            old_size = 0
            if file_id in self.my_file_size:
                old_size = self.my_file_size[file_id]

            if self.capacity != -1 and self.curr_cap - old_size + size > self.capacity:
                return False

            self.my_file_size[file_id] = size
            self.curr_cap -= old_size
            self.curr_cap += size
            return True
        
        def remain(self) -> int:
            return self.capacity - self.curr_cap
            
    
    users: dict[str, User] = {
        "admin": User(capacity=-1),
    }

    for q in queries:
        action, data = q[0], q[1:]

        if action not in action_set:
            raise Exception("action not found")

        if action == ACTION_ADD_FILE:
            file_name, new_file_size = data[0], int(data[1])

            users["admin"].add_file(file_id=file_name, size=new_file_size)
            # if file_name in file_sizes:
            #     file_sizes[file_name] = new_file_size
            #     res.append("overwritten")
            #     continue
            # file_sizes[file_name] = new_file_size
            # res.append("true")
            if file_name in all_files:
                all_files[file_name] = File(owner="admin", size=new_file_size)
                res.append("true")
                continue
            all_files[file_name] = File(owner="admin", size=new_file_size)
            res.append("true")

        elif action == ACTION_GET_FILE_SIZE:
            file_name = data[0]

            # if file_name not in file_sizes:
            #     res.append("")
            #     continue
            # res.append(file_sizes[file_name])
            if file_name not in all_files:
                res.append("")
                continue
            res.append(all_files[file_name].size)


        elif action == ACTION_MOVE_FILE:
            name_from, name_to = data[0], data[1]

            # if name_from not in file_sizes:
            #     res.append("false")
            #     continue
            # if name_to in file_sizes:
            #     res.append("false")
            #     continue
            # file_sizes[name_to] = file_sizes[name_from]
            # del file_sizes[name_from]
            if name_from not in all_files:
                res.append("false")
                continue
            if name_to in all_files:
                res.append("false")
                continue
            all_files[name_to] = all_files[name_from]
            del all_files[name_from]

            res.append("true")

        elif action == ACTION_GET_LARGEST_N:
            prefix, n = data[0], int(data[1])
            # files = sorted(
            #     filter(lambda file: prefix == file[0][:len(prefix)], file_sizes.items()), 
            #     key=lambda file: (-file[1], file[0]),
            # )[:n]
            files = sorted(
                filter(lambda file: prefix == file[0][:len(prefix)], all_files.items()), 
                key=lambda file: (-file[1].size, file[0]),
            )[:n]

            display: str = ",".join([f"{f[0]}({f[1].size})" for f in files])
            res.append(display)
        
        elif action == ACTION_ADD_USER:
            user_id, cap = data[0], int(data[1])
            if user_id in users:
                res.append("false")
                continue
            users[user_id] = User(capacity=cap)
            res.append("true")

        elif action == ACTION_ADD_FILE_BY:
            user_id, file_name, new_file_size = data[0], data[1], int(data[2])

            if file_name in all_files and all_files[file_name].owner != user_id:
                res.append("")
                continue
            if not users[user_id].add_file(file_id=file_name, size=new_file_size):
                res.append("")
                continue
            # file_sizes[file_name] = new_file_size
            if file_name not in all_files:
                all_files[file_name] = File(owner=user_id, size=new_file_size)    
            all_files[file_name].size = new_file_size
            res.append(users[user_id].remain())
        
        elif action == ACTION_MERGE_USER:
            user_to, user_from = data[0], data[1]
            if user_to == "admin" or user_from == "admin":
                res.append("")
                continue
            if user_to == user_from:
                res.append("")
                continue
            if user_to not in users or user_from not in users:
                res.append("")
                continue
            user_to_instance = users[user_to]
            user_from_instance = users[user_from]
            user_to_instance.capacity += user_from_instance.capacity
            for f in user_from_instance.my_file_size.items():
                user_to_instance.add_file(file_id=f[0], size=f[1])
            del user_from_instance
            res.append(user_to_instance.remain())

    return res

queries = [
    ["ADD_USER", "user1", "200"],
    ["ADD_USER", "user1", "100"],
    ["ADD_FILE_BY", "user1", "/dir/file.med", "50"],
    ["ADD_FILE_BY", "user1", "/file.big", "140"],
    ["ADD_FILE_BY", "user1", "/dir/file.small", "20"],
    ["ADD_FILE", "/dir/admin_file", "300"],
    ["ADD_USER", "user2", "110"],
    ["ADD_FILE_BY", "user2", "/dir/file.med", "45"],
    ["ADD_FILE_BY", "user2", "/new_file", "50"],
    ["MERGE_USER", "user1", "user2"],
]

results = process_queries(queries=queries)
for ridx in range(len(queries)):
    print(f"Query{ridx+1}: {results[ridx]}")

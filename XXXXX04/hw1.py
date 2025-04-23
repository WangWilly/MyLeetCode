
action_set: set[str] = {
    "ADD_WORKER",
    "REGISTER",
    "GET",
}

def process_queries(queries: list[list[str]]) -> list[str]:
    res: list[str] = []

    class RegRecord:
        def __init__(self, enter_time: int, curr_compansation: int):
            self.enter_time = enter_time
            self.leave_time = None
            self.curr_compansation = curr_compansation
        
        def is_left(self) -> bool:
            return not self.leave_time == None

        def set_leave(self, leave_time: int):
            self.leave_time = leave_time

        def get_time(self) -> int:
            if not self.is_left():
                return 0
            return self.leave_time - self.enter_time

        def get_salary(self) -> int:
            return self.get_time() * self.curr_compansation
    
    class WorkerInfo:
        def __init__(self, position: str, curr_compansation: int):
            self.position = position
            self.curr_compansation = curr_compansation
            self.records: list[RegRecord] = []
        
        def add_time(self, timestamp: int):
            if len(self.records) == 0 or self.records[-1].is_left():
                self.records.append(RegRecord(timestamp, self.curr_compansation))
                return
            self.records[-1].set_leave(timestamp)
        
        def get_all_time(self)->int:
            time_res = 0
            for r in self.records:
                time_res += r.get_time()
            return time_res

    workers: dict[str, WorkerInfo] = {}

    for q in queries:
        action, data = q[0], q[1:]
        
        if action not in action_set:
            raise Exception(f"action {action} not in list")
        
        if action == "ADD_WORKER":
            worker_id, position, compansation = data[0], data[1], int(data[2])
            if worker_id in workers:
                res.append("false")
                continue
            workers[worker_id] = WorkerInfo(position, compansation)
            res.append("true")

        elif action == "REGISTER":
            worker_id, timestamp = data[0], int(data[1])
            if worker_id not in workers:
                res.append("invalid_request")
                continue
            w = workers[worker_id]
            w.add_time(timestamp)
            res.append("registered")

        elif action == "GET":
            worker_id = data[0]
            if worker_id not in workers:
                res.append("")
                continue
            w = workers[worker_id]
            res.append(w.get_all_time())

    return res

queries = [
    ["ADD_WORKER", "Ashley", "Middle Developer", "150"],
    ["ADD_WORKER", "Ashley", "Junior Developer", "100"],
    ["REGISTER", "Ashley", "10"],
    ["REGISTER", "Ashley", "25"],
    ["GET", "Ashley"],
    ["REGISTER", "Ashley", "40"],
    ["REGISTER", "Ashley", "67"], 
    ["REGISTER", "Ashley", "100"],
    ["GET", "Ashley"],
    ["GET", "Walter"],
    ["REGISTER", "Walter", "120"],
]

results = process_queries(queries=queries)
for ridx in range(len(results)):
    print(f"Query{ridx+1}: {results[ridx]}")

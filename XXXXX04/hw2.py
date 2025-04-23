
action_set: set[str] = {
    "ADD_WORKER",
    "REGISTER",
    "GET",
    "TOP_N_WORKERS",
}

def process_queries(queries: list[list[str]]) -> list[str]:
    res: list[str] = []

    class Position:
        def __init__(self, pos: str, compen: int):
            self.pos = pos
            self.compen = compen

    ############################################################################

    class Record:
        def __init__(self, time_start: int, pos_inst: Position):
            self.time_start = time_start
            self.time_end = None
            self.pos_inst = pos_inst

        def is_complete(self):
            return self.time_end != None
        
        def clockout(self, timestamp: int):
            self.time_end = timestamp

        def get_time(self) -> int:
            if self.time_end == None:
                return 0
            return self.time_end - self.time_start

    ############################################################################

    class WorkerInfo:
        def __init__(self, pos: str, compen: int):
            self.pos_list: list[Position] = [Position(pos, compen)]
            self.records: list[Record] = []
        
        def reg(self, timestamp: int):
            if len(self.records) == 0 or self.records[-1].is_complete():
                self.records.append(Record(timestamp, self.pos_list[-1]))
                return
            self.records[-1].clockout(timestamp)
        
        def get_all_time(self):
            t = 0
            for r in self.records:
                t += r.get_time()
            return t
        
        def has_pos(self, pos: str) -> bool:
            for p in self.pos_list:
                if pos == p.pos:
                    return True
            return False

        def get_pos_time(self, pos: str) -> int:
            t = 0
            for r in self.records:
                if r.pos_inst.pos != pos:
                    continue
                t += r.get_time()
            return t

    workers: dict[str, WorkerInfo] = {}

    ############################################################################

    for q in queries:
        action, data = q[0], q[1:]

        if action not in action_set:
            raise Exception(f"action {action} not listed")

        if action == "ADD_WORKER":
            worker_id, position, compensation = data[0], data[1], data[2]
            if worker_id in workers:
                res.append("false")
                continue
            workers[worker_id] = WorkerInfo(position, compensation)
            res.append("true")
            pass

        elif action == "REGISTER":
            worker_id, timestamp = data[0], int(data[1])
            if worker_id not in workers:
                res.append("invalid_request")
                continue
            w = workers[worker_id]
            w.reg(timestamp)
            res.append("registered")
            pass

        elif action == "GET":
            worker_id = data[0]
            if worker_id not in workers:
                res.append("")
                continue
            w = workers[worker_id]
            res.append(w.get_all_time())
            pass

        elif action == "TOP_N_WORKERS":
            n, position = int(data[0]), data[1]
            filtered = sorted(
                filter(
                    lambda x : x[1].has_pos(position),
                    workers.items(),
                ),
                key=lambda x : (-x[1].get_pos_time(position), x[0]),
            )[:n]
            res_str = ", ".join([f"{x[0]}({x[1].get_pos_time(position)})" for x in filtered])
            res.append(res_str)
            pass

    return res
        

queries = [
    ["ADD_WORKER", "John", "Junior Developer", "120"],
    ["ADD_WORKER", "Jason", "Junior Developer", "120"],
    ["ADD_WORKER", "Ashley", "Junior Developer", "120"],
    ["REGISTER", "John", "100"],
    ["REGISTER", "John", "150"],
    ["REGISTER", "Jason", "200"],
    ["REGISTER", "Jason", "250"],
    ["REGISTER", "Jason", "275"],
    ["TOP_N_WORKERS", "5", "Junior Developer"],
    ["TOP_N_WORKERS", "1", "Junior Developer"],
    ["REGISTER", "Ashley", "400"],
    ["REGISTER", "Ashley", "500"],
    ["REGISTER", "Jason",  "575"],
    ["TOP_N_WORKERS", "3",  "Junior Developer"],
    ["TOP_N_WORKERS", "3",  "Middle Developer"],
]

results = process_queries(queries=queries)
for ridx in range(len(results)):
    print(f"Query{ridx+1}: {results[ridx]}")

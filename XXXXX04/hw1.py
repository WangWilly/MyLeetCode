# aHR0cDovLzUyMDE5My54eXovRGlzY3V6LzFwb2ludDNhY3Jlcy90aHJlYWQtNGU2ZWY4ZC0xLTEuaHRtbA==
# aHR0cDovLzUyMDE5My54eXovRGlzY3V6LzFwb2ludDNhY3Jlcy90aHJlYWQtNjM2YThiYy0xLTEuaHRtbA==
# aHR0cDovLzUyMDE5My54eXovRGlzY3V6LzFwb2ludDNhY3Jlcy90aHJlYWQtM2I5ZTcyNy0xLTEuaHRtbA==

action_set: set[str] = {
    "ADD_WORKER",
    "REGISTER",
    "GET",
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

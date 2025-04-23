
action_set: set[str] = {
    "ADD_WORKER",
    "REGISTER",
    "GET",
    "TOP_N_WORKERS",
    "PROMOTE",
    "CALC_SALARY",
}

def process_queries(queries: list[list[str]]) -> list[str]:
    res: list[str] = []

    class Position:
        # def __init__(self, pos: str, compen: int):
        #     self.pos = pos
        #     self.compen = compen
        def __init__(self, pos: str, compen: int, time_start: int):
            self.pos = pos
            self.compen = compen
            self.time_start = time_start

        def ok(self, timestamp: int):
            return timestamp >= self.time_start

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
        
        def get_range_salary(self, time_start: int, time_end: int) -> int:
            if self.time_end == None:
                return 0
            if time_start > self.time_end:
                return 0
            if time_end < self.time_start:
                return 0
            time_end = min(self.time_end, time_end)
            time_start = max(self.time_start, time_start)
            r = (time_end - time_start) * self.pos_inst.compen
            return r

    ############################################################################

    class WorkerInfo:
        def __init__(self, pos: str, compen: int):
            self.pos_list: list[Position] = [Position(pos, compen, 0)]
            self.records: list[Record] = []
        
        def reg(self, timestamp: int):
            pos = self.pos_list[0]
            for p in self.pos_list:
                if not p.ok(timestamp):
                    continue
                pos = p
            if len(self.records) == 0 or self.records[-1].is_complete():
                # self.records.append(Record(timestamp, self.pos_list[-1]))
                self.records.append(Record(timestamp, pos))
                return
            self.records[-1].clockout(timestamp)
        
        def get_all_time(self):
            t = 0
            for r in self.records:
                t += r.get_time()
            return t
        
        def has_pos(self, pos: str) -> bool:
            # for p in self.pos_list:
            #     if pos == p.pos:
            #         return True
            # return False
            if len(self.records) == 0:
                return False
            p = self.records[-1].pos_inst.pos
            return pos == p

        def get_pos_time(self, pos: str) -> int:
            t = 0
            for r in self.records:
                if r.pos_inst.pos != pos:
                    continue
                t += r.get_time()
            return t
        
        def pos_has_record(self) -> bool:
            p = self.pos_list[-1]
            for r in self.records:
                if not r.is_complete():
                    continue
                if r.pos_inst.pos == p.pos:
                    return True
            return False

        # def promote(self, pos: str, compen: int):
        #     self.pos_list.append(Position(pos, compen))
        def promote(self, pos: str, compen: int, time_start: int):
            self.pos_list.append(Position(pos, compen, time_start))

        def calc_salary(self, time_start: int, time_end: int) -> int:
            t = 0
            for r in self.records:
                t += r.get_range_salary(time_start, time_end)
            return t

    workers: dict[str, WorkerInfo] = {}

    ############################################################################

    for q in queries:
        action, data = q[0], q[1:]

        if action not in action_set:
            raise Exception(f"action {action} not listed")

        if action == "ADD_WORKER":
            worker_id, position, compensation = data[0], data[1], int(data[2])
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

        elif action == "PROMOTE":
            worker_id, position, compensation, time_start = data[0], data[1], int(data[2]), int(data[3])
            if worker_id not in workers:
                res.append("invalid_request")
                continue
            w = workers[worker_id]
            if not w.pos_has_record():
                res.append("invalid_request")
                continue
            w.promote(position, compensation, time_start)
            res.append("success")
            pass

        elif action == "CALC_SALARY":
            worker_id, time_start, time_end = data[0], int(data[1]), int(data[2])
            if worker_id not in workers:
                res.append("")
                continue
            w = workers[worker_id]
            res.append(w.calc_salary(time_start, time_end))
            pass

    return res
        

queries = [
    ["ADD_WORKER", "John", "Middle Developer", "200"],
    ["REGISTER", "John", "100"],
    ["REGISTER", "John", "125"],
    ["PROMOTE", "John", "Senior Developer", "500", "200"],
    ["REGISTER", "John", "150"],
    ["PROMOTE", "John", "Senior Developer", "350", "250"],
    ["REGISTER", "John", "300"],
    ["REGISTER", "John", "325"],
    ["CALC_SALARY", "John", "0", "500"],
    ["TOP_N_WORKERS", "3", "Senior Developer"],
    ["REGISTER", "John", "400"],
    ["GET", "John"],
    ["TOP_N_WORKERS", "10", "Senior Developer"],
    ["TOP_N_WORKERS", "10", "Middle Developer"],
    ["CALC_SALARY", "John", "110", "350"],
    ["CALC_SALARY", "John", "900", "1400"],
]

results = process_queries(queries=queries)
for ridx in range(len(results)):
    print(f"Query{ridx+1}: {results[ridx]}")


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
            print(self.leave_time, self.enter_time, self.curr_compansation)
            return self.get_time() * self.curr_compansation
    
    class WorkerInfo:
        def __init__(self, position: str, curr_compansation: int):
            # self.position = position
            # self.curr_compansation = curr_compansation
            # self.compansations = []
            # self.records: list[RegRecord] = []
            self.pos_compan: dict[str, (int, int)] = {position: (-1, curr_compansation)}
            self.pos_rec: dict[str, list[RegRecord]] = {}
            self.is_still_in = ""

        def promote(self, position: str, compansation: int, start_time: int):
            self.pos_compan[position] = (start_time, compansation)
        
        def add_time(self, timestamp: int):
            if self.is_still_in != "":
                self.pos_rec[self.is_still_in][-1].set_leave(timestamp)
                self.is_still_in = ""
                return
            pos = ""
            compan = 0
            for c in sorted(self.pos_compan.items(), key=lambda pc : pc[1][0]):
                if c[1][0] < timestamp:
                    pos = c[0]
                    compan = c[1][1]
            if pos not in self.pos_rec:
                self.pos_rec[pos] = []

            # if len(self.records) == 0 or self.records[-1].is_left():
            if len(self.pos_rec[pos]) == 0 or self.pos_rec[pos][-1].is_left():
                # self.records.append(RegRecord(timestamp, compan))
                self.pos_rec[pos].append(RegRecord(timestamp, compan))
                self.is_still_in = pos
                return
            # self.records[-1].set_leave(timestamp)
            # self.pos_rec[pos][-1].set_leave(timestamp)
            # self.is_still = False
        
        def get_all_time(self)->int:
            time_res = 0
            for pr in self.pos_rec.items():
                for r in pr[1]:
                    time_res += r.get_time()
            return time_res

        def get_time(self, pos: str) -> int:
            if pos not in self.pos_rec:
                return -1
            all_time = 0
            for r in self.pos_rec[pos]:
                all_time += r.get_time()
            return all_time
        
        def get_salary(self, start_time: int, end_time: int) -> int:
            # salary_sum = 0
            # for r in self.records:
            #     if not r.is_left():
            #         continue
            #     if r.enter_time < start_time or r.leave_time > end_time:
            #         continue
            #     salary_sum += r.get_salary()
            salary_sum = 0
            for pr in self.pos_rec.items():
                for r in pr[1]:
                    if not r.is_left():
                        continue
                    if r.enter_time < start_time or r.leave_time > end_time:
                        continue
                    salary_sum += r.get_salary()
            return salary_sum



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

        elif action == "TOP_N_WORKERS":
            n, position = int(data[0]), data[1]
            filtered = sorted(
                filter(
                    lambda worker : worker[1].get_time(position) != -1,
                    workers.items(),
                ),
                key=lambda worker : (-worker[1].get_time(position), worker[0])
            )[:n]

            res_str = ", ".join([f"{w[0]}({w[1].get_time(position)})" for w in filtered])
            res.append(res_str)

        elif action == "PROMOTE":
            worker_id, new_position, new_compansation, start_time = data[0], data[1], int(data[2]), int(data[3])
            if worker_id not in workers:
                res.append("invalid_request")
                continue
            w = workers[worker_id]
            # if len(w.records) == 0 or not w.records[-1].is_left():
            #     res.append("invalid_request")
            #     continue
            if w.is_still_in != "":
                res.append("invalid_request")
                continue
            w.promote(new_position, new_compansation, start_time)
            res.append("success")
        
        elif action == "CALC_SALARY":
            worker_id, start_time, end_time = data[0], int(data[1]), int(data[2])
            if worker_id not in workers:
                res.append("")
                continue
            w = workers[worker_id]
            res.append(w.get_salary(start_time, end_time))

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

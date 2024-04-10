class Service_time_struct:
    def __init__(self):
        self.arrival = None
        self.depart = None
        self.duration = None

class Service_status_struct:
    def __init__(self):
        self.service_time = Service_time_struct()
        self.status = 'idle'
        self.group = None

class Service_idle_struct:
    def __init__(self):
        self.idle_pos = None
        self.all_idle = True

    def clear(self):
        self.idle_pos = None
        self.all_idle = True

class Service_depart_struct:
    def __init__(self):
        self.service_time = Service_time_struct()
        self.group = None
        self.result = None

class Server:
    def __init__(self, n, n0, t_limit):
        service_status_group0 = [Service_status_struct() for _ in range(n0)]
        service_status_group1 = [Service_status_struct() for _ in range(n - n0)]
        self.service_status = (service_status_group0, service_status_group1)
        self.t_limit = t_limit
        self.idle = Service_idle_struct()
        self.depart = Service_depart_struct()

    def check_idle(self, group):
        self.idle.clear()
        service_status_group = self.service_status[group]
        for idx in range(0, len(service_status_group)):
            if service_status_group[idx].status == 'idle':
                self.idle.idle_pos = idx
            else:
                self.idle.all_idle = False
        return self.idle

    def check_depart(self, master_clock):
        for group in (0, 1):
            for ss in self.service_status[group]:
                if ss.status == 'busy' and master_clock >= ss.service_time.depart:
                    if group == 0 and ss.service_time.duration > self.t_limit:
                        self.depart.result = 'timeout'
                    else:
                        if group == 1 and ss.group == 0:
                            self.depart.result = 're_circ'
                        else:
                            self.depart.result = 'ok'
                    self.depart.service_time.arrival = ss.service_time.arrival
                    self.depart.service_time.depart = ss.service_time.depart
                    self.depart.service_time.duration = ss.service_time.duration
                    self.depart.group = ss.group
                    ss.status = 'idle'
                    return self.depart
        return None
    
    def append_service(self, arrival, duration, group, master_clock, idle_pos, re_circ=False):
        if re_circ:
            group = 1

        self.service_status[group][idle_pos].status = 'busy'
        self.service_status[group][idle_pos].service_time.arrival = arrival
        if group == 0 and duration > self.t_limit:
            self.service_status[group][idle_pos].service_time.depart = master_clock + self.t_limit
        else:
            self.service_status[group][idle_pos].service_time.depart = master_clock + duration
            if re_circ:
                self.service_status[group][idle_pos].group = 0
            else:
                self.service_status[group][idle_pos].group = group
        self.service_status[group][idle_pos].service_time.duration = duration

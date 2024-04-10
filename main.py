import readWriteFile
import randomData
import server
import sys
import seed

if __name__ == '__main__':
    rwf = readWriteFile.ReadWriteFile(sys.argv[1])
    config = rwf.get_config()
    if config[0] == 'trace':
        mode, n, n0, t_limit, interarrival_list, time_group_list = config
    else:
        mode, n, n0, t_limit, time_end, lambd, alpha2l, alpha2u, p0, alpha0, beta0, eta0, alpha1, eta1 = config
        rd = randomData.RandomData(seed.seed, p0, alpha0, beta0, eta0, alpha1, eta1, lambd, alpha2l, alpha2u)
        interarrival_list = list()
        time_group_list = list()
        for i in range(3 * time_end):
            interarrival, time, group = rd.generate_service()
            interarrival_list.append(interarrival)
            time_group_list.append((time, group))

    arrival_time = 0
    arrival_time_list = []
    for ia in interarrival_list:
        arrival_time += ia
        arrival_time_list.append(arrival_time)

    master_clock = 0
    clock_increment = 0.0001

    server = server.Server(n, n0, t_limit)
    queue = [list(), list()]
    list_empty = False
    queue_empty = [False, False]

    while True:
        depart = server.check_depart(master_clock)
        if depart is not None:
            if depart.result == 'ok':
                rwf.write(depart.service_time.arrival, depart.service_time.depart, depart.service_time.duration, depart.group)
            elif depart.result == 're_circ':
                rwf.write(depart.service_time.arrival, depart.service_time.depart, depart.service_time.duration, 'r0')
            elif depart.result == 'timeout':
                idle = server.check_idle(1)
                if idle.idle_pos is not None:
                    server.append_service(depart.service_time.arrival, depart.service_time.duration, 1, master_clock, idle.idle_pos, True)
                else:
                    queue[1].append((depart.service_time.arrival, depart.service_time.duration, 0))

        for group in (0, 1):
            if len(queue[group]) != 0:
                idle = server.check_idle(group)
                if idle.idle_pos is not None:
                    arrival_time = queue[group][0][0]
                    service_time = queue[group][0][1]
                    service_group = queue[group][0][2]

                    if group == 1 and service_group == 0:
                        server.append_service(arrival_time, service_time, 1, master_clock, idle.idle_pos, True)
                    else:
                        server.append_service(arrival_time, service_time, group, master_clock, idle.idle_pos)
                    
                    queue[group].pop(0)
                queue_empty[group] = False
            else:
                queue_empty[group] = True

        if not list_empty:
            try:
                arrival_time = arrival_time_list[0]
                service_time, service_group = time_group_list[0]
            except IndexError:
                list_empty = True
            else:
                if mode == 'random' and master_clock >= time_end:
                    list_empty = True
                if master_clock >= arrival_time:
                    idle = server.check_idle(service_group)
                    if idle.idle_pos is not None:
                        server.append_service(arrival_time, service_time, service_group, master_clock, idle.idle_pos)
                    else:
                        queue[service_group].append((arrival_time, service_time, service_group))
                    
                    arrival_time_list.pop(0)
                    time_group_list.pop(0)
        
        if list_empty and queue_empty[0] and queue_empty[1] and server.check_idle(0).all_idle and server.check_idle(1).all_idle:
            rwf.completed()
            break

        master_clock += clock_increment
import os

class ReadWriteFile:
    def __init__(self, num):
        self.num = num
        self.service_list = list()
        self.rt0 = list()
        self.rt1 = list()
        self.time0 = list()
        self.time1 = list()

    def get_config(self):
        mode_path = os.path.join('config', 'mode_{}.txt'.format(self.num))
        para_path = os.path.join('config', 'para_{}.txt'.format(self.num))
        interarrival_path = os.path.join('config', 'interarrival_{}.txt'.format(self.num))
        service_path = os.path.join('config', 'service_{}.txt'.format(self.num))

        with open(mode_path, 'r') as f:
            mode = f.read().strip()

        with open(para_path, 'r') as f:
            n = int(f.readline().strip())
            n0 = int(f.readline().strip())
            t_limit = float(f.readline().strip())
            if mode == 'random':
                time_end = int(f.readline().strip())

        with open(interarrival_path, 'r') as f:
            if mode == 'trace':
                interarrival_list = [float(line.strip()) for line in f]
            else:
                lambd, alpha2l, alpha2u = [float(_) for _ in f.readline().strip().split()]

        with open(service_path, 'r') as f:
            if mode == 'trace':
                time_group_list = [(float(line.split()[0]), int(line.split()[1])) for line in f]
            else:
                p0 = float(f.readline().strip())
                alpha0, beta0, eta0 = [float(_) for _ in f.readline().strip().split()]
                alpha1, eta1 = [float(_) for _ in f.readline().strip().split()]
        
        if mode == 'trace':
            return (
                mode,
                n,
                n0,
                t_limit,
                interarrival_list,
                time_group_list
            )
        else:
            return (
                mode,
                n,
                n0,
                t_limit,
                time_end,
                lambd,
                alpha2l,
                alpha2u,
                p0,
                alpha0,
                beta0,
                eta0,
                alpha1,
                eta1
            )
        
    def write(self, arrival, depart, time, classi):
        self.service_list.append((arrival, depart, classi))
        classi = str(classi)
        if classi == '0':
            self.rt0.append(depart - arrival)
            self.time0.append(time)
        elif classi == '1':
            self.rt1.append(depart - arrival)
            self.time1.append(time)

    def completed(self):
        dep_path = os.path.join('output', 'dep_{}.txt'.format(self.num))
        mrt_path = os.path.join('output', 'mrt_{}.txt'.format(self.num))
        
        with open(dep_path,'w') as f:
            for arrival, depart, classi in self.service_list:
                f.write('{:.4f} {:.4f} {}\n'.format(arrival, depart, classi))
        
        mrt0 = sum(self.rt0) / len(self.rt0)
        mrt1 = sum(self.rt1) / len(self.rt1)

        with open(mrt_path, 'w') as f:
            f.write('{:.4f} {:.4f}\n'.format(mrt0, mrt1))

        if self.num == 'test':
            with open('response_time_group0_test.txt', 'w') as f:
                for rt0, t0 in zip(self.rt0, self.time0):
                    f.write('{} {}\n'.format(rt0, t0))
            with open('response_time_group1_test.txt', 'w') as f:
                for rt1, t1 in zip(self.rt1, self.time1):
                    f.write('{} {}\n'.format(rt1, t1))
                    
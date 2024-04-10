import random

class RandomData:
    def __init__(self, seed, p0, alpha0, beta0, eta0, alpha1, eta1, lambd, alpha2l, alpha2u):
        random.seed(seed)
        self.alpha0 = alpha0
        self.beta0 = beta0
        self.eta0 = eta0
        self.alpha1 = alpha1
        self.eta1 = eta1
        self.lambd = lambd
        self.alpha2l = alpha2l
        self.alpha2u = alpha2u
        self.choice = [0, 1]
        self.weights = [p0, 1 - p0]

    def generate_interarrival(self):
        a1 = random.expovariate(self.lambd)
        a2 = random.uniform(self.alpha2l, self.alpha2u)
        return a1 * a2
    
    def generate_service(self):
        interarrival = self.generate_interarrival()
        g0_icdf = lambda x: (self.alpha0**self.eta0 * self.beta0**self.eta0 / (self.alpha0**self.eta0 * x - self.beta0**self.eta0 * x + self.beta0**self.eta0))**(1 / self.eta0)
        g1_icdf = lambda x: (-self.alpha1**self.eta1 / (x-1))**(1 / self.eta1)

        group = random.choices(self.choice, self.weights)[0]
        p = random.uniform(0, 1)
        if group == 0:
            time = g0_icdf(p)
        else:
            time = g1_icdf(p)
        return (interarrival, time, group)
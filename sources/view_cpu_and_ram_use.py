# Author : matteo dubuisson
# Written in 2023

import numpy as np
from matplotlib import animation as animation, pyplot as plt
import threading as th
from time import sleep
import psutil

limitx = [0, 50]
limity = [0, 100]
periode_in_secondes = 0.5

xs = np.arange(limitx[0], limitx[1], 1, int)
ys_pourcent_ram = np.zeros(len(xs), int)
ys_pourcent_cpu = np.zeros(len(xs), int)

ram_pourcent_graph, = plt.plot(xs, ys_pourcent_ram, "-r")
cpu_pourcent_graph, = plt.plot(xs, ys_pourcent_cpu, "-y")
plt.xlim(limitx[0], limitx[1])
plt.ylim(limity[0], limity[1])
plt.ylabel("Rate of use of CPU/RAM in pourcent")
plt.legend(("ram use in percent", "cpu use in percent"), loc=0)

working = True
def thread_f():
    while working:
        for i in range(len(xs) - 1, 0, -1):
            ys_pourcent_ram[i] = ys_pourcent_ram[i - 1]
            ys_pourcent_cpu[i] = ys_pourcent_cpu[i - 1]
        ys_pourcent_ram[0] = psutil.virtual_memory()[2]
        ys_pourcent_cpu[0] = psutil.cpu_percent(periode_in_secondes) # Does a sleep
        ram_pourcent_graph.set_ydata(ys_pourcent_ram)
        cpu_pourcent_graph.set_ydata(ys_pourcent_cpu)
        plt.xlabel("Current use each {0} => [RAM : {1}] [CPU : {2}]".format(periode_in_secondes, ys_pourcent_ram[0], ys_pourcent_cpu[0]))
        
        plt.draw()

t = th.Thread(target=lambda: thread_f())
t.start()

plt.show()
working = 0
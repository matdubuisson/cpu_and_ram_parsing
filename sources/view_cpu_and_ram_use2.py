# Author : matteo dubuisson
# Written in 2023

import numpy as np
from matplotlib import animation as animation, pyplot as plt
import threading as th
from time import sleep
import psutil

limitx = [0, 200]
limity = [0, 100]
periode_in_secondes = 0.5
ram_infos = psutil.virtual_memory()

xs = np.arange(limitx[0], limitx[1], 1, int)
ys_pourcent_ram = np.zeros(len(xs), int)
ys_pourcent_cpu = np.zeros(len(xs), int)
ys_variation_ram = np.zeros(len(xs), np.float64)

fig, axs = plt.subplots(2, 2)
axs[0][0].set_xlim((limitx[0], limitx[1]))
axs[0][0].set_ylim((0, 110))
axs[0][1].set_xlim((limitx[0], limitx[1]))
axs[0][1].set_ylim((0, 110))
a = ram_infos.total / 1000000000
axs[1][0].set_xlim((limitx[0], limitx[1]))
axs[1][0].set_ylim((-a, a))

graphs = (
    (axs[0][0].plot(xs, ys_pourcent_ram)[0], axs[0][1].plot(xs, ys_pourcent_cpu)[0]),
    (axs[1][0].plot(xs, ys_variation_ram)[0], axs[1][1].plot(xs, ys_variation_ram)[0])
)

axs[0][0].set_title("RAM use in percent")
axs[0][1].set_title("CPU use in percent")
axs[1][0].set_title("RAM precise variation IN GB")
axs[1][1].set_title("RAM variation IN GB")

accuracy_for_ram_variation = 0.1

working = True
def thread_f():
    first = True
    previous_ram_variation = 0
    current_ram_variation = 0
    while working:
        for i in range(len(xs) - 1, 0, -1):
            ys_pourcent_ram[i] = ys_pourcent_ram[i - 1]
            ys_pourcent_cpu[i] = ys_pourcent_cpu[i - 1]
            ys_variation_ram[i] = ys_variation_ram[i - 1]
        ram_infos = psutil.virtual_memory()
        ys_pourcent_ram[0] = ram_infos.percent
        ys_pourcent_cpu[0] = psutil.cpu_percent(periode_in_secondes) # Does a sleep
        previous_ram_variation = current_ram_variation
        current_ram_variation = ram_infos.used / 1000000000
        if first:
            first = False
        else:        
            ys_variation_ram[0] = current_ram_variation - previous_ram_variation
        
        graphs[0][0].set_ydata(ys_pourcent_ram)
        graphs[0][1].set_ydata(ys_pourcent_cpu)
        graphs[1][0].set_ydata(ys_variation_ram)
        graphs[1][1].set_ydata(ys_variation_ram)
        
        axs[0][0].set_xlabel("RAM : {0}%".format(ys_pourcent_ram[0]))
        axs[0][1].set_xlabel("CPU : {0}%".format(ys_pourcent_cpu[0]))
        axs[1][0].set_xlabel("VARIATION : {0} GB".format(np.round(ys_variation_ram[0], 6)))
        axs[1][1].set_xlabel("PERCENT VARIATION : {0} %".format(np.round((np.round(ys_variation_ram[0], 6) / previous_ram_variation) * 100), 6))
        miny = np.round(np.min(ys_variation_ram), 6)
        maxy = np.round(np.max(ys_variation_ram), 6)
        if miny != maxy:
            axs[1][1].set_ylim(miny, maxy)
        
        plt.draw()

t = th.Thread(target=lambda: thread_f())
t.start()

plt.show()
working = 0
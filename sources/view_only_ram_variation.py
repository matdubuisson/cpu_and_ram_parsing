# Author : matteo dubuisson
# Written in 2023

import numpy as np
from matplotlib import animation as animation, pyplot as plt
import threading as th
from time import sleep
import psutil

limitx = [0, 100]
limity = [0, 100]
periode_in_secondes = 0.5
ram_infos = psutil.virtual_memory()

xs = np.arange(limitx[0], limitx[1], 1, int)
ys_variation_ram = np.zeros(len(xs), np.float64)

aux, axs = plt.subplots(1, 1)
fig = axs.plot(xs, ys_variation_ram)[0]

axs.set_title("RAM variation IN GB")

working = True
def thread_f():
    first = True
    previous_ram_variation = 0
    current_ram_variation = 0
    while working:
        for i in range(len(xs) - 1, 0, -1):
            ys_variation_ram[i] = ys_variation_ram[i - 1]
        ram_infos = psutil.virtual_memory()
        previous_ram_variation = current_ram_variation
        current_ram_variation = ram_infos.used / 1000000000
        if first:
            first = False
        else:        
            ys_variation_ram[0] = current_ram_variation - previous_ram_variation
        
        fig.set_ydata(ys_variation_ram)
        
        if previous_ram_variation != 0.0:
            axs.set_xlabel("PERCENT VARIATION : {0} %".format(np.round((np.round(ys_variation_ram[0], 6) / previous_ram_variation) * 100), 6))
        miny = np.round(np.min(ys_variation_ram), 6)
        maxy = np.round(np.max(ys_variation_ram), 6)
        if miny != maxy:
            axs.set_ylim(miny, maxy)
        
        plt.draw()
        sleep(periode_in_secondes)

t = th.Thread(target=lambda: thread_f())
t.start()

plt.show()
working = 0

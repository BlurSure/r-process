#!/usr/bin/env python

import numpy as np

s_list = list(range(12, 52, 2))
s_arr = np.array(s_list)
Ye_list = list(range(200, 435, 5))
Ye_arr = np.array(Ye_list) / 1000

directory = "/mnt/scratch/agarw132/jina/r_process_grid/"
def path(Ye, s):
    filename = "final_y" +str(float(Ye) / 1000.0) + "_s" + str(int(s))
    path = directory + filename
    return path

with open('gridpoints.txt', 'w') as outfile:
    for y in Ye_list:
        for s in s_list:
            outfile.write(str(s) + ' ' + str(float(y) / 1000.0) + ' ' + str(s) + '\n')
            try:
                with open(path(y, s)) as infile:
                    outfile.write(infile.read())

            except:
                print("not found")
                print(y,s)

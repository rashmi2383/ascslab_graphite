import numpy as np
from collections import Counter, defaultdict
import sys
from copy import deepcopy
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

                          
def main():
    dict1, dicttemp, dictdf = defaultdict(list), defaultdict(list), defaultdict(list)
    i = 0
    # filepointer to the output file
    fileptr = "sim.out"

    # open the file for reading
    data = open(fileptr, 'r')
    
    # Read the file to obtain various parameters
    for line in data:
        words = line.split()
        for word in words:
            # Store the start time for the benchmark
            if word == "Start":
                for text in words:
                    if (text.isdigit()):
                        start_time = int(text)
                        dict1["start_time"].append(start_time)  
            # Store the stop time for the benchmark                
            if word == "Stop":
                for text in words:
                    if (text.isdigit()):
                        stop_time = int(text)
                        dict1["stop_time"].append(stop_time)
            # Store the completion times for each thread in the benchmark  
            if word == "Completion":
                for text in words:
                    if (text.isdigit()) and int(text) != 0:
                        dict1["completion_time_threads"].append(int(text))
            # Store the Cache Miss rates for various caches in a temporary dictionary
            if word == "Cache": 
                for text in words:
                    if text == "Misses":
                        dicttemp["Cache Misses"+str(i)].append(words)
                        i += 1

    # Store L1-I Cache, L1-D Cache & L2 Cache Miss Rates in the main dictionary            
    for key in dicttemp:
        if key == "Cache Misses0":
            for values in dicttemp[key]:
                for text in values:
                    if (text.isdigit()) and int(text) != 0:
                        dict1["L1-I Cache Misses"].append(int(text))
        if key == "Cache Misses1":
            for values in dicttemp[key]:
                for text in values:
                    if (text.isdigit()) and int(text) != 0:
                        dict1["L1-D Cache Misses"].append(int(text))
        if key == "Cache Misses2":
            for values in dicttemp[key]:
                for text in values:
                    if (text.isdigit()) and int(text) != 0:
                        dict1["L2 Cache Misses"].append(int(text))

    # Calculate the completion time for the benchmark and store it in main dictionary                  
    completion_time = stop_time - start_time
    dict1["completion_time"].append(completion_time)
    for j in range(1, len(dict1["completion_time_threads"])+1):
        dict1["No_of_Threads"].append(j)

    for key in dict1:
        if key=="No_of_Threads" in dict1:
            dictdf[key]=dict1[key]
        if key=="L1-I Cache Misses" in dict1:
            dictdf[key]=dict1[key]
        if key=="L1-D Cache Misses" in dict1:
            dictdf[key]=dict1[key]
        if key=="L2 Cache Misses" in dict1:
            dictdf[key]=dict1[key]

    df = pd.DataFrame(dictdf, columns = ['No_of_Threads', 'L1-I Cache Misses', 'L1-D Cache Misses', 'L2 Cache Misses'])

    # Create the general blog and the "subplots" i.e. the bars
    f, ax1 = plt.subplots(1, figsize=(10,10))

    # Set the bar width
    bar_width = 0.75

    # positions of the left bar-boundaries
    bar_l = [i+1 for i in range(len(df['L1-I Cache Misses']))] 

    # positions of the x-axis ticks (center of the bars as bar labels)
    tick_pos = [i+(bar_width/2) for i in bar_l] 

    # Create a bar plot, in position bar_1
    ax1.bar(bar_l, 
        # using the L1-I Cache Misses data
        df['L1-I Cache Misses'], 
        # set the width
        width=bar_width,
        # with the label pre score
        label='L1-I Cache Misses', 
        # with alpha 0.5
        alpha=0.5, 
        # with color
        color='#F4561D')

    # Create a bar plot, in position bar_1
    ax1.bar(bar_l, 
        # using the L1-D Cache Misses data
        df['L1-D Cache Misses'], 
        # set the width
        width=bar_width,
        # with L1-I Cache Misses on the bottom
        bottom=df['L1-I Cache Misses'], 
        # with the label mid score
        label='L1-D Cache Misses', 
        # with alpha 0.5
        alpha=0.5, 
        # with color
        color='#F1911E')

    # Create a bar plot, in position bar_1
    ax1.bar(bar_l, 
        # using the L2 Cache Misses data
        df['L2 Cache Misses'], 
        # set the width
        width=bar_width,
        # with L1-I Cache Misses and L1-D Cache Misses on the bottom
        bottom=[i+j for i,j in zip(df['L1-I Cache Misses'],df['L1-D Cache Misses'])], 
        # with the label L2 Cache Misses
        label='L2 Cache Misses', 
        # with alpha 0.5
        alpha=0.5, 
        # with color
        color='#F1BD1A')

    # set the x ticks with names
    plt.xticks(tick_pos, df['No_of_Threads'])

    # Set the label and legends
    ax1.set_ylabel("Cache Misses")
    ax1.set_xlabel("No. of Threads")
    plt.legend(loc='upper left')

    # Set a buffer around the edge
    plt.xlim([min(tick_pos)-bar_width, max(tick_pos)+bar_width])

    plt.savefig('cache_miss')


if __name__ == '__main__':
    main()   

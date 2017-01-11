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

    # read command file in the result folder and extract the benchmark and command run details
    fileptr1 = "command"
    data1 = open(fileptr1,'r')
    s = data1.read()
    lines = s.split('/')
    lines.reverse()
    details = lines[0].strip('\n')
    det_list = details.split(' ', 4 )
    benchmark_name = det_list[0].upper()
    thread_count = det_list[1]
    data1.close()

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

    #Setting the positions and width for the bars
    pos = list(range(len(df['L1-I Cache Misses'])))
    width = 0.25

    # Plotting the bars
    fig, ax = plt.subplots(figsize=(10,5))

    # Create bars
    plt.bar(pos, df['L1-I Cache Misses'], width, alpha=0.5, color='#EE3224', label=df['No_of_Threads'][0])
    plt.bar([p + width for p in pos], df['L1-D Cache Misses'], width, alpha=0.5, color='#F78F1E', label=df['No_of_Threads'][1])
    plt.bar([p + width*2 for p in pos], df['L2 Cache Misses'], width, alpha=0.5, color='#FFC222', label=df['No_of_Threads'][2])

    # Set the y axis label
    ax.set_ylabel('Cache Miss')

    # Set the chart's title
    ax.set_title('Cache Miss Stastics'+' - '+'Benchmark: '+benchmark_name+' - '+'Run with '+thread_count+' threads')

    # Set the position of the x ticks
    ax.set_xticks([p + 1.5 * width for p in pos])

    # Set the labels for the x ticks
    ax.set_xticklabels(df['No_of_Threads'])
    ax.set_xlabel('No. of Threads')

    # Setting the x-axis and y-axis limits
    plt.xlim(min(pos)-width, max(pos)+width*4)
    plt.ylim([0, max(df['L1-I Cache Misses'] + df['L1-D Cache Misses'] + df['L2 Cache Misses'])] )

    # Adding the legend and showing the plot
    plt.legend(['L1-I Cache Misses', 'L1-D Cache Misses', 'L2 Cache Misses'], loc='upper left')
    #plt.grid()
    plt.savefig('Cache Miss APSP')

 

if __name__ == '__main__':
    main()   
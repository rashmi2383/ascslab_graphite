import numpy as np
from collections import Counter, defaultdict
import sys
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import simplejson

def if_float_value(float_number):
    try:
        float(float_number)
        return True
    except ValueError:
        return False

def draw_cache_miss_chart(dictdf, graph_algorithm, thread_count):
    # data frame for Cache Miss Rates        
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
    ax.set_ylabel('Cache Miss Rate (In Percentage)')
    # Set the chart's title
    ax.set_title('Cache Miss Rates'+' - '+'Graph Algorithm: '+graph_algorithm+' - '+'Run with '+thread_count+' threads')
    # Set the position of the x ticks
    ax.set_xticks([p + 1.5 * width for p in pos])
    # Set the labels for the x ticks
    ax.set_xticklabels(df['No_of_Threads'])
    ax.set_xlabel('No. of Threads')
    # Setting the x-axis and y-axis limits
    plt.xlim(min(pos)-width, max(pos)+width*4)
    plt.ylim([0, max(df['L1-I Cache Misses'] + df['L1-D Cache Misses'] + df['L2 Cache Misses'])] )
    # Adding the legend and showing the plot
    plt.legend(['L1-I Cache Miss Rate (Scaled by 40)', 'L1-D Cache Miss Rate (Scaled by 20)', 'L2 Cache Miss Rate'], loc='upper left')
    plt.savefig('Cache Miss '+graph_algorithm+' '+thread_count)    

def draw_bar_chart(dictdftemp, graph_algorithm, thread_count):
    column_list = dictdftemp.keys()
    # data frame for Network Latency       
    df1 = pd.DataFrame(dictdftemp, columns = [column_list[0], column_list[1]]) 
    #Setting the positions and width for the bars
    bar_l = [i+1 for i in range(len(df1[column_list[1]]))] 
    width = 0.5
    # positions of the x-axis ticks (center of the bars as bar labels)
    tick_pos = [i+(width/10) for i in bar_l] 
    # Plotting the bars
    fig, ax = plt.subplots(figsize=(10,5))
    # Create bar
    ax.bar(bar_l, df1[column_list[1]], width, alpha=0.5, color='b', label=column_list[1])
    # Set the position of the x ticks
    plt.xticks(tick_pos, df1[column_list[0]])
    # Set the y axis label
    if column_list[1] == 'Network Latency':
        ax.set_ylabel('Average packet latency')
    if column_list[1] == 'Throughput':
        ax.set_ylabel('Bits sent per second')
    if column_list[1] == 'Completion Time':
        ax.set_ylabel('Completion time (in nanoseconds)')
    if column_list[1] == "CPU Performance":
        ax.set_ylabel('Instructions per cycle')
    # Set the x axis label
    ax.set_xlabel('No. of Threads')
    # Set the chart's title
    ax.set_title(column_list[1]+' - '+'Graph Algorithm: '+graph_algorithm+' - '+'Run with '+thread_count+' threads')
    plt.savefig(column_list[1]+' '+graph_algorithm+' '+thread_count)

              
def main():
    dict1, dicttemp, dictdf, dictdf4, dicttempInstr = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    dicttemplatency, dict1tempbits, dictdf2, dictdf3, dictdf5 = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    dictfile = defaultdict(list)
    listtmp1, listtmp2, listtmp3 = [], [], []
    i, j, k = 0, 0 , 0
    # read command file in the result folder and extract the benchmark and command run details
    fileptr1 = "command"
    data1 = open(fileptr1,'r')
    s = data1.read()
    lines = s.split('/')
    lines.reverse()
    details = lines[0].strip('\n')
    det_list = details.split(' ', 4 )
    graph_algorithm = det_list[0].upper()
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
            if word == "Miss": 
                for text in words:
                    if text == "Rate":
                        dicttemp["Cache Misses"+str(i)].append(words)
                        i += 1
            # Store the packet latency for each thread in the benchmark
            if word == "Average":
                for text in words:
                    if text == "Packet":
                        dicttemplatency["Packet Latency"+str(j)].append(words)
                        j += 1
            # Store the total packets sent for each thread in the benchmark
            if word == "Bits":
                for text in words:
                    if text == "Sent":  
                        dict1tempbits["Total bits sent"+str(k)].append(words)
                        k += 1
            # Store the total Instructions executed for each thread
            if word == "Total":
                for text in words:
                    if text == "Instructions":
                        dicttempInstr["Total Instructions"].append(words)
    del dict1tempbits["Total bits sent0"]                   
    del dicttemplatency["Packet Latency0"]
    del dicttemplatency["Packet Latency1"]
    del dicttemplatency["Packet Latency3"]
    # Store Average Packet Latency in the main dictionary
    counter_thread = int(thread_count)
    for values in dicttemplatency["Packet Latency2"]:
        for text in values:
            if (if_float_value(text)) and float(text) != 0:
                if counter_thread != 0:
                    dict1["Network Latency"].append(float(text))
                    counter_thread -= 1
    # Store total bits sent Values in the main dictionary & calculate throughput
    counter_thread = int(thread_count)
    for values in dict1tempbits["Total bits sent1"]:
        for text in values:
            if (text.isdigit()):
                if counter_thread != 0:
                    dict1["Total bits sent"].append(int(text))
                    counter_thread -= 1
    for key in dict1:
        if key=="Total bits sent" in dict1:
            listtmp1 = dict1[key]
        if key=="completion_time_threads" in dict1:
            listtmp2 = dict1[key]
    for i in range(0,len(listtmp1)):
        dict1["Throughput"].append((float(listtmp1[i])/listtmp2[i]) * (10**9))
    del listtmp1
    # Store total Instructions in the main dictionary & calculate IPC 
    for values in dicttempInstr["Total Instructions"]:
        for text in values:
            if (text.isdigit()) and int(text) != 0:
                dict1["Total Instructions"].append(int(text))
    for key in dict1:
        if key == "Total Instructions" in dict1:
            listtmp1 = dict1[key]
    for i in range(0,len(listtmp1)):
        dict1["IPC"].append((float(listtmp1[i])/listtmp2[i]) * (10**9))                
    # Store L1-I Cache, L1-D Cache & L2 Cache Miss Rates in the main dictionary            
    for key in dicttemp:
        if key == "Cache Misses0":
            for values in dicttemp[key]:
                for text in values:
                    if (if_float_value(text)) and float(text) != 0:
                        dict1["L1-I Cache Misses"].append(float(text)*40)
        if key == "Cache Misses1":
            for values in dicttemp[key]:
                for text in values:
                    if (if_float_value(text)) and float(text) != 0:
                        dict1["L1-D Cache Misses"].append(float(text)*20)
        if key == "Cache Misses4":
            for values in dicttemp[key]:
                for text in values:
                    if (if_float_value(text)) and float(text) != 0:
                        dict1["L2 Cache Misses"].append(float(text))
    # Calculate the completion time & no. of threads for the benchmark and store it in main dictionary                  
    completion_time = stop_time - start_time
    dict1["completion_time"].append(completion_time)
    for j in range(1, len(dict1["completion_time_threads"])+1):
        dict1["No_of_Threads"].append(j)
    
    i = 0    
    if int(thread_count) > 16:
        while(i < int(thread_count)):
            listtmp3.append(i)
            i = (i * 2) + 1
      
    # generate the dictionary for data frame
    for key in dict1:
        if key=="No_of_Threads" in dict1:
            if int(thread_count) > 16:
                for i in range(0,int(thread_count)):
                    if i in listtmp3:
                        dictdf[key].append(dict1[key][i])
                        dictdf2[key].append(dict1[key][i])
                        dictdf3[key].append(dict1[key][i])
                        dictdf4[key].append(dict1[key][i])
                        dictdf5[key].append(dict1[key][i])
            else:
                dictdf[key]=dict1[key]
                dictdf2[key]=dict1[key]
                dictdf3[key]=dict1[key]
                dictdf4[key]=dict1[key]
                dictdf5[key]=dict1[key]
        if key=="L1-I Cache Misses" in dict1:
            if int(thread_count) > 16:
                for i in range(0,int(thread_count)):
                    if i in listtmp3:
                        dictdf[key].append(dict1[key][i])
            else:
                dictdf[key]=dict1[key]
        if key=="L1-D Cache Misses" in dict1:
            if int(thread_count) > 16:
                for i in range(0,int(thread_count)):
                    if i in listtmp3:
                        dictdf[key].append(dict1[key][i])
            else:
                dictdf[key]=dict1[key]
        if key=="L2 Cache Misses" in dict1:
            if int(thread_count) > 16:
                for i in range(0,int(thread_count)):
                    if i in listtmp3:
                        dictdf[key].append(dict1[key][i])
            else:
                dictdf[key]=dict1[key]
        if key=="Network Latency" in dict1:
            if int(thread_count) > 16:
                for i in range(0,int(thread_count)):
                    if i in listtmp3:
                        dictdf2[key].append(dict1[key][i])
            else:
                dictdf2[key]=dict1[key]
        if key=="Throughput" in dict1:
            if int(thread_count) > 16:
                for i in range(0,int(thread_count)):
                    if i in listtmp3:
                        dictdf3[key].append(dict1[key][i])
            else:
                dictdf3[key]=dict1[key]
        if key=="completion_time_threads" in dict1:
            if int(thread_count) > 16:
                for i in range(0,int(thread_count)):
                    if i in listtmp3:
                        dictdf4["Completion Time"].append(dict1[key][i])
            else:
                dictdf4["Completion Time"]=dict1[key]
        if key=="IPC" in dict1:
            if int(thread_count) > 16:
                for i in range(0,int(thread_count)):
                    if i in listtmp3:
                        dictdf5["CPU Performance"].append(dict1[key][i])
            else:
                dictdf5["CPU Performance"]=dict1[key]

    # Call the function to plot the bar chart for Cache Miss Rates
    draw_cache_miss_chart(dictdf, graph_algorithm, thread_count)
    # Call the function to plot the bar chart for Network Latency
    draw_bar_chart(dictdf2, graph_algorithm, thread_count)
    # Call the function to plot the bar chart for Network Throughput
    draw_bar_chart(dictdf3, graph_algorithm, thread_count)
    # Call the function to plot the bar chart for completion times
    draw_bar_chart(dictdf4, graph_algorithm, thread_count)
    # Call the function to plot the bar chart for completion times
    draw_bar_chart(dictdf5, graph_algorithm, thread_count)

    
    dictfile = dict(dictdf.items() + dictdf2.items() + dictdf3.items() + dictdf4.items() + dictdf5.items()) 
    dictfile[graph_algorithm] = thread_count

    f = open('statistics.txt', 'a')
    f.write(graph_algorithm)
    f.write(thread_count)
    simplejson.dump(dictfile, f)
    f.close()
    
if __name__ == '__main__':
    main()   

import numpy as np
from collections import Counter, defaultdict
import sys
from copy import deepcopy
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

                          
def main():
    dict1 = defaultdict(list)
    dict2 = defaultdict(dict)
    dicttemp =  defaultdict(list)

    with open("output.txt", 'r') as f:
        first_line = f.readline()
        second_line = f.readline()
        third_line = f.readline()
        fourth_line = f.readline()
        fifth_line = f.readline()
    print(fourth_line)
    print(fifth_line)

    words = fourth_line.split()
    print(words)
    for word in words:
        if word.isdigit():
            print(word)
            print(type(word))
            start_time = int(word)
            print(start_time)
            print(type(start_time))
    
    '''
    for word in data:
        print(word)
        if word == "Start":
          #  print(word)
            word += 1
            print(word)
            #word = word.replace("\n", "")
        #dict1[len(word)].append(word)

    for key in dict1:
        for word in dict1[key]:
            dicttemp[word[0:2]].append(word)
            dict2[key][word[0:2]] = dicttemp[word[0:2]]
        dicttemp.clear()
'''

if __name__ == '__main__':
    main()   
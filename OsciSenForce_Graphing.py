# this code will take the data collected from the
# 6 trials (ignorning the first one) and plot the average
# with standard deviation

# libraries
import tkinter as tk
from tkinter import filedialog
import numpy
import matplotlib.pyplot as plt
from drawnow import *
import time
import datetime
import os
import statistics
import xlwt
from xlwt import Workbook

# begin by identifying and opening the text file with collected data
root = tk.Tk();
root.withdraw();
file_path = filedialog.askopenfilename();
f = open(file_path);
data = f.readlines()

# removing "\n" from the end of each string
data2=[]
for i in data:
    data2.append(i.strip())

# separating pressure and timestamp data into individual arrays with
# event separators (*# markers)
ts=[]
pres=[]
counter = 0
while counter < len(data2):
    if '*' not in data2[counter]:
        holder = data2[counter].split(',')
        if len(holder) == 2 and counter > 0:
            ts.append(float(holder[0]))
            pres.append(float(holder[1]))
    elif '*' in data2[counter]:
        ts.append(data2[counter])
        pres.append(data2[counter])
    counter = counter + 1

#### separating events into sublists ####
presmat=[]
tsmat=[]
holder2=[]
holder3=[]
counter2=0
count=0
trigger=0
while counter2<6:
    if (type(pres[count])==int or type(pres[count])==float) and trigger==1:
        holder2.append(pres[count])
        holder3.append(ts[count]) #added ts
    elif (type(pres[count])!=int and type(pres[count])!=float):
        presmat.append(holder2)
        tsmat.append(holder3)
        holder2=[]
        holder3=[]
        counter2=counter2+1
        trigger=1
    else:
        pass
    count=count+1

# create finding smallest number function
def findSmall(nestedList,start,end):
    lengths=[]
    g=start
    while g<=end:
        hold=lengths.append(len(nestedList[g]))
        g=g+1
    small = lengths[0]
    for i in range(1,len(lengths)):
        if (lengths[i] < small):
            small = lengths[i]
    return small, lengths

# average points with same time stamp into singular point
counter1=1
while counter1 < len(tsmat):
    counter2=0
    while counter2 < len(tsmat[counter1])-1:
        num = tsmat[counter1][counter2]
        if num == tsmat[counter1][counter2+1]:
            pr = numpy.array(presmat[counter1])
            t = numpy.array(tsmat[counter1])
            x, = numpy.where(t == num)
            vals = pr[x]
            av = sum(vals)/len(vals)
            pr = list(pr)
            pr[counter2] = av
            t = list(t)
            x = list(x)
            x.pop(0)
            for i in range(0, len(x)):
                pr.pop(counter2+1)
                t.pop(counter2+1)
        counter2 = counter2 + 1
    counter1 = counter1 + 1

# reconstruct main nested list and find smallest one for future use
arrays = [tsmat[1],tsmat[2],tsmat[3],tsmat[4],tsmat[5]]
result = findSmall(arrays,0,4)
small = result[0]

# remove end elements from each sublist untill they are all the same length
counts = 0
lengths = result[1]
for i in range(0,4):
    if lengths[i]>small:
        diff = lengths[i] - small
        presmat[i+1]=presmat[i+1][:-diff]
        tsmat[i+1]=tsmat[i+1][:-diff]

# find average and standard dev across each time point
avpres=[]
stdevarray=[]
counter=0
while counter < small:
    array = [presmat[1][counter],presmat[2][counter],
                     presmat[3][counter],presmat[4][counter],
                      presmat[5][counter]]
    avpres.append(sum(array)/5)
    stdevarray.append(statistics.stdev(array))
    counter = counter + 1

# creates time point vector for pressure values
ms = []
counter = 1
while counter <= small:
    ms.append(counter)
    counter = counter+1

# write data to excel file
directory = file_path[:-4]
wb = Workbook()
sheet1 = wb.add_sheet("Avg and Stdev")
sheet1.write(0, 0, 'Time Stamp (ms)')
sheet1.write(0, 1, 'Average Pressure (psi)')
sheet1.write(0, 2, 'STDEV Pressure (psi)')
counter=0
while counter < small:
    sheet1.write(counter+1,0,ms[counter])
    sheet1.write(counter+1,1,avpres[counter])
    sheet1.write(counter+1,2,stdevarray[counter])
    counter=counter+1
wb.save(directory+".xls")
print(directory)

# graph data
# --> improvement would be to make the error bars more clear
def makeFig(directory,numPoints): #create plot
    plt.title('OsciSenForce Reading Over 5 Trials')
    plt.grid(True)
    plt.ylabel('Average Pressure (psi)')
    plt.xlabel('Time (milliseconds)')
    plt.xlim(0,numPoints)
    plt.ylim(0,1) #previous number was 0,1
    plt.plot(ms,avpres,'ko:',markersize=2,label='Measured Points')
    plt.legend(loc='upper left')
    plt.errorbar(ms, avpres, yerr=stdevarray,ecolor='black')
    plt.savefig(directory+'.png')
    plt.show()
makeFig(directory,small)


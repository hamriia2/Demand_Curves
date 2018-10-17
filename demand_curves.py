# coding: utf-8

# In[53]:

import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
from beautifultable import BeautifulTable
import math


### This section contains the math functions to create different demand curve models ###

### Note : these two functions constitutes 1 model

# Returns the cumulative demand [0..1] for 0 <= T <=1
def BetaCum(A, B, T):
    if T <= 0:
        bc = 0
    elif T >= 1:
        bc = 1
    else:
        # all hail the 5th degree polynomial!
        bc = 10 * T ** 2 * (1 - T) ** 2 * (A + B * T) + T ** 4 * (5 - 4 * T)

    return bc

# Returns the period demand for iPer
def BetaPer(A, B, iPerBeg, iPerEnd, iPer):
    # mix of int and floats not good
    iPerBeg = float(iPerBeg)
    iPerEnd = float(iPerEnd)
    iPer = float(iPer)

    if iPerBeg > iPerEnd:
        bper = -1
    else:
        nPer = iPerEnd - iPerBeg + 1
        bper = BetaCum(A, B, (iPer - iPerBeg + 1) / nPer) - BetaCum(A, B, (iPer - iPerBeg + 0) / nPer)

    return bper

##############################################

#simple sigmoid function
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

#############################################


### this procedure executes a given model and builds the plot    ###########################

# Builds a plot based on A and B values, the demand load, the period start and end numbers and a list of date values
# also including some options for the chart
def BuildPlot(demand, pstart, pend, dlist, model):
    # list to hold X-axis values
    i = []
    # list to hold y-axis values
    i2 = []

    table = BeautifulTable()
    table.column_headers = ["Period", "Demand"]
    runtot = 0

    for x in range(pend+1):
        i.append(dlist[x])

        #here we apply the model

        # this model will make a variety of demand curves, depending on a and b variables set between 0 and 1
        if model == 'FL':
            distload = BetaPer(1, 0, pstart, pend, x) * demand
        elif model == 'BL':
            distload = BetaPer(0, 0, pstart, pend, x) * demand
        elif model == 'Bell':
            distload = BetaPer(0.25, 0.5, pstart, pend, x) * demand
        # this model will apply a sigmoid curve
        elif model == 'Sigmoid':
            distload = 1 + sigmoid(x)
        elif model == 'Linear':
            distload = demand / (pend + 1)
        else:
            distload = demand / (pend + 1)

        i2.append(distload)
        table.append_row([x, distload])
        runtot += distload

    table.append_row(['Total', runtot])

    #show the results in a nice table
    print(table)

    # plot using matplotlib
    plt.plot(i, i2)

    plt.xlabel('Date')
    plt.ylabel('Working days')
    plt.title('Demand curve with model ' + model)
    plt.grid(True)
    plt.savefig("test.png")

    plt.show()

###### MAIN PROGRAM  ###############################

# create 12 datetime variables, first of month
dates = pd.date_range('2018-01-01', '2019-01-01', freq='1M') - pd.offsets.MonthBegin(1)
dates1 = [dt.datetime.strptime(str(d), '%Y-%m-%d %X').date() for d in dates]

# set a total demand load eg. 20 working days
demand = 20

# call the plot with given date range, demand and demand curve profile
BuildPlot(demand, 0, 11, dates1, 'Linear')
BuildPlot(demand, 0, 11, dates1, 'Bell')
BuildPlot(demand, 0, 11, dates1, 'FL')
BuildPlot(demand, 0, 11, dates1, 'BL')
BuildPlot(demand, 0, 11, dates1, 'Sigmoid')

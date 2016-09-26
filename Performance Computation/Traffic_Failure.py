
import csv
import sys
import re

row = 0 #The desired row to fetch from the CSV
column = 7 #The desired column to feth from the CSV
step = 1 #Used to either increment the column or the row
headers = []

def readCSV():
    try:
        spirentData = open('mlacp_switchover.csv')
        readData = csv.reader(spirentData)
    except:
        sys.exit("file not found!!!")

    return readData


def getHeader(row, column):
    data = readCSV()
    computed_Data = list(data)
    header = computed_Data[row][column]
    return header

def get_Dropped_Count():
    data = readCSV()
    values = []
    for row in data:
        dropped_count = row[column]
        values.append(dropped_count)
    return values


def get_Tx_Rate():
    data = readCSV()
    values = []
    for row in data:
        tx_rate = row[column + step]
        values.append(tx_rate)
    return values


def calculate_Loss():
    loss = []
    for drop_counter in range(0, get_Dropped_Count().__len__()):
        if drop_counter == 0:
            header = getHeader(row, column)
            second_header = getHeader(row, column + step)
            headers.append(header)
            headers.append(second_header)
            drop_counter += 1
        else:

            drop_value = float("".join(get_Dropped_Count()[drop_counter].split(",")))
            rate_value = float("".join(get_Tx_Rate()[drop_counter].split(",")))
            total_loss = drop_value / rate_value
            loss.append(total_loss)
    return loss



def outage():
    maximum_Outage = raw_input("Please enter the maximum outage: ")
    stream_selection = raw_input("do you want to see passed or failed streams: ")
    passed_Streams = []
    failed_Streams = []

    for loss_values in calculate_Loss():
        if loss_values <= int(maximum_Outage):
            passed_Streams.append(loss_values)
        elif loss_values > int(maximum_Outage):
                failed_Streams.append(loss_values)
    if stream_selection == 'passed':
        for passed in passed_Streams:
            print "%.3f" % passed
    else:
        for failed in failed_Streams:
            print "%.3f" % failed




def main():

    outage()


main()

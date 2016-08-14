import csv
import sys
import re




def readCSV():
    spirentData = open('mlacp_switchover.csv')
    readData = csv.reader(spirentData)
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
        dropped_count = row[7]
        values.append(dropped_count)
    return values


def get_Tx_Rate():
    data = readCSV()
    values = []
    for row in data:
        tx_rate = row[8]
        values.append(tx_rate)
    return values


def calculate_Loss(dropped_count, tx_rate):

        #maximum_Outage = raw_input("Please enter the maximum outage")
        passed_Streams = []
        counter = 0
        total_number_of_drops = dropped_count.__len__()
        total_number_of_tx_rate = tx_rate.__len__()
        for row in range(counter, total_number_of_drops):
            print dropped_count[row]
            counter += 1

        #if value <= maximum_Outage:
            #passed_Streams.append(value)





def main():
    row = 0
    column = 7
    getHeader(row, column)
    dropped_count = get_Dropped_Count()
    tx_rate = get_Tx_Rate()
    calculate_Loss(dropped_count, tx_rate)

main()


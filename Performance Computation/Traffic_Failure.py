import csv
import sys
import re

row = 0 #The desired row to fetch from the CSV
column = 7 #The desired column to feth from the CSV
step = 1 #Used to either increment the column or the row

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


def calculate_Loss(dropped_count, tx_rate):

        #maximum_Outage = raw_input("Please enter the maximum outage")
        passed_Streams = []
        drop_value = 0
        rate_value = 0
        drop_counter = 0
        tx_counter = 0
        total_number_of_drops = dropped_count.__len__()
        total_number_of_tx_rate = tx_rate.__len__()
        for rown in range(drop_counter, total_number_of_drops - 1):
            if drop_counter == 0:
                header = getHeader(row, column)
                #print header
            drop_counter += 1
            drop_value = float(dropped_count[drop_counter])

        for rowne in range(tx_counter, total_number_of_tx_rate - 1):
            if tx_counter == 0:
                header = getHeader(row, column + step)
                #print header
            tx_counter += 1
            rate_value = float(tx_rate[tx_counter])
        total_loss = rate_value/drop_value
        print total_loss
        #if value <= maximum_Outage:
            #passed_Streams.append(value)





def main():

    dropped_count = get_Dropped_Count()
    tx_rate = get_Tx_Rate()
    calculate_Loss(dropped_count, tx_rate)

main()



import csv
import sys
import re

row = 0 #The desired row to fetch from the CSV
column = 5 #The desired column to feth from the CSV
step = 3 #Used to either increment the column or the row
headers = []

def readCSV():
    try:
        spirentData = open('mlacp switchover.csv')
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

        #maximum_Outage = raw_input("Please enter the maximum outage")
        passed_Streams = []


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
                print "%.3f" % total_loss


'''''''''




        #if value <= maximum_Outage:
            #passed_Streams.append(value)

'''''''''



def main():

    calculate_Loss()

main()




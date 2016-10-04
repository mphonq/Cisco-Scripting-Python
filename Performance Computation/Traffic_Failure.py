import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple
import re

headers = []  # Contains whatever header you so choose to insert


def readCSV():
    try:
        spirentData = open('mlacpswitchover.csv')
        readData = list(csv.reader(spirentData))
    except:
        sys.exit("file not found!!!")

    return readData


def get_Dropped_Column():
    data = readCSV()
    headers = data[0]
    index = 0
    for s in headers:
        if s == "Dropped Count (Frames)":
            index = data[0].index(str(s))

    return index


def get_FPS_Column():
    data = readCSV()
    headers = data[0]
    index = 0
    for s in headers:
        if s == "Frames per Second (fps)":
            index = data[0].index(str(s))
    return index


def getHeader(row, column):
    data = readCSV()
    computed_Data = list(data)
    header = computed_Data[row][column]
    return header


def get_Dropped_Count(column):
    data = readCSV()
    values = []
    for row in data:
        dropped_count = row[column]
        values.append(dropped_count)
        headers.append(row[0])
    return values


def get_Tx_Rate(column):
    data = readCSV()
    values = []
    for row in data:
        tx_rate = row[column]
        values.append(tx_rate)
    return values


def calculate_Loss(drop_column, rate_column):
    loss = []
    for drop_counter in range(0, get_Dropped_Count(drop_column).__len__()):
        if drop_counter == 0:
            drop_counter += 1
        else:
            drop_value = float("".join(get_Dropped_Count(drop_column)[drop_counter].split(",")))
            rate_value = float("".join(get_Tx_Rate(rate_column)[drop_counter].split(",")))
            total_loss = drop_value / rate_value
            loss.append(total_loss)
    return loss


def outage(dropped_column, rate_column):
    maximum_Outage = raw_input("Please enter the maximum outage in seconds: ")
    stream_selection = raw_input("do you want to see passed or failed streams: ")
    passed_Streams = []
    failed_Streams = []
    passed_Headers = []
    failed_headers = []
    header_counter = 0
    for loss_values in calculate_Loss(dropped_column, rate_column):
        header_counter += 1
        if loss_values <= int(maximum_Outage):
            passed_Streams.append(loss_values)
            passed_Headers.append(headers[header_counter])
        elif loss_values > int(maximum_Outage):
            failed_Streams.append(loss_values)
            failed_headers.append(headers[header_counter])

    if stream_selection == 'passed':
        pass_counter = 0
        for passed in passed_Streams:
            print passed_Headers[pass_counter] + " %.3f " % passed
            pass_counter += 1

    elif stream_selection == 'failed':
        fail_counter = 0
        for failed in failed_Streams:
            print failed_headers[fail_counter] + " %.3f" % failed
            fail_counter += 1
    else:
        sys.exit("Sorry but your input is not recognised, please enter passed or failed")


def main():
    dropped_column = get_Dropped_Column()
    rate_column = get_FPS_Column()
    outage(dropped_column, rate_column)


main()

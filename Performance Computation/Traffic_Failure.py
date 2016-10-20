import sys
import csv

def main():
    if(len(sys.argv) != 2):
        sys.exit("Please enter a filename")

    filename = sys.argv[1]

    with open(filename) as f:
        rows = csv.reader(f)
        headers = rows.next()
        indexes = {
            "name": headers.index("StreamBlock Name"),
            "drop": headers.index("Dropped Count (Frames)"),
            "rate": headers.index("Frames per Second (fps)")
        }
        columns = {key:list() for key in indexes}
        for row in rows:
            if any(row):
                columns["name"].append(row[indexes["name"]])
                columns["drop"].append(float(row[indexes["drop"]].replace(",","")))
                columns["rate"].append(float(row[indexes["rate"]].replace(",","")))
    
    columns["loss"] = [drop/rate for drop, rate in zip(columns["drop"], columns["rate"])]
    max_outage = float(raw_input("Please enter the maximum outage in seconds: "))
    stream_selection = raw_input("Do you want to see passed or failed streams: ")
    if stream_selection == "passed":
        for index, loss in enumerate(columns["loss"]):
            if loss <= max_outage:
                print columns["name"][index], " %.3f " % loss
    elif stream_selection == "failed":
        for index, loss in enumerate(columns["loss"]):
            if loss > max_outage:
                print columns["name"][index], " %.3f " % loss
    else:
        sys.exit("Your input is not recognised, please enter 'passed' or 'failed' without quotes")

main()

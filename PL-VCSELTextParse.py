from os import listdir
import csv
from datetime import datetime


def get_temp(data):
    f = open(path + data, 'r')
    while True:
        text = f.readline()
        if 'Temperature' in text:
            measdata.append(text[-7:-3])
            f.close()
            break


def get_datetime(data):
    f = open(path + data, 'r')
    while True:
        text = f.readline()
        if 'Date' in text:
            d = datetime.strptime(text[-28:-2], '%B %d, %Y %H:%M:%S')
            newd = d.strftime('%Y-%m-%d %H:%M:%S')
            measdata.append(newd)
            f.close()
            break


def get_SBcenter(data):
    f = open(path + data, 'r')
    while True:
        text = f.readline()
        if 'Average' in text:
            measdata.append(text[18:23])
            f.close()
            break


def get_FPdip(data):
    f = open(path + data, 'r')
    while True:
        text = f.readline()
        if 'Average' in text:
            measdata.append(text[32:37])
            f.close()
            break


def get_SBwidth(data):
    f = open(path + data, 'r')
    while True:
        text = f.readline()
        if 'Average' in text:
            measdata.append(text[46:51])
            f.close()
            break


def get_SBdelta(data):
    f = open(path + data, 'r')
    while True:
        text = f.readline()
        if 'Average' in text:
            measdata.append(text[60:65])
            f.close()
            break


path = "./VCSEL_Text_Files/"
datafiles = listdir(path)
current_time = datetime.now().strftime('%Y%m%d%H%M%S')
data_file = "VCSELData_" + current_time + ".csv"

Headers = ["FileName",
           "Measurement DateTime",
           "Temperature (degC)",
           "SB Center (nm)",
           "F-P Dip (nm)",
           "SB Width (nm)",
           "SB Delta (nm)"
           ]

g = open(data_file, 'a', newline='')
gwriter = csv.writer(g)
gwriter.writerow(Headers)

for i in datafiles:
    measdata = [i]
    get_datetime(i)
    get_temp(i)
    get_SBcenter(i)
    get_FPdip(i)
    get_SBwidth(i)
    get_SBdelta(i)
    gwriter.writerow(measdata)

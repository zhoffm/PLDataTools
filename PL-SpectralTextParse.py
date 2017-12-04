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


def get_pklambda(data):
    f = open(path + data, 'r')
    while True:
        text = f.readline()
        if 'Average' in text:
            measdata.append(text[18:23])
            f.close()
            break


def get_pkintensity(data):
    f = open(path + data, 'r')
    while True:
        text = f.readline()
        if 'Average' in text:
            measdata.append(text[30:35])
            f.close()
            break


def get_intsignal(data):
    f = open(path + data, 'r')
    while True:
        text = f.readline()
        if 'Average' in text:
            measdata.append(text[44:49])
            f.close()
            break


def get_FWHM(data):
    f = open(path + data, 'r')
    while True:
        text = f.readline()
        if 'Average' in text:
            measdata.append(text[61:65])
            f.close()
            break


path = "./Spectral_Text_Files/"
datafiles = listdir(path)
current_time = datetime.now().strftime('%Y%m%d%H%M%S')
data_file = "SpectralData_" + current_time + ".csv"

Headers = ["FileName",
           "Measurement DateTime",
           "Temperature (degC)",
           "AvgPeakWavelength (nm)",
           "AvgPeakIntensity (V)",
           "IntegratedSignal (a.u.)",
           "FWHM (nm)"]

g = open(data_file, 'a', newline='')
gwriter = csv.writer(g)
gwriter.writerow(Headers)

for i in datafiles:
    measdata = [i]
    get_datetime(i)
    get_temp(i)
    get_pklambda(i)
    get_pkintensity(i)
    get_intsignal(i)
    get_FWHM(i)
    gwriter.writerow(measdata)

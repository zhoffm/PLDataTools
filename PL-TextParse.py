from os import listdir
import csv
from datetime import datetime


def get_temp(path, data):
    f = open(path + data, 'r')
    while True:
        text = f.readline()
        if 'Temperature' in text:
            measdata.append(text[-7:-3])
            f.close()
            break


def get_datetime(path, data):
    f = open(path + data, 'r')
    while True:
        text = f.readline()
        if 'Date' in text:
            d = datetime.strptime(text[13:], '%B %d, %Y %H:%M:%S ')
            newd = d.strftime('%Y-%m-%d %H:%M:%S')
            measdata.append(newd)
            f.close()
            break


def get_vcsel_data(data):
    f = open(VCSEL_path + data, 'r')
    while True:
        text = f.readline()
        if 'Average' in text:
            measdata.append(text[18:23])
            measdata.append(text[32:37])
            measdata.append(text[46:51])
            measdata.append(text[60:65])
            f.close()
            break


def get_spectral_data(data):
    f = open(spectral_path + data, 'r')
    while True:
        text = f.readline()
        if 'Average' in text:
            measdata.append(text[18:23])
            measdata.append(text[30:35])
            measdata.append(text[44:49])
            measdata.append(text[61:65])
            f.close()
            break


while True:
    print('\nWelcome to PL-TextParse!\n')
    print('1. Spectral\n2. VCSEL\n3. Exit')
    x = input('Please input your measurement type: ')

    if x == '1' or x == 'spectral' or x == 'Spectral':
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        spectral_path = "./SPECTRAL_PR03/"
        spectral_datafiles = listdir(spectral_path)
        spectral_data = "SpectralData_" + current_time + ".csv"
        spectral_headers = ["FileName",
                            "Measurement DateTime",
                            "Temperature (degC)",
                            "AvgPeakWavelength (nm)",
                            "AvgPeakIntensity (V)",
                            "IntegratedSignal (a.u.)",
                            "FWHM (nm)"]

        with open(spectral_data, 'a', newline='') as g:
            gwriter = csv.writer(g)
            gwriter.writerow(spectral_headers)
            for i in spectral_datafiles:
                measdata = [i]
                get_datetime(spectral_path, i)
                get_temp(spectral_path, i)
                get_spectral_data(i)
                gwriter.writerow(measdata)
        print('\nParsing complete. Returning to menu...\n')
    elif x == '2' or x == 'VCSEL' or x == 'vcsel':
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        VCSEL_path = "./VCSEL_Text_Files/"
        VCSEL_datafiles = listdir(VCSEL_path)
        VCSEL_data = "VCSELData_" + current_time + ".csv"
        VCSEL_headers = ["FileName",
                         "Measurement DateTime",
                         "Temperature (degC)",
                         "SB Center (nm)",
                         "F-P Dip (nm)",
                         "SB Width (nm)",
                         "SB Delta (nm)"
                         ]

        with open(VCSEL_data, 'a', newline='') as h:
            hwriter = csv.writer(h)
            hwriter.writerow(VCSEL_headers)
            for i in VCSEL_datafiles:
                measdata = [i]
                get_datetime(VCSEL_path, i)
                get_temp(VCSEL_path, i)
                get_vcsel_data(i)
                hwriter.writerow(measdata)
        print('\nParsing complete. Returning to menu...\n')
    elif x == '3':
        print('Exiting...')
        break
    else:
        print('\nIncorrect choice. Please try again.\1n')
        pass

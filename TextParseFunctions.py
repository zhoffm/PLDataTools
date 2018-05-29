from os import listdir
import csv
from datetime import datetime


class Measurement:

    @staticmethod
    def check_meas_type(path):
        dir_list = listdir(path)
        if '_spm' in dir_list[0]:
            return 'Spectral'
        elif '_vsm' in dir_list[0]:
            return 'VCSEL'
        else:
            raise ValueError('Measurement Type is not VCSEL or Spectral. Are you in the right directory?')

    @staticmethod
    def get_temp(path, raw_data):
        f = open(path + raw_data, 'r')
        while True:
            text = f.readline()
            if 'Temperature' in text:
                temp = text[-7:-3]
                f.close()
                return temp

    @staticmethod
    def get_datetime(path, raw_data):
        f = open(path + raw_data, 'r')
        while True:
            text = f.readline()
            if 'Date' in text:
                d = datetime.strptime(text[13:], '%B %d, %Y %H:%M:%S ')
                newd = d.strftime('%Y-%m-%d %H:%M:%S')
                f.close()
                return newd

    @staticmethod
    def get_current_datetime():
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        return current_time

    @staticmethod
    def write_parsed_data(meas_type):
        with open("./output_data/" + meas_type.output_filename, 'a', newline='') as h:
            hwriter = csv.writer(h)
            hwriter.writerow(meas_type.headers)
            for file in meas_type.datafiles:
                measdata = [
                    file,
                    meas_type.get_datetime(meas_type.path, file),
                    meas_type.get_temp(meas_type.path, file)
                ] + meas_type.get_data(file)
                hwriter.writerow(measdata)


class VCSEL(Measurement):
    def __init__(self, path):
        self.path = path
        self.output_filename = "VCSELData_" + self.get_current_datetime() + ".csv"
        self.datafiles = listdir(self.path)
        self.headers = ["FileName",
                        "Measurement DateTime",
                        "Temperature (degC)",
                        "SB Center (nm)",
                        "F-P Dip (nm)",
                        "SB Width (nm)",
                        "SB Delta (nm)"
                        ]

    def get_data(self, raw_data):
        f = open(self.path + raw_data, 'r')
        while True:
            text = f.readline()
            if 'Average' in text:
                sb_center = text[17:23]
                fp_dip = text[31:37]
                sb_width = text[46:51]
                sb_delta = text[60:65]
                f.close()
                return [sb_center, fp_dip, sb_width, sb_delta]


class Spectral(Measurement):

    def __init__(self, path):
        self.path = path
        self.output_filename = "SpectralData_" + self.get_current_datetime() + ".csv"
        self.datafiles = listdir(self.path)
        self.headers = ["FileName",
                        "Measurement DateTime",
                        "Temperature (degC)",
                        "AvgPeakWavelength (nm)",
                        "AvgPeakIntensity (V)",
                        "IntegratedSignal (a.u.)",
                        "FWHM (nm)"]

    def get_data(self, raw_data):
        f = open(self.path + raw_data, 'r')
        while True:
            text = f.readline()
            if 'Average' in text:
                avg_peak_wavelength = text[17:23]
                avg_peak_intensity = text[30:35]
                integrated_signal = text[44:49]
                fwhm = text[61:65]
                f.close()
                return [avg_peak_wavelength, avg_peak_intensity, integrated_signal, fwhm]


if __name__ == '__main__':
    while True:
        print('\nWelcome to PL-TextParse Test!\n')
        print('1. Spectral\n2. VCSEL\n3. Exit')
        x = input('Please input your measurement type: ')

        if x == '1':
            spectral_datafile_path = input("Please input your data folder name: ")
            spectral = Spectral(spectral_datafile_path + "/")
            print(spectral.check_meas_type(spectral_datafile_path + "/"))

            spectral.write_parsed_data(spectral)
            print('\nTest complete. Returning to menu...\n')
        elif x == '2':
            VCSEL_datafile_path = input("Please input your data folder name: ")
            VCSEL = VCSEL(VCSEL_datafile_path + "/")
            print(VCSEL.check_meas_type(VCSEL_datafile_path + '/'))

            VCSEL.write_parsed_data(VCSEL)
            print('\nTest complete. Returning to menu...\n')
        elif x == '3':
            print('Exiting...')
            break
        else:
            print('\nIncorrect choice. Please try again.\n')
            pass

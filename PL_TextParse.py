# work on static methods so they don't need to be called so frequently.
# working on looping while list is under a certain length.

from os import listdir
import csv
from datetime import datetime


# this is inspired by https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float?rq=1
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class Measurement:

    scan_params = ['Wafer size', 'Scan diameter', 'Resolution', 'Scan rate', 'Temperature']
    wave_params = ['Center', 'Range', 'Slit width', 'Grating', 'Detector', 'Filter', 'Gain', 'Calibration']
    laser_params = ['Name', 'Wavelength', 'Power']

    @staticmethod
    def get_current_datetime():
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        return current_time

    @staticmethod
    def check_meas_type(path):
        dir_list = listdir(path)
        if '_spm' in dir_list[0]:
            return 'Spectral'
        elif '_vsm' in dir_list[0]:
            return 'VCSEL'
        else:
            raise Exception('Measurement Type is not VCSEL or Spectral. Are you in the right directory?')

    @staticmethod
    def get_recipe_name(path, raw_data):
        with open(path + raw_data, 'r') as f:
            for count, line in enumerate(f):
                if 'Recipe' in line:
                    parsed_text = [i.strip() for i in line.split()]
                    recipe = parsed_text[2]
                    return recipe

    @staticmethod
    def get_datetime(path, raw_data):
        with open(path + raw_data, 'r') as f:
            for count, line in enumerate(f):
                if 'Date' in line:
                    parsed_text = [i.strip() for i in line.split()]
                    raw_date = ' '.join(parsed_text[-4:])
                    d = datetime.strptime(raw_date, '%B %d, %Y %H:%M:%S')
                    newd = d.strftime('%Y-%m-%d %H:%M:%S')
                    return newd

    @staticmethod
    def get_parameters(param_list, path, raw_data):
        params = []
        for param in param_list:
            with open(path + raw_data, 'r') as f:
                for count, line in enumerate(f):
                    if param in line:
                        parsed_text = [i.strip() for i in line.split()]
                        for item in parsed_text:
                            # if item == 'to' or item == ':' or ':' in item:
                            if item == 'to' or ':' in item:
                                semi_index = parsed_text.index(item)
                                params.append(parsed_text[semi_index + 1])
        return params

# Need to readjust this method to accomodate all of the extra data being added to the output
    @staticmethod
    def write_parsed_data(meas_type):
        with open(meas_type.output_filename, 'a', newline='') as h:
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
                        "Recipe",
                        "Measurement DateTime",
                        "Wafer Size (mm)",
                        "Scan Diameter (mm)",
                        "Resolution (mm)",
                        "Scan Rate",
                        "Temperature (degC)",
                        "Center Wavelength (nm)",
                        "Wavelength Range (nm)",
                        "Slit Width (mm)",
                        "Grating (g/mm)",
                        "Detector",
                        "Filter",
                        "Gain",
                        "Calibration",
                        "SB Center (nm)",
                        "F-P Dip (nm)",
                        "SB Width (nm)",
                        "SB Delta (nm)"
                        ]

    def get_data(self, raw_data):
        with open(self.path + raw_data, 'r') as f:
            for count, line in enumerate(f):
                if 'Average' in line:
                    parsed_text = [i.strip() for i in line.split()]
                    return [parsed_text[2], parsed_text[4], parsed_text[6], parsed_text[8]]


class Spectral(Measurement):

    def __init__(self, path):
        self.path = path
        self.output_filename = "SpectralData_" + self.get_current_datetime() + ".csv"
        self.datafiles = listdir(self.path)
        self.headers = ["FileName",
                        "Recipe",
                        "Measurement DateTime",
                        "Wafer Size (mm)",
                        "Scan Diameter (mm)",
                        "Resolution (mm)",
                        "Scan Rate",
                        "Temperature (degC)",
                        "Center Wavelength (nm)",
                        "Wavelength Range (nm)",
                        "Slit Width (mm)",
                        "Grating (g/mm)",
                        "Detector",
                        "Filter",
                        "Gain",
                        "Calibration",
                        "Laser Name",
                        "Laser Wavelength (nm)",
                        "Laser Power (mW)",
                        "AvgPeakWavelength (nm)",
                        "AvgPeakIntensity (V)",
                        "IntegratedSignal (a.u.)",
                        "FWHM (nm)"]

    def get_data(self, raw_data):
        with open(self.path + raw_data, 'r') as f:
            for count, line in enumerate(f):
                if 'Average' in line:
                    parsed_text = [i.strip() for i in line.split()]
                    return [parsed_text[2], parsed_text[4], parsed_text[6], parsed_text[8]]

# ##Archived Methods##
# def get_scan_parameters(path, raw_data):
#     scan_params = []
#     for param in ['Wafer size', 'Scan diameter', 'Resolution', 'Scan rate', 'Temperature']:
#         with open(path + raw_data, 'r') as f:
#             for count, line in enumerate(f):
#                 if param in line:
#                     parsed_text = [i.strip() for i in line.split()]
#                     semi_index = parsed_text.index(':')
#                     scan_params.append(parsed_text[semi_index + 1])
#     return scan_params
#
# def get_wavelength_parameters(path, raw_data):
#     wave_params = []
#     for param in ['Center', 'Range', 'Slit width', 'Grating', 'Detector', 'Filter', 'Gain', 'Calibration']:
#         with open(path + raw_data, 'r') as f:
#             for count, line in enumerate(f):
#                 if param in line:
#                     parsed_text = [i.strip() for i in line.split()]
#                     for item in parsed_text:
#                         if item == 'to' or item == ':':
#                             semi_index = parsed_text.index(item)
#                             wave_params.append(parsed_text[semi_index + 1])
#     return wave_params
#
# def get_laser_parameters(path, raw_data):
#     laser_params = []
#     for param in ['Name', 'Wavelength', 'Power']:
#         with open(path + raw_data, 'r') as f:
#             for count, line in enumerate(f):
#                 if param in line:
#                     parsed_text = [i.strip() for i in line.split()]
#                     for item in parsed_text:
#                         if ':' in item:
#                             semi_index = parsed_text.index(item)
#                             laser_params.append(parsed_text[semi_index + 1])
#     return laser_params


if __name__ == '__main__':
    v_meas = VCSEL('./VCSEL_TestData/')
    s_meas = Spectral('./Spectral_TestData/')

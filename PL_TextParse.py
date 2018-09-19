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

    def __init__(self):
        self.output_path = './output_data/'

    @staticmethod
    def get_current_datetime():
        current_time = datetime.now().strftime('%Y%m%d%H%M%S')
        return current_time

    @staticmethod
    def check_meas_type(path):
        dir_list = listdir(path)
        try:
            with open(path + dir_list[0], 'r') as f:
                for count, line in enumerate(f):
                    if 'PL Spectral' in line:
                        return 'Spectral'
                    elif 'VCSEL/DBR' in line:
                        return 'VCSEL'
        except PermissionError:
            pass

    @staticmethod
    def check_tool_type(path, raw_data):
        with open(path + raw_data, 'r') as f:
            for count, line in enumerate(f):
                if 'ACCENT' in line:
                    return '2000'
                elif 'Nanometrics' in line:
                    return 'blue'

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


class VCSEL(Measurement):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.output_filename = "VCSELData_" + self.get_current_datetime() + ".csv"
        self.datafiles = listdir(self.path)
        self.output_headers = ["FileName",
                               "Recipe",
                               "Measurement DateTime",
                               "Wafer Size (mm)",
                               "Scan Diameter (mm)",
                               "Resolution (mm)",
                               "Scan Rate",
                               "Temperature (degC)",
                               "Center Wavelength (nm)",
                               "Wavelength Range - Low (nm)",
                               "Wavelength Range - High (nm)",
                               "Slit Width (mm)",
                               "Grating (g/mm)",
                               "Detector",
                               "Filter",
                               "Gain",
                               "Calibration",
                               "SB Center (nm)",
                               "F-P Dip (nm)",
                               "SB Width (nm)",
                               "SB Height (V)"
                               ]
        self.requested_data_headers = ['SB Center', 'F-P Dip', 'SB Width', 'SB Height']
        self.parsed_text = []
        self.parsed_headers = []

    def get_data(self, raw_data):
        requested_data = []
        with open(self.path + raw_data, 'r') as f:
            for count, line in enumerate(f):
                if 'STATISTICS:' in line:
                    self.parsed_headers = [i.strip() for i in next(f).split('  ')]
                    self.parsed_headers = list(filter(None, self.parsed_headers))
                if 'Average' in line:
                    self.parsed_text = [i.strip() for i in line.split()]
                    self.parsed_text = [
                        float(x) for x in self.parsed_text if x.replace('.', '', 1).replace('-', '', 1).isdigit()
                    ]
            parsed_data_dict = dict(zip(self.parsed_headers, self.parsed_text))
            # print(parsed_data_dict)
            for x in self.requested_data_headers:
                try:
                    requested_data.append(parsed_data_dict[x])
                except KeyError:
                    requested_data.append('')
            # print(requested_data)
            return requested_data

    def write_parsed_data(self):
        with open(self.output_path + self.output_filename, 'a', newline='') as h:
            hwriter = csv.writer(h)
            hwriter.writerow(self.output_headers)
            for file in self.datafiles:
                measdata = [
                               file,
                               self.get_recipe_name(self.path, file),
                               self.get_datetime(self.path, file)
                           ] \
                           + self.get_parameters(self.scan_params, self.path, file) \
                           + self.get_parameters(self.wave_params, self.path, file) \
                           + self.get_data(file)
                hwriter.writerow(measdata)


class Spectral(Measurement):

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.output_filename = "SpectralData_" + self.get_current_datetime() + ".csv"
        self.datafiles = listdir(self.path)
        self.output_headers = ["FileName",
                               "Recipe",
                               "Measurement DateTime",
                               "Wafer Size (mm)",
                               "Scan Diameter (mm)",
                               "Resolution (mm)",
                               "Scan Rate",
                               "Temperature (degC)",
                               "Center Wavelength (nm)",
                               "Wavelength Range - Low (nm)",
                               "Wavelength Range - High (nm)",
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
        self.requested_data_headers = ['Peak Lambda', 'Peak Int', 'Int. Signal', 'FWHM']
        self.parsed_text = []
        self.parsed_headers = []

    def get_data(self, raw_data):
        requested_data = []
        with open(self.path + raw_data, 'r') as f:
            for count, line in enumerate(f):
                if 'STATISTICS:' in line:
                    self.parsed_headers = [i.strip() for i in next(f).split('  ')]
                    self.parsed_headers = list(filter(None, self.parsed_headers))
                if 'Average' in line:
                    self.parsed_text = [i.strip() for i in line.split()]
                    self.parsed_text = [
                        float(x) for x in self.parsed_text if x.replace('.', '', 1).replace('-', '', 1).isdigit()
                    ]
            parsed_data_dict = dict(zip(self.parsed_headers, self.parsed_text))
            # print(parsed_data_dict)
            for x in self.requested_data_headers:
                try:
                    requested_data.append(parsed_data_dict[x])
                except KeyError:
                    requested_data.append('')
            # print(requested_data)
            return requested_data

    def write_parsed_data(self):
        with open(self.output_path + self.output_filename, 'a', newline='') as h:
            hwriter = csv.writer(h)
            hwriter.writerow(self.output_headers)
            for file in self.datafiles:
                measdata = [
                               file,
                               self.get_recipe_name(self.path, file),
                               self.get_datetime(self.path, file)
                           ] \
                           + self.get_parameters(self.scan_params, self.path, file) \
                           + self.get_parameters(self.wave_params, self.path, file) \
                           + self.get_parameters(self.laser_params, self.path, file) \
                           + self.get_data(file)
                hwriter.writerow(measdata)


# ##Archived Methods##
# @staticmethod
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
# @staticmethod
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
# @staticmethod
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
    pass

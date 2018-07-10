from unittest import TestCase
from PL_TextParse import *


spm_path = './Spectral_TestData/'
test_spm_file = 'GA07-812B_03_spm.txt'
spm = Spectral(spm_path)

vsm_path = './VCSEL_TestData/'
test_vsm_file = 'GA07-1719C_05_vsm.txt'
vsm = VCSEL(vsm_path)


class TestMeasurement(TestCase):
    def test_check_meas_type(self):
        self.assertEqual(
            Measurement.check_meas_type(spm_path),
            'Spectral'
        )
        self.assertEqual(
            Measurement.check_meas_type(vsm_path),
            'VCSEL'
        )

    def test_get_recipe_name(self):
        self.assertEqual(
            Measurement.get_recipe_name(vsm_path, test_vsm_file),
            'reflectance_6inch_940_PR03.rcf'
        )

    def test_get_datetime(self):
        self.assertEqual(
            Measurement.get_datetime(vsm_path, test_vsm_file),
            '2017-11-30 17:20:49'
        )

    def test_get_parameters(self):
        self.assertEqual(
            Measurement.get_parameters(Measurement.scan_params, vsm_path, test_vsm_file),
            ['150.0', '148.0', '2.0', '40', '29.0']
        )
        self.assertEqual(
            Measurement.get_parameters(Measurement.wave_params, vsm_path, test_vsm_file),
            ['938.8', '811.2', '1067.4', '0.120', '300g/mm-760', 'CCD1024TE', 'None', 'x1', 'G300-CCD.cal']
        )
        self.assertEqual(
            Measurement.get_parameters(Measurement.laser_params, spm_path, test_spm_file),
            ['OBIS532', '532.0', '0.999']
        )

    def test_get_scan_parameters(self):
        self.assertEqual(
            Measurement.get_scan_parameters(vsm_path, test_vsm_file),
            ['150.0', '148.0', '2.0', '40', '29.0']
        )

    def test_get_wavelength_parameters(self):
        self.assertEqual(
            Measurement.get_wavelength_parameters(vsm_path, test_vsm_file),
            ['938.8', '811.2', '1067.4', '0.120', '300g/mm-760', 'CCD1024TE', 'None', 'x1', 'G300-CCD.cal']
        )

    def test_get_laser_parameters(self):
        self.assertEqual(
            Measurement.get_laser_parameters(spm_path, test_spm_file),
            ['OBIS532', '532.0', '0.999']
        )

    def test_get_current_datetime(self):
        self.assertEqual(
            Measurement.get_current_datetime(),
            datetime.now().strftime('%Y%m%d%H%M%S')
        )

    # need to think about how to implement this one
    # def test_write_parsed_data(self):
    #     self.fail()


class TestVCSEL(TestCase):
    def test_get_data(self):
        self.assertEqual(
            vsm.get_data(test_vsm_file),
            ['892.4', '879.8', '104.3', '-12.5']
        )


class TestSpectral(TestCase):
    def test_get_data(self):
        self.assertEqual(
            spm.get_data(test_spm_file),
            ['923.5', '0.916', '30.13', '26.7']
        )


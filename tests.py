from unittest import TestCase
from PL_TextParse import *


spm_path = ''
test_spm_file = ''
spm = Spectral(spm_path)

vsm_path = ''
test_vsm_file = ''
vsm = VCSEL(vsm_path)

tool_test_path = ''
rpm2000_test_file = ''
rpmBlue_test_file = ''


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

    def test_check_tool_type(self):
        self.assertEqual(
            Measurement.check_tool_type(tool_test_path, rpm2000_test_file),
            '2000'
        )
        self.assertEqual(
            Measurement.check_tool_type(tool_test_path, rpmBlue_test_file),
            'blue'
        )

    def test_get_recipe_name(self):
        self.assertEqual(
            Measurement.get_recipe_name(vsm_path, test_vsm_file),
            ''
        )
        self.assertEqual(
            Measurement.get_recipe_name(spm_path, test_spm_file),
            ''
        )

    def test_get_datetime(self):
        self.assertEqual(
            Measurement.get_datetime(vsm_path, test_vsm_file),
            '2017-11-30 17:20:49'
        )
        self.assertEqual(
            Measurement.get_datetime(spm_path, test_spm_file),
            '2017-11-28 11:31:58'
        )

    def test_get_parameters(self):
        self.assertEqual(
            Measurement.get_parameters(Measurement.scan_params, vsm_path, test_vsm_file),
            []
        )
        self.assertEqual(
            Measurement.get_parameters(Measurement.wave_params, vsm_path, test_vsm_file),
            []
        )
        self.assertEqual(
            Measurement.get_parameters(Measurement.scan_params, spm_path, test_spm_file),
            []
        )
        self.assertEqual(
            Measurement.get_parameters(Measurement.wave_params, spm_path, test_spm_file),
            []
        )
        self.assertEqual(
            Measurement.get_parameters(Measurement.laser_params, spm_path, test_spm_file),
            []
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
            []
        )


class TestSpectral(TestCase):
    def test_get_data(self):
        self.assertEqual(
            spm.get_data(test_spm_file),
            []
        )


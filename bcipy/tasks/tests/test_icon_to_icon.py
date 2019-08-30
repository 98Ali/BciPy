import unittest
import os
import shutil

from mock import mock_open, patch
from mockito import mock

from bcipy.display.display_main import init_display_window
from bcipy.helpers.load import load_json_parameters
from bcipy.tasks.rsvp.icon_to_icon import RSVPIconToIconTask
from bcipy.helpers.save import init_save_data_structure


class TestIconToIcon(unittest.TestCase):
    """Tests for Icon to Icon class"""

    def setUp(self):
        """set up the needed path for load functions."""
        params_path = 'bcipy/parameters/parameters.json'
        self.parameters = load_json_parameters(params_path, value_cast=True)
        parameters = self.parameters
        parameters['window_height'] = 1
        parameters['window_width'] = 1
        parameters['is_txt_stim'] = False
        img_path = 'bcipy/static/images/rsvp_images/'
        parameters['path_to_presentation_images'] = img_path

        self.data_save_path = 'data/'
        self.user_information = 'test_user_003'

        self.save = init_save_data_structure(
            self.data_save_path,
            self.user_information,
            params_path)

        # TODO: can this be mocked?
        self.display = init_display_window(parameters)
        daq = mock()
        signal_model = None
        language_model = None
        fake = True
        auc_filename = ""

        with patch('bcipy.tasks.rsvp.icon_to_icon.open', mock_open()):
            self.task = RSVPIconToIconTask(self.display, daq, parameters, self.save,
                                           signal_model, language_model, fake,
                                           False, auc_filename)

    def tearDown(self):
        self.display.close()
        shutil.rmtree(self.data_save_path + self.user_information)

    def test_img_path(self):
        """Test img_path method"""
        fixation = 'bcipy/static/images/bci_main_images/PLUS.png'
        self.assertTrue(len(self.task.alp) > 0)
        self.assertTrue('PLUS' not in self.task.alp)

        self.assertEqual('bcipy/static/images/rsvp_images/A.png',
                         self.task.img_path('A'))
        self.assertEqual('A.png', self.task.img_path('A.png'))
        self.assertEqual(fixation, self.task.img_path(fixation))

    def test_init_session_data(self):
        self.task.init_session_data()
        self.assertEqual(os.path.exists(self.save), 1)

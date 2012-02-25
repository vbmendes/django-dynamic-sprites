# coding: utf8

import os
import subprocess
import sys
import unittest

class CliClientTestCase(unittest.TestCase):

    def setUp(self):
        self.ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.TMP_DIR = os.path.join(self.ROOT_DIR, '.tmp')
        if not os.path.exists(self.TMP_DIR):
            os.mkdir(self.TMP_DIR)
        self.script_path = os.path.join(self.ROOT_DIR, 'scripts', 'generate_sprite.py')
        self.input_path = os.path.join(self.ROOT_DIR, 'tests', 'media', 'cli_images')
        self.output_path = os.path.join(self.TMP_DIR, 'output-sprite')
        self.output_png = '%s.png' % self.output_path
        self.output_css = '%s.css' % self.output_path
        
        self.old_python_path = sys.path.append(self.ROOT_DIR)

    def tearDown(self):
        os.remove(self.output_png)
        os.remove(self.output_css)
        os.rmdir(self.TMP_DIR)

    def test_command_generates_the_output_image(self):
        subprocess.call([self.script_path, self.input_path, self.output_path])
        self.assertTrue(os.path.isfile(self.output_png))

    def test_command_generates_the_output_style(self):
        subprocess.call([self.script_path, self.input_path, self.output_path])
        self.assertTrue(os.path.isfile(self.output_png))
    



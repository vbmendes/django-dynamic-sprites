# coding: utf8

import cssutils
import os
import subprocess
import sys
import unittest


class ScriptTestCase(unittest.TestCase):

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
        os.environ['PYTHONPATH'] = self.ROOT_DIR + ':' + os.environ.get('PYTHONPATH', '')

    def tearDown(self):
        os.remove(self.output_png)
        os.remove(self.output_css)
        os.rmdir(self.TMP_DIR)

    def assertOutputCss(self, *selector_positions):
        self.assertTrue(os.path.isfile(self.output_css))
        parsed_css = cssutils.parseFile(self.output_css)
        self.assertEquals(4, len(parsed_css.cssRules))
        image_rule = parsed_css.cssRules[0]
        self.assertEquals('.sprite-output-sprite', image_rule.selectorText)
        self.assertEquals('url(%s)' % self.output_png, image_rule.style.background)
        i = 1
        for selector, position in selector_positions:
            rule = parsed_css.cssRules[i]
            self.assertEquals(selector, rule.selectorText)
            self.assertEquals(position, rule.style.backgroundPosition)
            i += 1

    def test_command_generates_the_output_image(self):
        subprocess.call([self.script_path, self.input_path, self.output_path])
        self.assertTrue(os.path.isfile(self.output_png))

    def test_command_generates_the_output_style(self):
        subprocess.call([self.script_path, self.input_path, self.output_path])
        self.assertOutputCss(
            ('.sprite-output-sprite-bandeira-do-brasil', '0 0'),
            ('.sprite-output-sprite-can', '-48px 0'),
            ('.sprite-output-sprite-usa', '-96px 0'),
        )

    def test_command_accepts_the_vertical_packing_parameter(self):
        subprocess.call([self.script_path, '-p vertical', self.input_path, self.output_path])
        self.assertOutputCss(
            ('.sprite-output-sprite-bandeira-do-brasil', '0 0'),
            ('.sprite-output-sprite-can', '0 -48px'),
            ('.sprite-output-sprite-usa', '0 -96px'),
        )

    def test_command_accepts_the_bin_packing_parameter(self):
        subprocess.call([self.script_path, '--packing=bin', self.input_path, self.output_path])
        self.assertOutputCss(
            ('.sprite-output-sprite-bandeira-do-brasil', '0 0'),
            ('.sprite-output-sprite-can', '-48px 0'),
            ('.sprite-output-sprite-usa', '0 -48px'),
        )

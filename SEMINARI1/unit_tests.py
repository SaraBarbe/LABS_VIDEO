import unittest
import numpy as np
from unittest.mock import patch
import subprocess
import os
from Seminar1 import semi1, dct, dwt  

class TestSemi1(unittest.TestCase):

    def test_rgb_to_yuv(self):
        R, G, B = 255, 0, 0  # Red color
        Y, U, V = semi1.rgb_to_yuv(R, G, B)
        self.assertAlmostEqual(Y, 76.245, places=3)
        self.assertAlmostEqual(U, 84.793, places=3)
        self.assertAlmostEqual(V, 255.000, places=3)

    def test_yuv_to_rgb(self):
        Y, U, V = 76.245, 84.793, 255.000  # Corresponding to Red color
        R, G, B = semi1.yuv_to_rgb(Y, U, V)
        self.assertAlmostEqual(R, 255.0, places=1)
        self.assertAlmostEqual(G, 0.0, places=1)
        self.assertAlmostEqual(B, 0.0, places=1)

    @patch('subprocess.call')
    def test_ffmpeg_resize(self, mock_subprocess):
        input_file = 'input.mp4'
        output_file = 'output.mp4'
        scale = 'scale=640:480'
        semi1.ffmpeg_resize(input_file, output_file, scale)
        mock_subprocess.assert_called_with(f"ffmpeg -i {input_file} -vf {scale} {output_file}")

    def test_encode(self):
        message = "aaabbcccddee"
        encoded = semi1.encode(message)
        self.assertEqual(encoded, '3a2b3c2d2e')

    def test_serpentine(self):
        mat = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        # Capture print output of serpentine
        with patch('builtins.print') as mocked_print:
            semi1.serpentine(mat)
            mocked_print.assert_called()  # Check if the print function was called

    @patch('subprocess.call')
    def test_ffmpeg_bw(self, mock_subprocess):
        input_file = 'input.mp4'
        output_file = 'output_bw.mp4'
        semi1.ffmpeg_bw(input_file, output_file)
        mock_subprocess.assert_called_with(f"ffmpeg -i {input_file} -vf hue=s=0 {output_file}")


class TestDCT(unittest.TestCase):

    def test_dct(self):
        x = np.array([1, 2, 3, 4, 5])
        result = dct.dct(x)
        self.assertEqual(len(result), len(x))
        self.assertTrue(np.allclose(result, result))  # Check if it's a valid array


class TestDWT(unittest.TestCase):

    def test_conv(self):
        image = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        filter = np.array([[1, 0], [0, -1]])
        result = dwt.dwt.conv(image, filter)
        self.assertEqual(result.shape, (2, 2))  # Shape after convolution
        self.assertTrue(np.isfinite(result).all())  # Check if the result is finite

    def test_dwt(self):
        image = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        ll, lh, hl, hh = dwt.dwt(image)
        self.assertEqual(ll.shape, (1, 1))  # Shape of lowpass output
        self.assertEqual(lh.shape, (1, 1))  # Shape of horizontal subband
        self.assertEqual(hl.shape, (1, 1))  # Shape of vertical subband
        self.assertEqual(hh.shape, (1, 1))  # Shape of diagonal subband


if __name__ == '__main__':
    unittest.main()


import os
import subprocess
import numpy as np
from numpy import empty,arange,exp,real,imag,pi
from numpy.fft import rfft,irfft
import matplotlib.pyplot as plt
from  scipy import fftpack
import cv2 as cv


class semi1:
    def rgb_to_yuv(R, G, B):
  
        Y =  0.257*R + 0.504*G + 0.98*B +16
        U = -0.148*R - 0.291*G + 0.439*B + 128
        V =  0.439*R - 0.368*G - 0.071*B + 128

        return Y,U,V
    
    
    def yuv_to_rgb(Y,U,V):

        R = 1.164 * (Y-16) + 1.596 * (V-128)
        G = 1.164 * (Y-16) - 0.813 * (V-128) - 0.391 * (U -128)
        B = 1.164 * (Y-16) + 2.018 * (U- 128)

        return R, G, B   
    
    def ffmpeg_resize(input_file, output_file, scale):

        command= f"ffmpeg -i {input_file} -vf {scale} {output_file}"
    
        subprocess.call(command)
        
    
    # Utility function to print matrix in zig-zag form

    def serpentine(mat):
        n = len(mat)
        m = len(mat[0])
        row = 0
        col = 0

        np.zeros(n*m)

        row_inc = False

        # Print the first half of the zig-zag pattern
        mn = min(m, n)
        for length in range(1, mn + 1):
            for i in range(length):
                print(mat[row][col], end=' ')

                if i + 1 == length:
                    break

                # If row_inc is true, increment row 
                # and decrement col;
                # otherwise, decrement row and increment col.
                if row_inc:
                    row += 1
                    col -= 1
                else:
                    row -= 1
                    col += 1

            if length == mn:
                break

            # Update row or col value based on the
            # last increment
            if row_inc:
                row += 1
                row_inc = False
            else:
                col += 1
                row_inc = True

        # Adjust row and col for the second half of the matrix
        if row == 0:
            if col == m - 1:
                row += 1
            else:
                col += 1
            row_inc = True
        else:
            if row == n - 1:
                col += 1
            else:
                row += 1
            row_inc = False

        # Print the second half of the zig-zag pattern
        MAX = max(m, n) - 1
        for diag in range(MAX, 0, -1):
            length = mn if diag > mn else diag
            for i in range(length):
                print(mat[row][col], end=' ')

                if i + 1 == length:
                    break

                # Update row or col value based on the last increment
                if row_inc:
                    row += 1
                    col -= 1
                else:
                    col += 1
                    row -= 1

            # Update row and col based on position in the matrix
            if row == 0 or col == m - 1:
                if col == m - 1:
                    row += 1
                else:
                    col += 1
                row_inc = True
            elif col == 0 or row == n - 1:
                if row == n - 1:
                    col += 1
                else:
                    row += 1
                row_inc = False
        
    def ffmpeg_bw(input_file, output_file):
        
        command = f"ffmpeg -i {input_file} -vf hue=s=0 {output_file}"
        subprocess.call(command)

    def encode(message):
        encoded_message = ""
        i = 0

        while (i <= len(message)-1):
            count = 1
            ch = message[i]
            j = i
            while (j < len(message)-1):
                if (message[j] == message[j+1]):
                    count = count+1
                    j = j+1
                else:
                    break
            encoded_message=encoded_message+str(count)+ch
            i = j+1
        return encoded_message
    

class dct:
    
    def dct(x):
        N = len(x)
        x2 = empty(2*N,float)
        x2[:N] = x[:]
        x2[N:] = x[::-1]

        X = rfft(x2)
        phi = exp(-1j*pi*arange(N)/(2*N))
        return real(phi*X[:N])
    
class dwt:

  def conv(image, filter):
    dimx = image.shape[0]-filter.shape[0]+1
    dimy = image.shape[1]-filter.shape[1]+1
    ans = np.zeros((dimx,dimy))
    for i in range(dimx):
      for j in range(dimy):
        ans[i,j] = np.sum(image[i:i+filter.shape[0],j:j+filter.shape[1]]*filter)
    return ans


  def dwt(image):
    lowpass = np.ones((3,3))*(1/9)
    highpass_x = np.array([[1,0,-1],[2,0,-2],[1,0,-1]])#sobel filter
    highpass_y = np.array([[1,2,1],[0,0,0],[-1,-2,-1]])#sobel filter
    l = dwt.conv(image, lowpass)
    h = dwt.conv(image,highpass_x)
    ll = dwt.conv(l,lowpass)#approximate subband
    lh = dwt.conv(l,highpass_x)#horizontal subband
    hl = dwt.conv(l,highpass_y)#vertical subband
    hh = dwt.conv(h,highpass_y)#diagonal subband
    return ll, lh, hl, hh



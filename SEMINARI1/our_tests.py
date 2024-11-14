import Seminar1
from scipy import fftpack
import cv2 as cv
import matplotlib.pyplot as plt



#RGB TO YUV AND YUV TO RGB
print("rgb to yuv:", Seminar1.semi1.rgb_to_yuv(50, 0, 0))
print("yuv to rgb:", Seminar1.semi1.yuv_to_rgb(28.85, 120.6, 149.95))

print("yuv to rgb:", Seminar1.semi1.yuv_to_rgb(128, 150, 200))
print("rgb to yuv:", Seminar1.semi1.rgb_to_yuv(245.28, 63.22999999999999, 174.76399999999998))

#RESIZE USING FFMPEG

Seminar1.semi1.ffmpeg_resize("nudibranqui.jpg", "nudibranqui_R1.jpg", "scale=320:240")
Seminar1.semi1.ffmpeg_resize("nudibranqui.jpg", "nudibranqui_R2.jpg", "scale=160:120")


#SERPENTINE

mat = [
    [ 1,  2,  6,  7, 15, 16, 28, 29],
    [ 3,  5,  8, 14, 17, 27, 30, 43],
    [ 4,  9, 13, 18, 26, 31, 42, 44],
    [10, 12, 19, 25, 32, 41, 45, 54],
    [11, 20, 24, 33, 40, 46, 53, 55],
    [21, 23, 34, 39, 47, 52, 56, 63],
    [22, 35, 38, 48, 51, 57, 62, 64],
    [36, 37, 49, 50, 58, 61, 65, 66]
]

Seminar1.semi1.serpentine(mat)


#BLACK AND WHITE USING FFMPEG
Seminar1.semi1.ffmpeg_bw("nudibranqui.jpg", "nudibranqui_blw.jpg")

#RUN-LENGHT ENCODING

encoded_message = "000001101111000"
print("\n run-lenght:", Seminar1.semi1.encode(encoded_message))

#DCT

x = [72, 70, 65, 65, 66, 68, 72, 75, 80, 84, 84, 89]

print("Nostra funció:", Seminar1.dct.dct(x))

print("LLibreria:",fftpack.dct(x))


#DWT
image = cv.imread('nudibranqui.jpg', cv.IMREAD_GRAYSCALE)
ll0, lh0, hl0 ,hh0 = Seminar1.dwt.dwt(image)

plt.figure(figsize=(5,4))
plt.subplot(2,2,1), plt.imshow(ll0, cmap='gray')
plt.subplot(2,2,2), plt.imshow(lh0, cmap='gray')
plt.subplot(2,2,3), plt.imshow(hl0, cmap='gray')
plt.subplot(2,2,4), plt.imshow(hh0, cmap='gray')
from typing import Union

from fastapi import FastAPI, File, UploadFile
import subprocess
from tempfile import TemporaryDirectory
import os
from fastapi.responses import FileResponse


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/rgb_to_yuv/{R}/{G}/{B}")
def rgb_to_yuv(R: int, G: int, B: int):
    Y = 0.257 * R + 0.504 * G + 0.098 * B + 16
    U = -0.148 * R - 0.291 * G + 0.439 * B + 128
    V = 0.439 * R - 0.368 * G - 0.071 * B + 128
    return {"Y": Y, "U": U, "V": V}


@app.post("/ffmpeg_resize/{scale_x}/{scale_y}")
async def ffmpeg_resize(scale_x:int, scale_y:int, input_file: UploadFile):
    in_name = os.path.join("uploads/", input_file.filename)
    f = open(in_name, "wb")
    f.write(input_file.file.read())
    f.flush()
    command = f"ffmpeg -i uploads/{input_file.filename} -vf scale={scale_x}:{scale_y} uploads/resized.jpg"
    subprocess.run(command, shell=True)
    return FileResponse("uploads/resized.jpg")


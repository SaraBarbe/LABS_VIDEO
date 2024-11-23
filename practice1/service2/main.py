from typing import Union

from fastapi import FastAPI, File, UploadFile
import subprocess
from tempfile import TemporaryDirectory
import os
from fastapi.responses import FileResponse


app = FastAPI()


@app.post("/ffmpeg_bw/")
async def ffmpeg_bw(input_file: UploadFile):
    in_name = os.path.join("uploads/", input_file.filename)
    f = open(in_name, "wb")
    f.write(input_file.file.read())
    f.flush()
    command = f"ffmpeg -i uploads/{input_file.filename} -vf hue=s=0 uploads/bw.jpg"
    subprocess.run(command, shell=True)
    return FileResponse("uploads/bw.jpg")
from typing import Union

from fastapi import FastAPI, UploadFile
import subprocess
import os
from fastapi.responses import FileResponse


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/ffmpeg_resize_v/{scale_x}/{scale_y}")
async def ffmpeg_resize_v(scale_x:int, scale_y:int, input_file: UploadFile):
    in_name = os.path.join("uploads/", input_file.filename)
    f = open(in_name, "wb")
    f.write(input_file.file.read())
    f.flush()
    command = f"ffmpeg -y -i uploads/{input_file.filename} -vf scale={scale_x}:{scale_y} uploads/resized.mp4"
    subprocess.run(command, shell=True)
    return FileResponse("uploads/resized.mp4", media_type="video/mp4", filename="resized.mp4")


@app.post("/ffmpeg_chroma")
async def ffmpeg_chroma(input_file: UploadFile):
    in_name = os.path.join("uploads/", input_file.filename)
    f = open(in_name, "wb")
    f.write(input_file.file.read())
    f.flush()
    command = f"ffmpeg -i uploads/{input_file.filename} -pix_fmt yuv420p uploads/chroma.mp4"
    subprocess.run(command, shell=True)
    return FileResponse("uploads/chroma.mp4", media_type="video/mp4", filename="chroma.mp4")


@app.post("/ffmpeg_i")
async def ffmpeg_i(input_file: UploadFile):
    in_name = os.path.join("uploads/", input_file.filename)
    f = open(in_name, "wb")
    f.write(input_file.file.read())
    f.flush()
    command = f"ffprobe -v error -select_streams v -show_entries stream=codec_name,bit_rate,duration,width,height -of default=noprint_wrappers=1 uploads/{input_file.filename}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    stdout_lines = result.stdout.splitlines()

    for line in stdout_lines:
        print(line)

    return {"Info": stdout_lines}


@app.post("/ffmpeg_audio")
async def ffmpeg_audio(input_file: UploadFile):
    in_name = os.path.join("uploads/", input_file.filename)
    f = open(in_name, "wb")
    f.write(input_file.file.read())
    f.flush()
    no_aduio = f"ffmpeg -ss 00:00:00 -to 00:00:20 -i uploads/{input_file.filename} -c copy -an uploads/cut_noaudio.mp4"
    aac = f"ffmpeg -ss 00:00:00 -to 00:00:20 -i uploads/{input_file.filename} -vn -acodec aac -ac 1 uploads/audio_aac.aac"
    mp3 = f"ffmpeg -ss 00:00:00 -to 00:00:20 -i uploads/{input_file.filename} -ac 2 -b:a 64k uploads/audio_mp3.mp3"
    ac3 = f"ffmpeg -ss 00:00:00 -to 00:00:20 -i uploads/{input_file.filename} -c:a ac3 uploads/audio_ac3.ac3"

    subprocess.run(no_aduio, shell=True, capture_output=True, text=True)
    subprocess.run(aac, shell=True, capture_output=True, text=True)
    subprocess.run(mp3, shell=True, capture_output=True, text=True)
    subprocess.run(ac3, shell=True, capture_output=True, text=True)

    #package
    command_final = "ffmpeg -i uploads/cut_noaudio.mp4 -i uploads/audio_aac.aac -i uploads/audio_mp3.mp3 -i uploads/audio_ac3.ac3 -map 0 -map 1 -map 2 -map 3 -codec copy uploads/output.mp4"
    subprocess.run(command_final, shell=True, capture_output=True, text=True)
    return FileResponse("uploads/output.mp4", media_type="video/mp4", filename="output.mp4")

@app.post("/ffmpeg_tracks")
async def ffmpeg_tracks(input_file: UploadFile):
    in_name = os.path.join("uploads/", input_file.filename)
    f = open(in_name, "wb")
    f.write(input_file.file.read())
    f.flush()
    command = f"ffprobe -v error -show_entries stream=codec_type -of default=nw=1:nk=1 uploads/{input_file.filename} | uniq -c"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    return {"channels": result.stdout.splitlines()}

@app.post("/ffmpeg_motion")
async def ffmpeg_motion(input_file: UploadFile):
    in_name = os.path.join("uploads/", input_file.filename)
    f = open(in_name, "wb")
    f.write(input_file.file.read())
    f.flush()
    vectors = f"ffmpeg -flags2 +export_mvs -i uploads/{input_file.filename} -vf codecview=mv=pf+bf+bb uploads/motion_vector.mp4"
    subprocess.run(vectors, shell=True, capture_output=True, text=True)
    return FileResponse("uploads/motion_vector.mp4", media_type="motion_vector/mp4", filename="motion_vector.mp4")

@app.post("/ffmpeg_histogram")
async def ffmpeg_histogram(input_file: UploadFile):
    in_name = os.path.join("uploads/", input_file.filename)
    f = open(in_name, "wb")
    f.write(input_file.file.read())
    f.flush()
    command = f"ffmpeg -y -report -i uploads/{input_file.filename} -vf \"split=2[a][b]; [b]histogram,format=yuva444p[hh]; [a][hh]overlay=W-w-10:H-h-10\" -c:v libx264 -crf 22 -preset veryslow uploads/histogram.mp4"
    subprocess.run(command, shell=True, capture_output=True, text=True)
    return FileResponse("uploads/histogram.mp4", media_type="histogram/mp4", filename="histogram.mp4")


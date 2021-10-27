import shutil
import magic
import os
from typing import MutableSequence
from fastapi import FastAPI, File, UploadFile
from core import AudioAnalyzer
app = FastAPI()
audioAnalyzer = AudioAnalyzer()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/file")
async def create_file(file_name):
    res = "do something function"
    return {"Facial Expression": 1, "Geatures": 2, "Miss Spell Words": ["meowww", "mangosss", "tata", ], "Loudness": 3, "Frequently used Words": ["apple", "cute", "team", "project"], "Gramatical Errors": 50}


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    with open(f'{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    mime = magic.Magic(mime=True)
    filename = file.filename
    validation = mime.from_file(f'./{filename}')
    if validation.find('video') != -1:

        return {"filename": filename}
    else:
        os.remove(f'./{filename}')
        return {"Not a valid file format!"}


# 1. get and post request
# 2. post accept data from byte stream now apply validation formats of video + size limit of 25 MBs
#     Store data (locally)
# 3. Json (of etc etc)

import shutil
import magic
import os
from typing import MutableSequence
from fastapi import FastAPI, File, UploadFile
from core import AudioAnalyzer
app = FastAPI()
audioAnalyzer = AudioAnalyzer()

response = {"Facial Expression": 1, "Gestures": 2, "Miss Spell Words": [
    "meowww", "mangosss", "tata", ], "Loudness": 3, "Frequently used Words": ["apple", "cute", "team", "project"], "Gramatical Errors": 50}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/file")
async def create_file(file_name):
    res = "do something function"
    return response


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    with open(f'{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    mime = magic.Magic(mime=True)
    filename = file.filename
    validation = mime.from_file(f'./{filename}')
    if validation.find('video') != -1:
        audioAnalyzer = AudioAnalyzer(filename)
        response["Facial Expression"] = 1
        response["Gestures", 2]
        response["Miss Spell Words"] = audioAnalyzer.misspelled_words()
        if audioAnalyzer.loudness() > 70:
            response["Loudness"] = 3
        elif audioAnalyzer.loudness() > 50:
            response["Loudness"] = 2
        else:
            response["Loudness"] = 1
        # response["Loudness"] = audioAnalyzer.loudness()
        response["Frequently used Words"] = audioAnalyzer.most_common_words()
        response["Gramatical Errors"] = audioAnalyzer.check_grammer()
        return {"filename": filename}
    else:
        os.remove(f'./{filename}')
        return {"Not a valid file format!"}


# 1. get and post request
# 2. post accept data from byte stream now apply validation formats of video + size limit of 25 MBs
#     Store data (locally)
# 3. Json (of etc etc)

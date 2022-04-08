import base64
from io import BytesIO
from fastapi import FastAPI
from Model.model import predict
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from urllib.request import urlretrieve
from PIL import Image
import torch
from DataBase.DataFetch import fetch


class image_base64(BaseModel):
    img_base64: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def basetoimage(base):
    try:
        im_bytes = base64.b64decode(base)  # im_bytes is a binary image
        im_file = BytesIO(im_bytes)  # convert image to file-like object
        img = Image.open(im_file)
        return img, 1
    except:
        return None, 0

@app.post("/")
async def read_image(file: image_base64):
    #download model file
    if os.path.exists('Model/snake_jit.pt') == False:
        url = 'https://onedrive.live.com/download?cid=470A5A8DB59AAEA1&resid=470A5A8DB59AAEA1%2115989&authkey=AJ3CFbpMUgJXe04'
        filename = 'Model/snake_jit.pt'
        urlretrieve(url, filename)
    model = torch.jit.load("Model/snake_jit.pt")

    base64 = file.img_base64
    image, flag = basetoimage(base64)
    result = {"Result": "1"}
    if flag == 1:
        idx = predict(model, image)
        result.update(fetch(idx))
    else:
        result = {"Result": "Please Provide Correct Input"}

    return result
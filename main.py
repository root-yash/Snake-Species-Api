import base64
from io import BytesIO
from fastapi import FastAPI, UploadFile, File
from Model.model import predict
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import torch


class image_base64(BaseModel):
    img_base64: str
    img_file: UploadFile = File(...)

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
async def read_image(image: UploadFile = File(...)):
    # #download model file
    # if os.path.exists('Model/model_398_trace.pt') == False:
    #     url = 'https://onedrive.live.com/download?cid=470A5A8DB59AAEA1&resid=470A5A8DB59AAEA1%2114267&authkey=AMbqal_UGof27TE'
    #     filename = 'Model/model_398_trace.pt'
    #     urlretrieve(url, filename)
    model = torch.jit.load("Model/snake_jit.pt")
    flag = 0
    base64 = "string"

    if image!=None:
        image = image.file
        image = Image.open(image)
        flag = 1

    if base64 != "string":
        image, flag = basetoimage(base64)

    if flag == 1:
        result = predict(model, image)
    else:
        result = {"Result": "Please Provide Correct Input"}

    return result
from typing import List
import face_rec as frc
import numpy as np
import cv2
from starlette.responses import FileResponse

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse


app = FastAPI()

@cfd.get("/impro")
def impro():
    return ''


# @app.post("/files/")
# async def create_files(files: List[bytes] = File(...)):
#     return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}



@app.post("/files/")
async def create_file(

    file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)

):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }



# @app.post("/impro")
# async def upload_image(file: UploadFile=File(...)):
#     contents = await file.read()
#     nparr = np.fromstring(contents, np.uint8)
#     img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#     matched_image = frc.classify_face(img)
#     #print("hii")
#     img = cv2.imread('matched_image.png')
#     # return frc.classify_face(img)
#     return FileResponse("matched_image.png", media_type='application/octet-stream',filename="matched_image.png")

@app.post("/impro")
async def predict_api(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    image = read_imagefile(await file.read())
    prediction = frc.classify_face(image)

    return prediction



@app.get("/")
async def main():
    content = """
<body>

<form action="/impro" enctype="multipart/form-data" method="post">
<input name="files" type="file" >
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
from internal import metadata_extractor, hash

app = FastAPI()

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    print(f"File {file.filename} received.")
    try:
        contents = file.file.read()
        filename = file.filename
        with open(filename, "wb") as buffer:
            buffer.write(contents)
        metadata = metadata_extractor.extract_metadata(file.filename)
        perceptual_hash = hash.compute_perceptual_hash(file.filename)
        file.file.close()
        return {"metadata": metadata, "perceptual_hash": perceptual_hash}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
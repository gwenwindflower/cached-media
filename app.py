from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from boto3 import client

app = FastAPI()
s3 = client("s3")

@app.get("/download/{filename}")
async def root(filename: str):
    try:
        filename = filename + ".zip"
        response = s3.get_object(Bucket="cached-media", Key=filename)
        file_content = response['Body'].read()
        with open(filename, 'wb') as file:
            file.write(file_content)

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Cached Media Store</title>
        </head>
        <body>
            <h1>{filename}</h1>
            <p>Thank you for downloading {filename}</p>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)

    except Exception:
        raise HTTPException(status_code=404, detail="File not found")

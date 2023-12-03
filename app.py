from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from boto3 import client

app = FastAPI()
s3 = client("s3", region_name="us-east-2")

@app.get("/download/{filename}")
async def root(filename: str):
    try:
        filename = filename + ".zip"
        response = s3.get_object(Bucket="cached-media", Key=filename)
        file_content = response['Body'].read()

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
        return HTMLResponse(content=html_content), file_content

    except Exception:
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Cached Media Store</title>
        </head>
        <body>
            <h1>{filename}</h1>
            <p>File {filename} not found</p>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)
        raise HTTPException(status_code=404, detail="File not found")

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from boto3 import client
from botocore.exceptions import NoCredentialsError
import urllib.parse

app = FastAPI()
s3 = client("s3", region_name="us-east-2")

@app.get("/download/{filename}")
def generate_presigned_url(filename: str):
    filename = filename + ".zip"
    safe_filename = urllib.parse.quote_plus(filename)
    content_disposition = f'attachment; filename="{safe_filename}"'

    try:
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': 'cached-media',
                    'Key': filename,
                    'ResponseContentDisposition': content_disposition},
            ExpiresIn=600
        )
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Cached Media Store</title>
        </head>
        <body>
            <h1>{filename}</h1>
            <a href={presigned_url} download="{filename}">Click here to download {filename}</a>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=200)
    except NoCredentialsError:
        return {"error": "Credentials not available"}

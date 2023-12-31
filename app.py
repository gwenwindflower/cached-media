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
    bucket_name = "cached-media"

    try:
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name,
                    'Key': filename,
                    'ResponseContentDisposition': content_disposition},
            ExpiresIn=600
        )
        
        html_content = f"""
        <!DOCTYPE html>
        <style>
            body {{
                background-color: #efefef;
                font-size: 2rem;
                color: #333;
                font-family: sans-serif;
                padding: 1rem;
            }}
            a {{
                color: #333;
                font-family: monospace;
                text-decoration: none;
                box-shadow: inset 0 -0.7rem 0 0 rgba(0, 120, 100, 0.5);
                color: inherit;
                transition: 0.2s;
            }}
            a:hover {{
                box-shadow: inset 0 -1.5rem 0 0 rgba(0, 120, 100, 0.5);
                transition: 0.2s;
            }}
        </style>
        <html>
        <head>
            <title>Cached Media Store | {filename}</title>
        </head>
        <body>
            <h1>Thanks for your support!</h1>
            <a href={presigned_url} download="{filename}">Click here to download {filename}</a>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=200)
    except NoCredentialsError:
        return {"error": "Credentials not available"}

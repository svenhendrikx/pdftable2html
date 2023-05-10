from fastapi import FastAPI, UploadFile, File, Form
from starlette.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import uvicorn

import os
import base64
import camelot as cam

app = FastAPI()

@app.post("/convert")
async def convert(file: UploadFile = File(...), pages: str = Form(...)):

    """
    This endpoint accepts a PDF file and a string representing pages to be converted into HTML tables.

    For each table found in the PDF, it is converted to an HTML table and stored as a file. The contents of each HTML file 
    are then read into a list of HTML tables.

    The endpoint returns a list of HTML responses, each containing one HTML table.

    Args:
        file (UploadFile): The PDF file to be processed.
        pages (str): A string representing the pages to be converted into HTML tables.

    Returns:
        List[HTMLResponse]: A list of HTML responses, each containing an HTML table.
    """

    with open("input.pdf","wb") as f:
        contents = await file.read()
        base64_pdf = base64.b64encode(contents).decode('utf-8')
        f.write(base64.b64decode(base64_pdf))

    tables = cam.read_pdf("input.pdf", pages = pages, flavor = 'stream')
    
    html_tables = []
    for i in range(tables.n):
        filename = '/tmp/table_{}.html'
        tables[i].to_html(filename)

        with open(filename, 'r') as f:
            html_tables.append(f.read())

    responses = [HTMLResponse(content=t) for t in html_tables]

    return responses

app.mount('', StaticFiles(directory="front/public/", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

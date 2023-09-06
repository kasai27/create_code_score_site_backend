from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

app = FastAPI()

origins = {
    "http://localhost:3000",
}

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers= ["*"],
)


@app.post("/generate_pdf/")
async def generate_pdf(title: str = Form(...), name: str = Form(...), originalKey: str = Form(...), capo: str = Form(...), playKey: str = Form(...), lyric: str = Form(...)):
    pdf_filename = "generated_pdf.pdf"

    # フォントの設定
    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

    # x, yの間隔とスタート位置の設定
    x_index = 10*mm
    y_index = 15*mm
    x = 10*mm
    y = A4[1] - 15*mm 

    # canvs, fontの設定
    c = canvas.Canvas(pdf_filename, pagesize=A4)
    c.setFont("HeiseiMin-W3", 20)

    # １行目（title, artist, key)
    c.drawString(x, y, title)
    x += x_index + c.stringWidth(title)
    c.drawString(x, y, name)
    x += x_index + c.stringWidth(name)
    c.drawString(x, y, originalKey) 

    # ２行目（capo, play_key)
    x = 10*mm
    y -= y_index
    c.drawString(x, y, capo)
    x += x_index + c.stringWidth(capo)
    c.drawString(x, y, playKey)
    x += x_index + c.stringWidth(playKey)
    c.drawString(x, y, lyric)
    c.save()

    return FileResponse(pdf_filename, headers={"Content-Disposition": "inline; filename=generate_pdf.pdf"})
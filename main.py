from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from janome.tokenizer import Tokenizer
from my_library import mor_ana

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

    # ３行目以降（lyric)
    c.setFont("HeiseiMin-W3", 12)
    x = 10*mm
    y -= y_index + 10*mm
    max_length = 40
    lyric_split = mor_ana.split_sentence_by_particles(lyric)
    lyric_split = mor_ana.join_elements_with_limit(lyric_split, max_length)

    t = Tokenizer()
    for line in range(len(lyric_split)):
        lyric_split[line] = list(t.tokenize(lyric_split[line], wakati=True))
        lyric_split[line] = mor_ana.code_join(lyric_split[line])
        for lyric_item in lyric_split[line]:
            if lyric_item.startswith("[") and lyric_item.endswith("]"):
                lyric_item = lyric_item.replace('[','')
                lyric_item = lyric_item.replace(']','')
                c.drawString(x, y+5*mm, lyric_item)
            else:
                c.drawString(x, y, lyric_item)
                x += c.stringWidth(lyric_item, "HeiseiMin-W3", 12)
        x = 10*mm
        y -= y_index

        # 次のページ
        if y <= 0:
            c.showPage()
            c.setFont("HeiseiMin-W3", 12)
            y = A4[1] - 15*mm

    c.save()

    return FileResponse(pdf_filename, headers={"Content-Disposition": "inline; filename=generate_pdf.pdf"})
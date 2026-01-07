from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import io

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/fix-csv")
async def fix_csv(file: UploadFile = File(...)):
    raw = await file.read()

    text = raw.decode("latin1", errors="replace")

    fixed_lines = []
    for line in text.splitlines():
        parts = line.split("|")
        fixed_lines.append("|".join(parts[:51]))  # ajusta qtd colunas

    output = "\n".join(fixed_lines)

    buffer = io.BytesIO()
    buffer.write(output.encode("utf-8"))
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="fixed_{file.filename}"'
        }
    )

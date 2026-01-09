from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import io

app = FastAPI()

EXPECTED_COLUMNS = 39
DELIMITER = "|"

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/fix-csv")
async def fix_csv(file: UploadFile = File(...)):
    raw = await file.read()

    #  Decode seguro 
    text = raw.decode("latin1", errors="replace")

    #  Normaliza quebras de linha 
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    #  REMOVE aspas — CSV NÃO usa quote 
    # (isso resolve o erro do n8n definitivamente)
    text = text.replace('"', '')

    fixed_lines = []

    for line_number, line in enumerate(text.split("\n"), start=1):
        if not line.strip():
            continue

        parts = line.split(DELIMITER)

        #  Ajusta número de colunas 
        if len(parts) < EXPECTED_COLUMNS:
            parts.extend([""] * (EXPECTED_COLUMNS - len(parts)))
        elif len(parts) > EXPECTED_COLUMNS:
            parts = parts[:EXPECTED_COLUMNS]

        fixed_lines.append(DELIMITER.join(parts))

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

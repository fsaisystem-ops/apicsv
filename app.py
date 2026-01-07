from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
import csv
import io

app = FastAPI()

DELIM = "|"
ENCODING_IN = "latin1"
ENCODING_OUT = "utf-8"

@app.post("/fix-csv")
async def fix_csv(file: UploadFile = File(...)):
    raw = await file.read()
    text = raw.decode(ENCODING_IN, errors="ignore")

    reader = csv.reader(io.StringIO(text), delimiter=DELIM)
    rows = list(reader)

    cols = max(len(r) for r in rows)

    fixed = []
    for r in rows:
        if len(r) > cols:
            r = r[:cols-1] + [' '.join(r[cols-1:])]
        elif len(r) < cols:
            r = r + [''] * (cols - len(r))
        fixed.append(r)

    out = io.StringIO()
    writer = csv.writer(out, delimiter=DELIM)
    writer.writerows(fixed)

    return Response(
        content=out.getvalue().encode(ENCODING_OUT),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=fixed.csv"}
    )

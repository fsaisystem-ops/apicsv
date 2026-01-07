from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import csv
import io

app = FastAPI()

@app.post("/fix-csv")
async def fix_csv(file: UploadFile = File(...)):
    raw = await file.read()

    # força leitura tolerante (CSV quebrado / encoding ruim)
    text = raw.decode("latin1", errors="ignore")

    reader = csv.reader(io.StringIO(text), delimiter="|")
    output = io.StringIO()
    writer = csv.writer(output, delimiter="|", lineterminator="\n")

    for row in reader:
        writer.writerow(row)

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={file.filename}"
        }
    )

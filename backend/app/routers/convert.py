from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.csv_excel import convert_file_to_markdown

router = APIRouter(prefix="/api/convert", tags=["convert"])

ALLOWED_TABULAR_TYPES = {
    "text/csv",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel",
}

@router.post("/csv-excel")
async def convert_csv_excel(file: UploadFile = File(...)):
    if (
        file.content_type not in ALLOWED_TABULAR_TYPES
        and not file.filename.endswith((".csv", ".xlsx", ".xls"))
    ):
        raise HTTPException(status_code=400, detail="Only CSV and Excel files are supported.")
    content = await file.read()
    try:
        markdown = convert_file_to_markdown(content, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return {"filename": file.filename, "markdown": markdown}

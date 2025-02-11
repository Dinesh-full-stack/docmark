from fastapi import APIRouter, UploadFile, File, HTTPException, Body
from app.services.csv_excel import convert_file_to_markdown
from app.services.docx_converter import convert_docx_to_markdown
from app.services.html_converter import convert_html_to_markdown

router = APIRouter(prefix="/api/convert", tags=["convert"])

ALLOWED_TABULAR_TYPES = {
    "text/csv",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-excel",
}

@router.post("/csv-excel")
async def convert_csv_excel(file: UploadFile = File(...)):
    if (file.content_type not in ALLOWED_TABULAR_TYPES
            and not file.filename.endswith((".csv", ".xlsx", ".xls"))):
        raise HTTPException(status_code=400, detail="Only CSV and Excel files are supported.")
    content = await file.read()
    try:
        markdown = convert_file_to_markdown(content, file.filename)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return {"filename": file.filename, "markdown": markdown}

@router.post("/docx")
async def convert_docx(file: UploadFile = File(...)):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Only .docx files are supported.")
    content = await file.read()
    try:
        markdown = convert_docx_to_markdown(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
    return {"filename": file.filename, "markdown": markdown}

@router.post("/html")
async def convert_html(html: str = Body(..., embed=True)):
    if not html.strip():
        raise HTTPException(status_code=400, detail="HTML content cannot be empty.")
    try:
        markdown = convert_html_to_markdown(html)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")
    return {"markdown": markdown}

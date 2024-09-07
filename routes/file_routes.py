from fastapi import APIRouter, UploadFile, File

from domain.file_processor import FileProcessor

router = APIRouter()


@router.post("/file/create_file")
async def create_file():
    return FileProcessor().create_file()


@router.post("/upload_file/")
async def upload_file(file: UploadFile = File(...)):
    return await FileProcessor().upload_file(file)


@router.post("/file/add_data")
async def add_data():
    return {"message": "Dado adicionado com sucesso"}


@router.delete("/file/delete_data")
async def delete_data():
    return {"message": "Dado removido com sucesso"}


@router.get("/file/list_files")
async def list_files():
    return {"message": "Lista de dados"}

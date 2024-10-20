import csv
import os

from fastapi import HTTPException, status, UploadFile

from services.api_client import APIClient


class FileProcessor:
    """ Manager of files and folders processor."""

    def __init__(self):
        self.file_path = 'data/seu_file.csv'
        self.directory = 'data'
        self.api_client = APIClient()

    async def list_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, mode='r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)
                for row in csv_reader:
                    row_dict = dict(conta=row[0], agencia=row[1], texto=row[2], valor=row[3])
                    self.api_client.send_data(row_dict)
            return {"detail": "Arquivo processado com sucesso!"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Arquivo inexistente!")

    def create_file(self):
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['conta', 'agencia', 'texto', 'valor'])
                return {"mensagem": f"Arquivo {self.file_path} craido com suscesso."}
        else:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail="Arquivo já existe")

    async def add_data_to_file(self, data: dict):
        """
        Add data to file created
        :param data: account data history
        :return: error or success message
        """

        if os.path.exists(self.file_path):
            with open(self.file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([data["conta"], data["agencia"], data["texto"], data["valor"]])
                return {"mensagem": f"Dados inseridos com sucesso: {data}"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Arquivo inexistente, por favor acessar"
                                       " a rota de criar a arquivo.")

    async def delete_data(self, selected_line: int):
        if os.path.exists(self.file_path):
            with open(self.file_path, mode='r') as file:
                lines = file.readlines()

            if selected_line < 1 or selected_line >= len(lines):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Linha selecionada invalida.")

            with open(self.file_path, mode='w') as file:
                for index, line in enumerate(lines):
                    if index != selected_line:
                        file.write(line)
            return {"mensagem": "Linha selecionada deletada."}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Arquivo inexistente.")

    async def upload_file(self, file: UploadFile):
        """
        Upload a file to read and print data
        :param file: uploaded file
        :return: success or error
        """
        if file.filename.endswith('.csv'):
            try:

                contents = await file.read()
                decoded_file = contents.decode("utf-8").splitlines()

                csv_reader = csv.DictReader(decoded_file)
                for row in csv_reader:
                    self.api_client.send_data(row)
                return {"mensagem": f"Arquivo {file.filename} processado com sucesso"}
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"Falha ao processar a arquivo CSV: {str(e)}")

        else:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail="Apenas arquivo CSV")

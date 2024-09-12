import csv
import os

from fastapi import HTTPException, status, UploadFile


class FileProcessor:
    """ Manager of files and folders processor."""

    def __init__(self):
        self.file_path = 'data/seu_file.csv'
        self.directory = 'data'

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

    async def upload_file(self, file: UploadFile):
        """
        Upload a file to read and print data
        :param file: uploaded file
        :return: success or error
        """
        if file.filename.endswith('.csv'):
            try:
                # Decodifica o arquivo para string
                contents = await file.read()
                decoded_file = contents.decode('utf-8').splitlines()

                # Cria o CSV reader a partir do conteúdo decodificado
                csv_reader = csv.DictReader(decoded_file)

                for row in csv_reader:
                    data = {
                        "conta": row['conta'],  # Usa o nome correto da coluna no CSV
                        "agencia": row['agencia'],
                        "texto": row['texto'],
                        "valor": float(row['valor'])
                    }
                    print(data)

                return {"mensagem": f"Arquivo {file.filename} processado com sucesso"}
            except KeyError as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Erro: coluna {str(e)} não encontrada no CSV"
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Falha ao processar o arquivo CSV: {str(e)}"
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Apenas arquivos CSV são aceitos"
            )

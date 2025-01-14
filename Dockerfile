# Use uma imagem base do Python com a versão desejada
FROM python:3.12-slim

# Copia o arquivo requirements.txt para o container
COPY requirements.txt requirements.txt

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código para o container
COPY . .

# Executa a aplicação usando Uvicorn na porta 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
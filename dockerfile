# Imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto para o container
COPY . /app

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta da aplicação
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "run.py"]

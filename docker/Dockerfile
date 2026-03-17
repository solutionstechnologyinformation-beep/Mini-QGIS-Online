
# Use uma imagem base Python oficial
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Define a variável de ambiente para o Flask
ENV FLASK_APP=backend/app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expõe a porta que o Flask vai usar
EXPOSE 5000

# Comando para iniciar a aplicação Flask
CMD ["python", "backend/app.py"]

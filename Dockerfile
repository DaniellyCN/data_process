# Use a imagem Python 3.11.9 slim
FROM python:3.11.9-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie os arquivos de dependências primeiro para cachear a instalação de pacotes
COPY requirements.txt /app/

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie todos os arquivos do projeto para o container
COPY . /app

# Defina uma variável de ambiente para o arquivo .env
#ENV ENV_FILE_PATH=/app/.env

# Exponha a porta que o container irá usar, se necessário (opcional)
# EXPOSE 5000

# Comando padrão (que pode ser sobrescrito no docker-compose)
CMD ["python", "producer.py"]

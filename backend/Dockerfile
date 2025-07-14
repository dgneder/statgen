# statgen/backend/Dockerfile

# 1. Imagem Base
# Começamos com uma imagem oficial e leve do Python.
FROM python:3.12-slim

# 2. Variáveis de Ambiente
# Evita que o Python gere arquivos .pyc e garante que a saída do print vá direto para o terminal do contêiner.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Diretório de Trabalho
WORKDIR /app

# 4. Instalar Dependências
# Copiamos primeiro o requirements.txt para aproveitar o cache do Docker.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar o Código da Aplicação
COPY . .

# 6. Expor a Porta
# Expomos a porta 8000, que é a que o Django/Gunicorn usará.
EXPOSE 8000

# 7. Comando de Inicialização
# Roda a aplicação usando o Gunicorn quando o contêiner iniciar.
# Ele aponta para o nosso arquivo wsgi e escuta em todas as interfaces de rede na porta 8000.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi"]

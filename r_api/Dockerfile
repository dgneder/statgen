# statgen/r_api/Dockerfile

# 1. Imagem Base
# Usamos uma imagem do projeto 'rocker', que é otimizada para R.
FROM rocker/r-ver:4.3.3

# 2. Instalar Dependências do R
# Copiamos e executamos nosso script de instalação.
COPY install_packages.R .
RUN Rscript install_packages.R

# 3. Copiar o Código da Aplicação
COPY . .

# 4. Expor a Porta
EXPOSE 8001

# 5. Comando de Inicialização
# Inicia o servidor Plumber na porta 8001, escutando em todas as interfaces.
CMD ["R", "-e", "pr <- plumber::plumb('plumber.R'); pr$run(host='0.0.0.0', port=8001)"]

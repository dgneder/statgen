FROM ubuntu:latest
LABEL authors="oem"

# statgen/java-api/Dockerfile

# --- Estágio 1: O Construtor (Builder) ---
# Usamos uma imagem oficial do Maven que já inclui o JDK 17.
# Damos um "apelido" a este estágio: 'build'.
FROM maven:3.9.6-eclipse-temurin-17-focal AS build

# Define o diretório de trabalho dentro do contêiner.
WORKDIR /app

# Copia primeiro o pom.xml para aproveitar o cache de camadas do Docker.
# Se as dependências não mudarem, o Docker não as baixará novamente.
COPY pom.xml .
RUN mvn dependency:go-offline

# Copia o resto do código-fonte da nossa aplicação.
COPY src ./src

# Roda o comando do Maven para compilar o código e empacotá-lo em um .jar.
# O '-DskipTests' pula a execução de testes automatizados durante o build da imagem.
RUN mvn clean install -DskipTests


# --- Estágio 2: O Executor (Runner) ---
# Começamos com uma imagem base leve, que só tem o necessário para rodar Java.
FROM eclipse-temurin:17-jre-focal

# Define o diretório de trabalho.
WORKDIR /app

# Expõe a porta que a nossa aplicação Spring Boot usa (padrão 8080).
EXPOSE 8080

# Copia APENAS o arquivo .jar compilado do estágio 'build'.
# O caminho do .jar é padrão para projetos Maven.
COPY --from=build /app/target/java-api-*.jar app.jar

# O comando que será executado quando o contêiner iniciar.
ENTRYPOINT ["java", "-jar", "app.jar"]
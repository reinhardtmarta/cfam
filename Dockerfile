# Usa um Linux minúsculo com Python já instalado
FROM python:3.9-slim

# Define a pasta de trabalho dentro do contêiner
WORKDIR /app

# Copia o seu binário e o script para dentro do contêiner
COPY cfam .
COPY server.py .

# Instala o Flask (a biblioteca web do Python)
RUN pip install flask

# Garante que o Linux tem permissão para rodar o seu binário
RUN chmod +x cfam

# Avisa o Google que usaremos a porta 8080
EXPOSE 8080

# Comando que liga o servidor quando o contêiner iniciar
CMD ["python", "server.py"]


FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN chmod +x cfam || echo "cfam binário não encontrado"
CMD ["python", "server.py"]

import subprocess
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def run_cfam():
    # Pega o texto enviado pela internet
    payload = request.data.decode('utf-8')
    
    # Executa o seu binário CFAM passando o texto
    result = subprocess.run(['./cfam', payload], capture_output=True, text=True)
    
    # Se o filtro aceitou (Exit code 0), retorna o dado limpo
    if result.returncode == 0:
        return result.stdout, 200
    # Se o filtro bloqueou, retorna um aviso de erro
    else:
        return "Security Breach: Payload Blocked by CFAM\n", 403

if __name__ == '__main__':
    # O Cloud Run exige que a porta seja 8080
    app.run(host='0.0.0.0', port=8080)
  

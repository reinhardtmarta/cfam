import subprocess
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configurações do CFAM
# Certifique-se de que o binário 'cfam' esteja no mesmo diretório ou forneça o caminho completo
CFAM_BINARY_PATH = "./cfam"

def run_cfam_filter(payload):
    """
    Executa o binário CFAM para validar o payload.
    Retorna (True, output) se aprovado, (False, error_msg) se bloqueado ou erro.
    """
    if not os.path.exists(CFAM_BINARY_PATH):
        return False, "Erro Interno: Binário CFAM não encontrado no servidor."

    try:
        # Executa o binário passando o payload como argumento
        # O CFAM retorna Exit Code 0 para sucesso e 1 para bloqueio
        result = subprocess.run(
            [CFAM_BINARY_PATH, payload],
            capture_output=True,
            text=True,
            timeout=5  # Timeout de segurança
        )

        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, "Security Breach: Payload Blocked by CFAM"
            
    except subprocess.TimeoutExpired:
        return False, "Erro: A validação do CFAM excedeu o tempo limite."
    except Exception as e:
        return False, f"Erro inesperado na execução do CFAM: {str(e)}"

@app.route('/validate', methods=['POST'])
def validate_payload():
    """
    Endpoint para validar dados vindos de uma IA.
    Espera um JSON: {"data": "conteúdo para validar"}
    """
    content = request.json
    
    if not content or 'data' not in content:
        return jsonify({"error": "Requisição inválida. O campo 'data' é obrigatório."}), 400

    payload = content['data']
    
    # Chama o filtro CFAM
    is_safe, message = run_cfam_filter(payload)

    if is_safe:
        return jsonify({
            "status": "approved",
            "message": "Payload validado com sucesso.",
            "original_data": payload,
            "cfam_output": message
        }), 200
    else:
        return jsonify({
            "status": "blocked",
            "error": message
        }), 403

@app.route('/health', methods=['GET'])
def health_check():
    """Verifica se o serviço está online."""
    return jsonify({"status": "online", "cfam_binary_present": os.path.exists(CFAM_BINARY_PATH)}), 200

if __name__ == '__main__':
    # Permite execução externa e define a porta (padrão 8080 para compatibilidade com nuvem)
    app.run(host='0.0.0.0', port=8080, debug=True)

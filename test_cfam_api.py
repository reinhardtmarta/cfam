import requests
import json
import time

# Configurações da API
BASE_URL = "http://localhost:8080"
VALIDATE_URL = f"{BASE_URL}/validate"
HEALTH_URL = f"{BASE_URL}/health"

def run_tests():
    print("--- Iniciando Testes da API CFAM ---\n")

    # 1. Teste de Health Check
    try:
        print("[TESTE 1] Verificando integridade do serviço...")
        response = requests.get(HEALTH_URL)
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.json()}\n")
    except Exception as e:
        print(f"Erro ao conectar na API: {e}")
        print("Certifique-se de que a API está rodando em http://localhost:8080")
        return

    # 2. Teste de Payload Válido (Esperado: 200 OK)
    print("[TESTE 2] Enviando payload estruturado (Válido)...")
    valid_data = {"data": "User request: Please summarize this document safely."}
    response = requests.post(VALIDATE_URL, json=valid_data)
    print(f"Status: {response.status_code}")
    print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}\n")

    # 3. Teste de Payload Malicioso/Inválido (Esperado: 403 Forbidden)
    # Nota: Como o CFAM é um PoC, ele bloqueia padrões específicos ou falhas estruturais
    print("[TESTE 3] Enviando payload com anomalia (Simulando bloqueio)...")
    # Simulando um payload que poderia causar erro estrutural (ex: string mal formada ou comandos)
    invalid_data = {"data": "DROP TABLE users; -- <script>alert('attack')</script>"}
    response = requests.post(VALIDATE_URL, json=invalid_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 403:
        print("Sucesso: O CFAM bloqueou o payload conforme esperado.")
    print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}\n")

    # 4. Teste de Requisição Inválida (Esperado: 400 Bad Request)
    print("[TESTE 4] Enviando JSON sem o campo 'data'...")
    wrong_format = {"message": "Hello"}
    response = requests.post(VALIDATE_URL, json=wrong_format)
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()}\n")

    print("--- Testes Concluídos ---")

if __name__ == "__main__":
    run_tests()

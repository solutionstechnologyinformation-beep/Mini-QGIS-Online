'''
Este script automatiza o deploy do projeto Mini-QGIS-Online no Render.com.

Como usar:
1. Obtenha sua API KEY no Render: Dashboard > Account Settings > API Keys.
2. Certifique-se de que o projeto já está no seu GitHub e é público.
3. Execute o script: python deploy_render.py
'''

import requests
import json
import os
import sys

def deploy_to_render():
    print("🚀 Iniciando automação de deploy no Render.com...")
    
    # 1. Obter informações necessárias
    api_key = input("🔑 Insira sua API Key do Render: ").strip()
    if not api_key:
        print("❌ Erro: API Key é obrigatória.")
        return

    repo_url = input("📂 Insira a URL do seu repositório GitHub (ex: https://github.com/usuario/projeto): ").strip()
    if not repo_url:
        print("❌ Erro: URL do repositório é obrigatória.")
        return

    service_name = input("📛 Insira um nome para o serviço (padrão: mini-qgis-online): ").strip() or "mini-qgis-online"

    # Configurações da API
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    base_url = "https://api.render.com/v1"

    # 2. Criar o serviço Web
    payload = {
        "type": "web_service",
        "name": service_name,
        "ownerId": "", # O Render preenche automaticamente se vazio para o dono da chave
        "repo": repo_url,
        "autoDeploy": "yes",
        "serviceDetails": {
            "env": "python",
            "plan": "free",
            "buildCommand": "pip install -r backend/requirements.txt",
            "startCommand": "cd backend && python app.py",
            "region": "oregon",
            "envVars": [
                {"key": "FLASK_ENV", "value": "production"},
                {"key": "PORT", "value": "8000"},
                {"key": "PYTHON_VERSION", "value": "3.11.0"}
            ]
        }
    }

    print(f"\n📡 Enviando requisição para criar o serviço '{service_name}'...")
    
    try:
        response = requests.post(f"{base_url}/services", headers=headers, json=payload)
        
        if response.status_code == 201:
            data = response.json()
            service_id = data['service']['id']
            deploy_url = data['service']['serviceDetails']['url']
            
            print("✅ Serviço criado com sucesso!")
            print(f"🆔 ID do Serviço: {service_id}")
            print(f"🌐 URL do App: {deploy_url}")
            print("\n⏳ O primeiro deploy pode levar alguns minutos. Você pode acompanhar no dashboard do Render.")
        else:
            print(f"❌ Erro ao criar serviço: {response.status_code}")
            print(f"Detalhes: {response.text}")
            
    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    # Verificar se o requests está instalado
    try:
        import requests
    except ImportError:
        print("📦 Instalando biblioteca 'requests' necessária...")
        os.system(f"{sys.executable} -m pip install requests")
        import requests

    deploy_to_render()

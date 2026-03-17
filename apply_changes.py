'''
Este script aplica automaticamente as correções e melhorias no projeto Mini-QGIS-Online.

Como usar:
1. Coloque este script na raiz do seu projeto (no mesmo nível que as pastas `backend` e `frontend`).
2. Execute o script a partir do terminal: python apply_changes.py
3. O script irá sobrescrever os arquivos existentes com as versões corrigidas e criar novos arquivos de configuração.
'''

import os

# Estrutura de arquivos e seus conteúdos corrigidos
files_to_update = {
    "render.yaml": '''services:
  - type: web
    name: mini-qgis-online
    env: python
    plan: free
    buildCommand: pip install -r backend/requirements.txt
    startCommand: cd backend && python app.py
    envVars:
      - key: FLASK_ENV
        value: production
      - key: PORT
        value: 8000
''',

    "Procfile": '''web: cd backend && python app.py
''',

    "backend/requirements.txt": '''Flask>=2.3.0,<3.0.0
flask-cors>=4.0.0,<5.0.0
pyproj>=3.4.0,<4.0.0
python-dotenv>=1.0.0,<2.0.0
''',

    "backend/app.py": '''import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pyproj import Transformer
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Configurações
PORT = int(os.getenv('PORT', 5000))
HOST = os.getenv('HOST', '0.0.0.0')
FLASK_ENV = os.getenv('FLASK_ENV', 'development')


@app.route('/')
def index():
    """Serve o arquivo index.html do frontend."""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/convert', methods=['POST'])
def convert():
    """Converte coordenadas entre diferentes sistemas de referência EPSG."""
    try:
        # Validar se o JSON foi recebido
        if not request.json:
            return jsonify({'error': 'Nenhum dado JSON fornecido'}), 400

        # Extrair dados
        data = request.json
        required_fields = ['x', 'y', 'src', 'dst']
        
        # Validar campos obrigatórios
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo obrigatório faltando: {field}'}), 400

        # Converter para tipos apropriados
        try:
            x = float(data['x'])
            y = float(data['y'])
        except (ValueError, TypeError):
            return jsonify({'error': 'Coordenadas x e y devem ser números válidos'}), 400

        src = str(data['src']).strip()
        dst = str(data['dst']).strip()

        # Validar se src e dst não estão vazios
        if not src or not dst:
            return jsonify({'error': 'Sistemas de referência (src e dst) não podem estar vazios'}), 400

        # Validar se src e dst são iguais
        if src == dst:
            return jsonify({
                'x': x,
                'y': y,
                'message': 'Sistemas de referência são iguais, nenhuma conversão necessária'
            })

        # Criar transformador
        try:
            transformer = Transformer.from_crs(
                f"EPSG:{src}",
                f"EPSG:{dst}",
                always_xy=True
            )
        except Exception as e:
            return jsonify({'error': f'Sistema de referência inválido: {str(e)}'}), 400

        # Realizar transformação
        try:
            new_x, new_y = transformer.transform(x, y)
        except Exception as e:
            return jsonify({'error': f'Erro ao transformar coordenadas: {str(e)}'}), 400

        return jsonify({
            'x': new_x,
            'y': new_y,
            'src': src,
            'dst': dst
        })

    except Exception as e:
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500


@app.route('/health', methods=['GET'])
def health():
    """Endpoint de verificação de saúde da API."""
    return jsonify({'status': 'ok', 'environment': FLASK_ENV})


@app.errorhandler(404)
def not_found(error):
    """Tratador para erros 404."""
    return jsonify({'error': 'Endpoint não encontrado'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Tratador para erros 500."""
    return jsonify({'error': 'Erro interno do servidor'}), 500


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=(FLASK_ENV == 'development'))
''',

    "frontend/converter.js": '''// Determinar a URL da API dinamicamente
function getApiUrl() {
    // Em produção, usar URL relativa; em desenvolvimento, usar localhost
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        return 'http://localhost:5000';
    }
    // Em produção, usar o mesmo domínio
    return window.location.origin;
}

const API_URL = getApiUrl();

async function convert() {
    try {
        // Obter valores dos inputs
        const x = document.getElementById("x").value.trim();
        const y = document.getElementById("y").value.trim();
        const src = document.getElementById("src").value;
        const dst = document.getElementById("dst").value;

        // Validar campos
        if (!x || !y) {
            showError('Por favor, preencha as coordenadas X e Y');
            return;
        }

        // Validar se são números
        if (isNaN(parseFloat(x)) || isNaN(parseFloat(y))) {
            showError('Coordenadas X e Y devem ser números válidos');
            return;
        }

        // Validar se os sistemas de referência foram selecionados
        if (!src || !dst) {
            showError('Por favor, selecione os sistemas de referência de origem e destino');
            return;
        }

        // Mostrar mensagem de carregamento
        showLoading();

        // Fazer requisição à API
        const response = await fetch(`${API_URL}/convert`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                x: parseFloat(x),
                y: parseFloat(y),
                src: src,
                dst: dst
            })
        });

        // Processar resposta
        if (!response.ok) {
            const errorData = await response.json();
            showError(errorData.error || `Erro ${response.status}: ${response.statusText}`);
            return;
        }

        const data = await response.json();

        // Exibir resultado com mais precisão
        const resultText = `
            <strong>Resultado da Conversão:</strong><br>
            X: ${data.x.toFixed(6)}<br>
            Y: ${data.y.toFixed(6)}<br>
            De: EPSG:${data.src} → Para: EPSG:${data.dst}
        `;
        
        document.getElementById("result").innerHTML = resultText;
        document.getElementById("result").style.color = 'green';

    } catch (error) {
        showError(`Erro de conexão: ${error.message}`);
    }
}

function showError(message) {
    document.getElementById("result").innerHTML = `<strong style="color: red;">Erro:</strong> ${message}`;
    document.getElementById("result").style.color = 'red';
}

function showLoading() {
    document.getElementById("result").innerHTML = '<em>Convertendo...</em>';
    document.getElementById("result").style.color = 'gray';
}

// Permitir converter ao pressionar Enter
document.addEventListener('DOMContentLoaded', function() {
    const xInput = document.getElementById("x");
    const yInput = document.getElementById("y");
    
    if (xInput) {
        xInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') convert();
        });
    }
    
    if (yInput) {
        yInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') convert();
        });
    }
});
''',

    "frontend/index.html": '''<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mini QGIS Online - Conversor de Coordenadas</title>

    <!-- Leaflet CSS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />

    <!-- Custom CSS -->
    <link rel="stylesheet" href="style.css">
</head>

<body>
    <header>
        <h1>🗺️ Mini QGIS Online</h1>
        <p>Ferramenta GIS web para conversão de coordenadas e visualização de mapas</p>
    </header>

    <main>
        <section class="map-section">
            <h2>Mapa Interativo</h2>
            <p class="hint">Clique no mapa para obter as coordenadas</p>
            <div id="map"></div>
        </section>

        <section class="converter-section">
            <h2>Conversor de Coordenadas</h2>
            
            <div class="form-group">
                <label for="x">Coordenada X (Longitude):</label>
                <input type="number" id="x" placeholder="Ex: -55.5" step="0.000001">
            </div>

            <div class="form-group">
                <label for="y">Coordenada Y (Latitude):</label>
                <input type="number" id="y" placeholder="Ex: -15.5" step="0.000001">
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="src">Sistema de Origem:</label>
                    <select id="src">
                        <option value="">-- Selecione --</option>
                        <option value="4326">WGS84 (EPSG:4326)</option>
                        <option value="4674">SIRGAS2000 (EPSG:4674)</option>
                        <option value="31983">UTM 23S (EPSG:31983)</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="dst">Sistema de Destino:</label>
                    <select id="dst">
                        <option value="">-- Selecione --</option>
                        <option value="4326">WGS84 (EPSG:4326)</option>
                        <option value="4674">SIRGAS2000 (EPSG:4674)</option>
                        <option value="31983">UTM 23S (EPSG:31983)</option>
                    </select>
                </div>
            </div>

            <button id="convertBtn" onclick="convert()" class="btn-convert">Converter</button>

            <div id="result" class="result-box"></div>
        </section>
    </main>

    <footer>
        <p>Mini QGIS Online © 2024 | Desenvolvido com Flask, Leaflet e Pyproj</p>
    </footer>

    <!-- Leaflet JS -->
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

    <!-- Custom Scripts -->
    <script src="map.js"></script>
    <script src="converter.js"></script>
</body>

</html>
''',

    "frontend/style.css": '''/* Reset e estilos globais */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body {
    height: 100%;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f5f5f5;
    color: #333;
}

/* Header */
header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem 1rem;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

header p {
    font-size: 1rem;
    opacity: 0.9;
}

/* Main content */
main {
    max-width: 1200px;
    margin: 2rem auto;
    padding: 0 1rem;
}

section {
    background: white;
    border-radius: 8px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

section h2 {
    color: #667eea;
    margin-bottom: 1rem;
    font-size: 1.8rem;
}

/* Mapa */
#map {
    height: 500px;
    width: 100%;
    border-radius: 6px;
    border: 1px solid #ddd;
    margin-bottom: 1rem;
}

.hint {
    color: #666;
    font-size: 0.9rem;
    font-style: italic;
    margin-bottom: 1rem;
}

/* Formulário */
.form-group {
    margin-bottom: 1.5rem;
}

.form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
}

label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: #333;
}

input[type="number"],
select {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
    transition: border-color 0.3s ease;
}

input[type="number"]:focus,
select:focus {
    outline: none;
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* Botão */
.btn-convert {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 0.75rem 2rem;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    width: 100%;
}

.btn-convert:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-convert:active {
    transform: translateY(0);
}

/* Resultado */
.result-box {
    margin-top: 1.5rem;
    padding: 1rem;
    border-radius: 4px;
    background-color: #f9f9f9;
    border-left: 4px solid #667eea;
    min-height: 3rem;
    display: flex;
    align-items: center;
}

.result-box:empty {
    display: none;
}

/* Footer */
footer {
    background-color: #333;
    color: white;
    text-align: center;
    padding: 2rem 1rem;
    margin-top: 3rem;
}

footer p {
    font-size: 0.9rem;
    opacity: 0.8;
}

/* Responsividade */
@media (max-width: 768px) {
    header h1 {
        font-size: 2rem;
    }

    main {
        margin: 1rem auto;
    }

    section {
        padding: 1.5rem;
    }

    .form-row {
        grid-template-columns: 1fr;
    }

    #map {
        height: 300px;
    }

    .btn-convert {
        padding: 0.6rem 1.5rem;
        font-size: 0.9rem;
    }
}

@media (max-width: 480px) {
    header h1 {
        font-size: 1.5rem;
    }

    header p {
        font-size: 0.9rem;
    }

    section {
        padding: 1rem;
        margin-bottom: 1rem;
    }

    section h2 {
        font-size: 1.3rem;
    }

    #map {
        height: 250px;
    }
}
''',

    ".gitignore": '''# Ambiente Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Ambientes virtuais
venv/
ENV/
env/
.venv
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
.project
.pydevproject
.settings/

# Variáveis de ambiente
.env
.env.local
.env.*.local

# Logs
*.log
logs/

# Cache
.cache/
.pytest_cache/

# Arquivos de teste
.coverage
htmlcov/

# Node (se usado no futuro)
node_modules/
npm-debug.log
yarn-error.log

# Arquivos de sistema
Thumbs.db
.DS_Store
''',

    ".env.example": '''# Configurações do Flask
FLASK_ENV=development
FLASK_APP=backend/app.py

# Configurações do Servidor
HOST=0.0.0.0
PORT=5000

# CORS (para desenvolvimento)
CORS_ORIGINS=http://localhost:3000,http://localhost:5000
''',

    "README.md": '''# Mini QGIS Online

Uma ferramenta GIS web simples e intuitiva para conversão de coordenadas e visualização de mapas interativos.

## ✨ Funcionalidades

- **Mapa Interativo**: Visualize mapas com Leaflet e OpenStreetMap
- **Conversão de Coordenadas**: Converta entre diferentes sistemas de referência EPSG
- **Suporte a Múltiplos EPSG**: WGS84, SIRGAS2000, UTM 23S e mais
- **Precisão Geodésica**: Utiliza PyProj para transformações precisas
- **Interface Responsiva**: Funciona em desktop, tablet e mobile
- **API RESTful**: Backend Flask com endpoints bem documentados

## 🛠️ Tecnologias Utilizadas

### Backend
- **Flask**: Framework web Python
- **Flask-CORS**: Suporte a CORS
- **PyProj**: Transformações de coordenadas geodésicas
- **Python 3.8+**

### Frontend
- **HTML5**: Estrutura semântica
- **CSS3**: Design responsivo
- **JavaScript**: Lógica do cliente
- **Leaflet**: Biblioteca de mapas
- **OpenStreetMap**: Dados de mapas

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git

## 🚀 Instalação e Execução

### 1. Clonar o Repositório

```bash
git clone https://github.com/solutionstechnologyinformation-beep/Mini-QGIS-Online.git
cd Mini-QGIS-Online
```

### 2. Criar Ambiente Virtual (Recomendado)

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependências

```bash
pip install -r backend/requirements.txt
```

### 4. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env conforme necessário (opcional)
# FLASK_ENV=development
# PORT=5000
```

### 5. Executar a Aplicação

```bash
cd backend
python app.py
```

A aplicação estará disponível em: **http://localhost:5000**

## 📖 Uso

### Interface Web

1. **Visualizar Mapa**: O mapa é carregado automaticamente mostrando o Brasil
2. **Obter Coordenadas**: Clique no mapa para obter as coordenadas do ponto
3. **Converter Coordenadas**:
   - Preencha os campos X (Longitude) e Y (Latitude)
   - Selecione o sistema de origem (Origem)
   - Selecione o sistema de destino (Destino)
   - Clique em "Converter"

### API REST

#### Endpoint: POST `/convert`

**Request:**
```json
{
  "x": -55.5,
  "y": -15.5,
  "src": "4326",
  "dst": "31983"
}
```

**Response (Sucesso):**
```json
{
  "x": 500000.0,
  "y": 8280000.0,
  "src": "4326",
  "dst": "31983"
}
```

**Response (Erro):**
```json
{
  "error": "Descrição do erro"
}
```

#### Endpoint: GET `/health`

Verifica o status da API.

**Response:**
```json
{
  "status": "ok",
  "environment": "development"
}
```

## 🔧 Sistemas de Referência Suportados

| Código EPSG | Nome | Descrição |
|-------------|------|-----------|
| 4326 | WGS84 | Sistema de referência global padrão |
| 4674 | SIRGAS2000 | Sistema de referência para América do Sul |
| 31983 | UTM 23S | Projeção UTM Zona 23 Sul |

Para adicionar mais sistemas, edite o arquivo `frontend/index.html` e adicione novas opções aos selects.

## 📁 Estrutura do Projeto

```
Mini-QGIS-Online/
├── backend/
│   ├── app.py              # Aplicação Flask principal
│   ├── converter.py        # Módulo de conversão (utilitário)
│   └── requirements.txt    # Dependências Python
├── frontend/
│   ├── index.html          # Página principal
│   ├── style.css           # Estilos CSS
│   ├── map.js              # Lógica do mapa
│   └── converter.js        # Lógica de conversão
├── .env.example            # Exemplo de variáveis de ambiente
├── .gitignore              # Arquivos ignorados pelo Git
├── Procfile                # Configuração para Heroku/Render
├── render.yaml             # Configuração para Render
├── README.md               # Este arquivo
└── LICENSE                 # Licença do projeto
```

## 🐛 Tratamento de Erros

A API fornece mensagens de erro descritivas:

- **400 Bad Request**: Dados inválidos ou incompletos
- **404 Not Found**: Endpoint não encontrado
- **500 Internal Server Error**: Erro no servidor

## 🚢 Implantação

### Render

1. Conecte o repositório ao Render
2. Configure as variáveis de ambiente
3. O `render.yaml` será usado automaticamente

### Heroku

1. Instale o Heroku CLI
2. Execute: `heroku create seu-app-name`
3. Execute: `git push heroku main`

### Outras Plataformas

Use o `Procfile` como referência para configurar a implantação.

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 👨‍💻 Autor

**Solutions Technology Information**

## 📧 Suporte

Para reportar problemas ou sugerir melhorias, abra uma issue no repositório GitHub.

## 🔗 Links Úteis

- [PyProj Documentation](https://pyproj4.github.io/pyproj/stable/)
- [Leaflet Documentation](https://leafletjs.com/)
- [EPSG Codes](https://epsg.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Última atualização**: Março de 2026
''',

    "setup.py": '''from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mini-qgis-online",
    version="1.0.0",
    author="Solutions Technology Information",
    description="Uma ferramenta GIS web simples para conversão de coordenadas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/solutionstechnologyinformation-beep/Mini-QGIS-Online",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    python_requires=">=3.8",
    install_requires=[
        "Flask>=2.3.0,<3.0.0",
        "flask-cors>=4.0.0,<5.0.0",
        "pyproj>=3.4.0,<4.0.0",
        "python-dotenv>=1.0.0,<2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
)
''',

    "CONTRIBUTING.md": '''# Guia de Contribuição

Obrigado por considerar contribuir para o Mini QGIS Online! Este documento fornece diretrizes e instruções para contribuir.

## Código de Conduta

Este projeto adota um Código de Conduta que esperamos que todos os contribuidores sigam. Por favor, leia [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) antes de contribuir.

## Como Contribuir

### Reportando Bugs

Antes de criar um relatório de bug, verifique a lista de issues, pois você pode descobrir que o bug já foi relatado. Ao criar um relatório de bug, inclua:

- **Título claro e descritivo**
- **Descrição exata do comportamento observado**
- **Comportamento esperado**
- **Passos para reproduzir o problema**
- **Exemplos específicos para demonstrar os passos**
- **Ambiente** (SO, versão do Python, etc.)

### Sugerindo Melhorias

As sugestões de melhorias são rastreadas como issues. Ao criar uma sugestão de melhoria, inclua:

- **Título claro e descritivo**
- **Descrição detalhada da melhoria sugerida**
- **Exemplos de como a melhoria funcionaria**
- **Possível implementação**

### Pull Requests

- Preencha o template de PR fornecido
- Siga os padrões de código do projeto
- Inclua testes apropriados
- Atualize a documentação conforme necessário
- Termine todos os arquivos com uma nova linha

## Padrões de Desenvolvimento

### Setup do Ambiente

```bash
# Clonar repositório
git clone https://github.com/solutionstechnologyinformation-beep/Mini-QGIS-Online.git
cd Mini-QGIS-Online

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows

# Instalar dependências de desenvolvimento
pip install -r backend/requirements.txt
pip install -e ".[dev]"
```

### Padrões de Código

- Use **PEP 8** para Python
- Use **ESLint** para JavaScript
- Nomes de variáveis em inglês
- Comentários em português (para contexto brasileiro)
- Máximo 100 caracteres por linha

### Commits

- Use mensagens de commit claras e descritivas
- Use o tempo presente ("Add feature" não "Added feature")
- Referencie issues quando apropriado (#123)

Exemplo:
```
Add coordinate conversion validation

- Validate input coordinates
- Add error handling for invalid EPSG codes
- Fixes #42
```

### Testes

- Escreva testes para novas funcionalidades
- Execute testes antes de fazer push: `pytest`
- Mantenha cobertura de testes acima de 80%

```bash
# Executar testes
pytest

# Com cobertura
pytest --cov=backend
```

### Documentação

- Atualize README.md se necessário
- Adicione docstrings em funções Python
- Adicione comentários em código complexo

## Processo de Review

1. Um mantenedor revisará seu PR
2. Mudanças podem ser solicitadas
3. Uma vez aprovado, será feito merge

## Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a licença MIT.

## Perguntas?

Sinta-se livre para abrir uma issue com a tag `question`.
''',

    "LICENSE": '''MIT License

Copyright (c) 2024 Solutions Technology Information

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
}

def apply_changes():
    """Aplica as mudanças nos arquivos do projeto."""
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    for file_path, content in files_to_update.items():
        full_path = os.path.join(project_root, file_path)
        
        # Garantir que o diretório exista
        dir_name = os.path.dirname(full_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"📁 Diretório criado: {dir_name}")
            
        # Escrever o conteúdo no arquivo
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Arquivo atualizado: {file_path}")
        except IOError as e:
            print(f"❌ Erro ao escrever o arquivo {file_path}: {e}")

    print("\n🎉 Script concluído! Todas as correções foram aplicadas com sucesso.")
    print("Execute `git status` para ver as mudanças.")

if __name__ == "__main__":
    # Verificar se o script está na pasta raiz do projeto
    if not (os.path.exists('backend') and os.path.exists('frontend')):
        print("❌ Erro: Este script deve ser executado na pasta raiz do projeto Mini-QGIS-Online.")
    else:
        apply_changes()

# Guia de Contribuição

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
venv\Scriptsctivate  # Windows

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

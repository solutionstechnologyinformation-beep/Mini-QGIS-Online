# Mini-QGIS-Online

Um projeto básico em Rust para uma versão mini do QGIS online, usando Rocket para servir uma página web simples.

## Como executar

Certifique-se de ter o Rust instalado. Então:

```bash
cargo build
cargo run
```

O servidor será iniciado na porta 8000. Acesse http://localhost:8000 para ver a página inicial.

## Deploy

Este projeto pode ser implantado no Render.com ou outras plataformas que suportam Rust. Configure o comando de start como `./target/release/mini-qgis-online` ou similar.
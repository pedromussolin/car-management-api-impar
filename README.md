# API de Gerenciamento de Carros

## Descrição

Esta API RESTful foi desenvolvida com FastAPI para gerenciar informações sobre carros. Ela permite criar, ler, atualizar e deletar registros de carros, além de fornecer informações detalhadas sobre cada carro.

## Pré-requisitos

* **Python:** Versão 3.12.1 ou superior
* **virtualenv:** Para criar ambientes virtuais isolados
* **Docker:** Para containerizar a aplicação

## Configuração

1. Clone esse repositório:
    ```
    git clone <url-do-repositorio>
    cd <nome-do-repositorio>
    ```

2. Crie e ative o ambiente virtual:
    ```
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3. Instale as bibliotecas necessárias:
    ```
    pip install -r requirements.txt
    ```

4. Installe o Docker Desktop: 
    <a href="https://www.docker.com/products/docker-desktop/" target="_blank">Docker Desktop</a>

## Inicialização

Execute os seguintes comandos:
```
docker build -t imagem-api .
docker run -p 8000:8000 imagem-api
```

Para acessar a documentação da API basta seguir uma dessas URLs no navegador:<br>
    * http://127.0.0.1:8000/docs<br>
    * http://localhost:8000/docs
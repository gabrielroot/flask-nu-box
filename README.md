# Nu@Box

> Um remake das caixinhas do Nbank

Aplicação Flask + arquitetura modelo 

## Passos para inicializar a aplicação
- Copie o arquivo `.env.sample` e o renomeie para `.env`
- Aguarde até o serviço `db` estar "ready to accept connections"
- Esteja na pasta do projeto e execute os seguintes comandos no terminal:
```
$ docker-compose up
$ docker exec -it main flask db upgrade
```
Pronto! A aplicação já estará em execução

## Manipulando novas Migrations

`docker exec -it main flask db migrate -m "New migration."` - Para gerar uma nova migração, com base na diferença da estrutura do código e a do banco
`docker exec -it main flask db upgrade` - Para executar (efetivar) as alterações, no banco de dados.

## OK!

Agora basta acessar a aplicação através do navegador pelo endereço http://127.0.0.1:8000
<br>
<br>
E caso necessite, o Adminer em http://127.0.0.1:8080
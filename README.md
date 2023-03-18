# Nu@Box

> Um remake das caixinhas do Nubank

Aplicação Flask + arquitetura modelo 

## Passos para inicializar a aplicação
- Copie o arquivo `.env.sample` e o renomeie para `.env`
- Esteja na pasta do projeto e execute os seguintes comandos no terminal:
- `docker-compose up --build`
> Aguarde até o serviço `db` estar "ready to accept connections"
- `$ docker exec -it main flask db upgrade`

## OK! A aplicação já estará em execução

Agora basta acessar a aplicação através do navegador pelo endereço http://127.0.0.1:8000
<br>
E caso necessite, o Adminer em http://127.0.0.1:8080

<br>
<hr>
<br>

## Manipulando novas Migrations

- `docker exec -it main flask db migrate -m "New migration."` - Para gerar uma nova migração, com base na diferença entre a estrutura do código (Models) e a do banco.

- `docker exec -it main flask db upgrade` - Para executar (efetivar) as alterações, no banco de dados.

- `docker exec -it main flask db` - Para ver todos os comandos disponíveis do Flask-Migrate.

- `docker exec -it main flask` - Para ver todos os comandos disponíveis do Flask.

<br>
<br>

![Diagrama de classes](doc/Caixinhas@Root.drawio.png "Diagrama de classes")
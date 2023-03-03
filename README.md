
# Aplicação Flask + arquitetura modelo 

## Passos para inicializar a aplicação

Acesse o diretório _**`modelo`**_ e execute os seguintes comandos no terminal:
```
$ docker-compose up
$ docker exec -it main flask create-db
$ docker exec -it main flask populate-db
$ docker exec -it main flask add-user -u <digite um usuário> -p <digite uma senha>
```

Agora basta acessar a aplicação através do navegador pelo endereço http://127.0.0.1:8000
E caso necessite, o Adminer em http://127.0.0.1:8080
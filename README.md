# Nu@Box

> Um remake das caixinhas do Nubank

No ano passado (2022) a @Nubank, um banco digital em ascensão no mercado, criou uma nova funcionalidade que viria permitir que seus usuários pudessem além de guardar valores, definir objetivos para eles.
<br>
<br>
Essa criação me cativou muito devido a eu ter sentido falta dessa característica anteriormente e ter sido um dos que sugeriram tal feito.
<br>
<br>
Quando me foi solicitado como trabalho avaliativo da disciplina "Arquitetura de Software", o desenvolvimento de qualquer projeto em mente, que implementasse uma arquitetura predeterminada, isso me veio logo à mente:
> Criar um remake de funcionalidade.

<br>
A arquitetura base utilizada foi a do @rochacbruno, do canal codeshow. Tem como característica o uso dos padrões 'Factory Method + Singleton' na instanciação do app Flask. Com o adicional do uso de extensões, como forma diminuir o acoplamento do projeto. 


<br>

## Estrutura

<br>

```
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── migrations
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
│       ├── 00a17e17cbad_added_a_trait_to_work_with_soft_delete.py
│       ├── 98a6678d52ee_added_balances_table.py
│       └── edf73edcf51e_inital_migration.py
├── nuBox
│   ├── app.py
│   ├── blueprints
│   │   ├── __init__.py
│   │   ├── restapi
│   │   │   ├── __init__.py
│   │   │   └── resources.py
│   │   └── webui
│   │       ├── forms
│   │       │   ├── BoxForm.py
│   │       │   ├── __init__.py
│   │       │   └── TransactionForm.py
│   │       ├── __init__.py
│   │       ├── repository
│   │       │   ├── BalanceRepository.py
│   │       │   ├── BoxRepository.py
│   │       │   └── TransactionRepository.py
│   │       ├── services
│   │       │   ├── flashMessagesService.py
│   │       │   └── __init__.py
│   │       ├── static
│   │       │   └── images
│   │       │       └── UserRoot.ico
│   │       ├── templates
│   │       │   ├── boxes
│   │       │   │   ├── edit.html
│   │       │   │   ├── formActions.html
│   │       │   │   ├── __form.html
│   │       │   │   ├── index.html
│   │       │   │   └── new.html
│   │       │   ├── dashboard.html
│   │       │   ├── layout
│   │       │   │   ├── aside.html
│   │       │   │   ├── base.html
│   │       │   │   ├── flash_messages.html
│   │       │   │   ├── footer.html
│   │       │   │   ├── header.html
│   │       │   │   └── pagination.html
│   │       │   ├── transactions
│   │       │   │   ├── depositWithdraw.html
│   │       │   │   ├── __form.html
│   │       │   │   ├── index.html
│   │       │   │   └── __tableContent.html
│   │       │   └── user
│   │       │       └── profile.html
│   │       ├── urls.py
│   │       ├── utils
│   │       │   └── OPTransactionEnum.py
│   │       └── views
│   │           ├── boxView.py
│   │           ├── indexView.py
│   │           ├── __init__.py
│   │           ├── profileView.py
│   │           └── transactionView.py
│   ├── ext
│   │   ├── admin.py
│   │   ├── appearance.py
│   │   ├── authentication
│   │   │   ├── __init__.py
│   │   │   ├── templates
│   │   │   │   ├── base.html
│   │   │   │   ├── flash_messages.html
│   │   │   │   ├── login.html
│   │   │   │   └── signup.html
│   │   │   ├── urls.py
│   │   │   └── views
│   │   │       ├── authView.py
│   │   │       └── __init__.py
│   │   ├── commands.py
│   │   ├── configuration.py
│   │   ├── database.py
│   │   ├── __init__.py
│   │   ├── migrations.py
│   │   └── template_filters.py
│   └── __init__.py
├── README.md
├── requirements.txt
├── settings.toml
└── settings.toml.sample
```

<br>

## Passos para inicializar a aplicação
- Copie o arquivo `.env.sample` e o renomeie para `.env`
- Copie o arquivo `settings.toml.sample` e o renomeie para `settings.toml`
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

# Documentação
![Diagrama de classes](doc/Caixinhas@Root.drawio.png "Diagrama de classes")

<br>
<br>

# Processo
![Kanban](doc/kanban.png "Kanban")

<br>
<br>

# Capturas

### - Dashboard
> ![Dashboard](doc/dashboard.png "Dashboard")

<br>

### - Minhas Caixinhas
> ![Minhas Caixinhas](doc/myBoxes.png "Minhas Caixinhas")

<br>

### - Minhas Movimentações
> ![Minhas Movimentações](doc/myTransactions.png "Minhas Movimentações")

<br>

### - Editar Caixinha
> ![Editar Caixinha](doc/editBox.png "Editar Caixinha")
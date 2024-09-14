# Aula_Flask_REST_API
 REST APIs com Python e Flask

 **Aula_01**

- __API__ (Application Programming Interface) – É como uma interface entre dois programas diferentes de modo que eles possam se comunicar um com o outro.

- __REST__ (Transferência de Estado Representacional):  É um estilo de arquitetura web que define um conjunto de regras e restrições para a criação de APIs.

- __REST API__ é um __Web Service__ para se comunicar obrigatoriamente via rede. Todos Web Services são APIs, mas nem todas os APIs são Web Services.

- __O Flask__ é um __microframework__ para __desenvolvimento web__ escrito em Python. É conhecido pela sua simplicidade e flexibilidade, possibilitando a criação de sites, aplicativos web e APIs de forma rápida e eficiente.

- __Rotas__ de acesso são como os endereços específicos que você usa para acessar diferentes recursos
---

**Aula_02**

- __Resources__ (recursos): é a base da arquitetura RESTful, que organiza a API em torno de recursos interligados, acesso aos dados por meio de métodos, __regras de negocio__.
---

**Aula_03**

- __Models__ (modelos): servem como base para definir e gerenciar os dados que fluem através da API, __modelagem de objetos__ (colunas da tabela).
---

**Aula_03.1**

- Uso de __Resources__ (recursos) e __Models__ (modelos)
---

**Aula_04**

- __PROJETO HOTEL__

- __SQLAlchemy__ é uma biblioteca de __ORM__ (__Object-Relational Mapping__) em Python que permite interagir com bancos de dados usando classes e objetos, abstraindo as consultas SQL complexas.

- Arquivos: 
    - __.\models\hotel.py__: (modelos)
    - __.\resources\hotel.py__: CRUD hotel
    - __app.py__: rotas
    - __config_DB.py__: configuração Banco de Dados em __SQLAlchemy__
    - __sql_alchemy.py__: ORM (Object Relational Mapping) => conexão para Banco de Dados <=

- Operações __(CRUD)__:
    - __CREATE (Criar)__: Insere novos registros em uma tabela do banco de dados.
    - __READ (Ler)__: Recupera dados existentes na tabela, podendo filtrar por critérios específicos.
    - __UPDATE (Atualizar)__: Modifica o conteúdo de registros já existentes.
    - __DELETE (Excluir)__: Remove registros da tabela.

- __CRUD__:
    - CRUD - CREATE   |  READ        |  UPDATE     |  DELETE
    - =====> Criar    |  Ler         |  Atualizar  |  Excluir
    - <==========================================================>
    - API  - __POST__ |  __GET__     |  __PUT__    |  __DELETE__
    - =====> Enviar   |  Solicitar   |  Atualizar  |  Excluir
    - <==========================================================>
    - SQL  - INSERT   |  SELECT      |  UPDATE     |  DELETE
    - =====> Inserir  |  Selecionar  |  Atualizar  |  Excluir
---

**Aula_05**

- __PROJETO HOTEL__

- Arquivos: 
    - __.\models\usuario.py__: (modelos)
    - __.\resources\usuario.py__: CRUD usuario, login e logout, senha autenticação (JWT)
    - __.\resources\hotel.py__: autenticação token (JWT)
    - __app.py__: JWTManager, novas rotas
    - __blacklist.py__: listagem autenticação JSON Web Tokens (JWTs)
    - __config_DB.py__: configuração de JSON Web Tokens (JWTs)

- A autenticação __JWT__ (JSON Web Token) é uma técnica amplamente usada para autenticar usuários em aplicações web, incluindo APIs construídas com Flask. A ideia principal é fornecer uma maneira segura e eficiente de transmitir informações de autenticação entre o cliente (por exemplo, um navegador ou um aplicativo móvel) e o servidor.
---

**Aula_06**

- __PROJETO HOTEL__

- Arquivo: 
    - __.\resources\hotel.py__: filtros avançados de consulta e paginação de conteúdos na "__class Hoteis(Resource)__"
    - __config_DB.py__: solicitação de arquivo __.env__ (nome do banco de dados)
    - __.env__:  armazenar variáveis de ambiente em um formato de texto simples (segurança de informações sensíveis)


- Exemplo:
    - __URL: /hoteis?cidade=Rio de Janeiro&estrelas_min=4&diaria_max=400__
---

**Aula_07**

- __PROJETO HOTEL__

- Arquivo:
    - __.\models\site.py__: (modelos)
    - __.\models\hotel.py__: adição de chave estrangeira __site_id__ 
    - __.\resources\site.py__: CRUD site
    - __.\resources\hotel.py__: adição de __site_id__ para criação de hotéis
    - __app.py__: novas rotas

- Relacionamento entre tabelas __.\models\site.py__ e __.\models\hotel.py__.
---

**Aula_08**

- __PROJETO HOTEL__

- Arquivo:
    - __.\models\site.py__: incremento de ativação de cadastro, adição de email e método de ativação de cadastro por email
    - __.\resources\site.py__: adição email, ativação e nova rota de ativação de cadastro
    - __app.py__: novas rotas
    - __.\templates\user_confirm.html__: mensagem em HTML de confirmação de email

- Implementado método de ativação de cadastro via e-mail e mensagem de confirmação.
---

**MAILGUN**

- O __Mailgun__ é um serviço de API de e-mail transacional projetado para desenvolvedores. Em termos mais simples, é uma ferramenta que permite que seus aplicativos enviem, recebam e rastreiem e-mails de forma eficiente e confiável. 
- Arquivo __.env__ armazena variáveis de ambiente em um formato de texto simples (segurança de informações sensíveis)

**SQLITE**

- Criação de banco de dados SQLite via programação Python com pré-registos. 
---

**documentos**
- Arquivos em PDF sobre REST APIS.
---
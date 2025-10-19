# Aula_Flask_REST_API
 REST APIs com Python e Flask

**Aula_EXTRA**

 - "__Aula_EXTRA__" resumo das aulas: Aula_01, Aula_02 e Aula_03.
---

 **Aula_01**

 - __PROJETO HOTEL: Flask__

- __API__ (Application Programming Interface) – É como uma interface entre dois programas diferentes de modo que eles possam se comunicar um com o outro.

- __REST__ (Transferência de Estado Representacional):  É um estilo de arquitetura web que define um conjunto de regras e restrições para a criação de APIs.

- __REST API__ é um __Web Service__ para se comunicar obrigatoriamente via rede. Todos Web Services são APIs, mas nem todas os APIs são Web Services.

- __O Flask__ é um __microframework__ para __desenvolvimento web__ escrito em Python. É conhecido pela sua simplicidade e flexibilidade, possibilitando a criação de sites, aplicativos web e APIs de forma rápida e eficiente.

- __Rotas__ de acesso são como os endereços específicos que você usa para acessar diferentes recursos

- OBS: para sair do serviço pressione __Ctrl+C__ 
---

**Aula_02**

- __PROJETO HOTEL: CRUD__

- __Resources__ (recursos): são recursos de acesso aos dados por meio de métodos, __regras de negocio__.

- __Models__ (modelos): gerencia e valida __dados de transição entre API e Banco de Dados__, por meio de solicitação de usuário, permitindo apenas saída e entrada de dados definidos no modelo.

- Pasta e arquivos:
    - models:  
        - __.\models\hotel.py__: (modelos) => modelagem da dados "__dados_hoteis.py__"
    - resources: 
        - __.\resources\hotel.py__: (recursos) => CRUD hotel
    - __app.py__: (rota) =>  hoteis
    - __dados_hoteis.py__: armazenamento lista de hotéis "Banco de dados"

- O CRUD é o fundamento da persistência de dados, toda aplicação que **cria**, **lê**, **atualiza** ou **exclui** informações (em um BANCO DE DADOS ou API) está implementando é um CRUD.

- __.\resources\hotel.py__:
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

**Aula_03**

- __PROJETO HOTEL: Banco de Dados com SQLAlchemy__

- __Flask com Banco de dados__:

- Pasta e arquivos:
    - config:
        - __config_DB.py__: configuração Banco de Dados em __SQLAlchemy__
        - __sql_alchemy.py__: ORM (Object Relational Mapping) => conexão para Banco de Dados <=
    - models:  
        - __.\models\hotel.py__: (modelos) => Banco de Dados
    - resources: 
        - __.\resources\hotel.py__: (recursos) => CRUD hotel
    - __app.py__: configuração Banco em __SQLAlchemy__
    - __banco.db__: banco de dados (SQLite)

Onde: 
- __config_DB.py__:
    - O __SQLite__ é um sistema de gerenciamento de banco de dados relacional. Ver pasta **SQLite**.

- __.\models\hotel.py__,  __sql_alchemy.py__ & __app.py__:
    - __SQLAlchemy__ é uma biblioteca de __ORM__ (__Object-Relational Mapping__) em Python que permite interagir com bancos de dados usando classes e objetos, abstraindo as consultas SQL complexas. 

- __.\resources\hotel.py__:   
    - A __"classe Resource"__ serve como um modelo para a criação de recursos na API. Cada recurso pode ser representado por uma classe que herda de Resource, onde você pode definir métodos HTTP como GET, POST, PUT, DELETE, etc. Ver pasta **SQLAlchemy**.
        
    - Operações __(CRUD)__:
        - __CREATE (Criar)__: Insere novos registros em uma tabela do banco de dados.
        - __READ (Ler)__: Recupera dados existentes na tabela, podendo filtrar por critérios específicos.
        - __UPDATE (Atualizar)__: Modifica o conteúdo de registros já existentes.
        - __DELETE (Excluir)__: Remove registros da tabela.
---

**Aula_04**

- __PROJETO HOTEL: Autenticação com JWT__

- Arquivos: 
    - config:
        - __config_DB.py__: configuração de JSON Web Tokens (JWTs)
    - models:
        - __.\models\usuario.py__: (modelos) => Banco de Dados
    - resources:
        - __.\resources\hotel.py__: (recursos) => CRUD usuário, autenticação token (JWT)
        - __.\resources\usuario.py__: (recursos) => CRUD usuário, autenticação token (JWT)
    - __app.py__: JWTManager, (novas rotas) => usuarios, cadastro e login   


- A autenticação __JWT__ (JSON Web Token) é uma técnica amplamente usada para autenticar usuários em aplicações web, incluindo APIs construídas com Flask. A ideia principal é fornecer uma maneira segura e eficiente de transmitir informações de autenticação entre o cliente (por exemplo, um navegador ou um aplicativo móvel) e o servidor.
- pip install flask-jwt-extended
---

**Aula_05**

- __PROJETO HOTEL: Lista negra de autenticação JWL (BLACKLIST)__

- Arquivos: 
    - resources:
        - __.\resources\usuario.py__: (recursos) => __BLACKLIST__ (class UsuarioLogout)
    - __app.py__: __BLACKLIST__ (autenticação token), (nova rota) => logout
    - __blacklist.py__: __BLACKLIST__ 

- Uma __BLACKLIST__(ou lista negra) é um mecanismo de segurança utilizado para bloquear o acesso de entidades (como usuários, endereços IP, dispositivos, etc.) 
    - Autenticação e Tokens (JWT):
        - Quando um usuário faz logout ou sua sessão expira, o token JWT gerado pode ser colocado em uma blacklist. Isso impede que o token seja usado novamente, mesmo antes do tempo de expiração definido no próprio token. Ou seja, a blacklist serve para invalidar tokens de forma forçada (caso o usuário precise ser desconectado ou tenha seu acesso revogado).
---

**Aula_06**

- __PROJETO HOTEL: Filtros avançados de pesquisa__

- Arquivo:
    - resources: 
        - __.\resources\hotel.py__: filtros avançados de consulta e paginação de conteúdos na "__class Hoteis(Resource)__"

- Paginação de conteúdo é o processo de dividir os resultados de uma consulta em páginas menores.

- Um __filtro avançado__ permite que um cliente faça consultas mais precisas ao banco de dados por meio de parâmetros na URL:
    - URL/hoteis?cidade=Rio de Janeiro # retorno por nome
    - URL/hoteis?estrelas_max=3 # retorna valores igual ou menores que 3
    - URL/hoteis?estrelas_min=3 # retorna valores igual ou maiores que 3
    - URL/hoteis?diaria_max=100 # retorna valores igual ou menores que 100
    - URL/hoteis?diaria_min=100 # retorna valores igual ou maiores que 100
    - URL/hoteis?itens=5 # retorna 5 itens por pagina
    - URL/hoteis?pagina=1 # retorna número da pagina
    
    - Mesclar filtros:
        - URL/hoteis?cidade=Rio de Janeiro&estrelas_min=4&pagina=2

        - O ponto de interrogação (?) indica o início dos parâmetros de consulta.
        - O e comercial (&) separa cada par chave=valor, permitindo o envio de múltiplos parâmetros ao servidor.
        - Definido pela especificação do protocolo HTTP e pelas RFCs (Request for Comments) da Internet.

---

**Aula_07**

- __PROJETO HOTEL: Relacionamento entre tabelas (hotel e site)__

 - models:
        - __.\models\site.py__: (modelos) => Banco de Dados e relacionamento entre tabelas (chave estrangeira)
        - __.\models\hotel.py__: (modelos) => Banco de Dados e relacionamento entre tabelas
    - resources:
        - __.\resources\site.py__: (recursos) => CRUD site, autenticação token (JWT)
        - __.\resources\hotel.py__: (recursos) => filtro "site_id" em métodos post e put (class Hotel)
    - __app.py__: (nova rota) => sites

- O relacionamento entre tabelas é a forma como conectamos dados de diferentes tabelas usando chaves primárias e chaves estrangeiras. Isso permite manter os dados organizados e evitar redundâncias.
---

**Aula_08**

- __PROJETO HOTEL: Implementado método de ativação de cadastro via e-mail e mensagem de confirmação__

- Arquivo:
    - models:
        - __.\models\usuario.py__: (modelos) => adição de método de ativação de cadastro por email e complementações
    - resources:
        - __.\resources\usuario.py__: (recursos) => adição de __"class UsuarioAtivacao"__ e complementações
    - templates\:
        - __.\templates\user_confirm.html__: mensagem em HTML de confirmação de email
    - __app.py__: (nova rota) => ativacao 

- __.\models\usuario.py__: 
    - O __Mailgun__ é um serviço de API de e-mail transacional projetado para desenvolvedores. 
    - Arquivo __.env__ armazena variáveis de ambiente em um formato de texto simples (segurança de informações sensíveis).
    - __request__ é um objeto que permite acessar dados enviados pelo cliente, como parâmetros de URL
    - __url_for__ é usado para construir URLs dinamicamente com base no nome da função da rota.

- __.\resources\usuario.py__:
    - __traceback.print_exc()__ é usado para imprimir o rastreamento completo de exceções (erros).
    - make_response(...): Esta função cria uma resposta HTTP personalizada.
    - render_template: Esta função renderiza um template HTML, quando você deseja retornar uma resposta para uma rota

- __.\templates\user_confirm.html__:
    - O arquivo __"user_confirm.html"__ obrigatoriamente deve esta alocado em uma pasta de nome "templastes", pois o Flask irá procurar este arquivo no diretório de templates da aplicação por padrão de uso HTML.     
---

**Aula_09**

- __PROJETO HOTEL: validação personalizada de valores inserido nas tabelas__

- Arquivo:
    - resources:
        - __.\resources\hotel.py__: validação personalizada __"class Hotel"__ (restricao_estrelas e restricao_diaria)
        - __.\resources\site.py__: validação personalizada __"class Site"__ = POST
        - __.\resources\usuario.py__: validação personalizada __"class CadastroUsuario"__ = POST
---

**HOTEL**

- __PROJETO HOTEL: Remodelação modelagem e recursos__

- Arquivo:
    - models:
        - __.\models\hotel.py__: (modelos) => eliminação de filtros e métodos
        - __.\models\site.py__: (modelos) => eliminação de filtros e métodos
        - __.\models\usuario.py__: (modelos) => eliminação de filtros e métodos
    - resources:
        - __.\resources\hotel.py__: (recursos) => alocação de filtros e métodos do model
        - __.\resources\site.py__: (recursos) => alocação de filtros e métodos do model
        - __.\resources\usuario.py__: (recursos) => alocação de filtros e métodos do model

- Foi realizado um esforço para enxugar dos modelos (models) os métodos e filtros, realocando os memos nas aplicações de GET, POST, PUT e DELETE nos respectivos recurso (resources), com o intuito de facilitar futuras intervenções ou manutenções. 
---

**SQLITE**
- Criação de banco de dados SQLite via programação Python com pré-registos. 
---

**SQLAlchemy**
- __SQLAlchemy__ é uma biblioteca de __ORM__ (__Object-Relational Mapping__) em Python que permite interagir com bancos de dados usando classes e objetos, abstraindo as consultas SQL complexas.
---

**JWT**
- A autenticação __JWT__ (JSON Web Token) é uma técnica amplamente usada para autenticar usuários em aplicações web.

- APP Insomnia ou Postman: 
    Body:
        JSON __(envio por POST ou PUT)__

    Headers:
        <CHAVE>         <VALOR>
        Authorization   Bearer __SUA SENHA TOKEN__
        Content-Type    application/json __(caso tenha Body)__
---

**JWT_BLACKLIST**
- A __BLACKLIST__ (lista negra) em JWT é uma estrutura usada para armazenar tokens inválidos ou revogados, impedindo que sejam usados novamente para autenticação. Ela é usada para forçar o logout de usuários ou invalidar tokens comprometidos antes de seu vencimento.
---

**MAILGUN**
- O __Mailgun__ é um serviço de API de e-mail transacional projetado para desenvolvedores. Em termos mais simples, é uma ferramenta que permite que seus aplicativos enviem, recebam e rastreiem e-mails de forma eficiente e confiável. 
- Arquivo __.env__ armazena variáveis de ambiente em um formato de texto simples (segurança de informações sensíveis)
---

**DOCUMENTOS_EM_PDF**
- Arquivos em PDF sobre REST APIS.
---
# Record Shop

Projeto criado para aprendizado, aqui é implementado um certo controle de concorrência para um ecommerce fictício.

A proposta é suportar um estresse de cerca de 50 requisições de venda/segundo por 60 segundos sem perder a consistência
do banco. Isto é, começando com os pedidos vazios e um estoque X, ao final do teste de estresse, é preciso que o
somatório das quantidades de vendas mais o estoque restante igual ao estoque inicial.

## Tecnologias utilizadas

- Python: Não tive opção, me foi passado que deveria fazer em Python, se não, faria em Node/Typescript ou C#.
- FastAPI: Minimalista, muito rápido e funcional, tem ainda muitas deficiências em questão do ecossistema, como suporte
  a múltiplos escopos de injeção de dependência (como `AddTransient`, `AddScoped` e `AddSingleton` no `.NET`), mas pelo
  menos é construído em cima do ASGI, ao invés do WSGI, como o Flask, então foi bem simples utilizar event
  loop/`async await`.
- Pydantic: Biblioteca simples pra realizar algumas validações, não conheço muito, mas achei interessante, utilizei mais
  por requisito do FastAPI.
- PostgreSQL: Amigo de longa data e adequado ao
  contexto ('[just use postgres mate](https://www.reddit.com/r/ProgrammerHumor/comments/9e002w/when_i_ask_coworkers_what_db_should_i_choose_for/)')
  . Pensei em incluir Redis pra fazer um cache e DynamoDB/MongoDB pra escrever os pedidos, mas temos mais o que fazer no
  momento.
- asyncpg: Biblioteca para conexão com o postgres, precisava de algo que tivesse suporte a `async/await` e não fosse um
  pesadelo de usar em Darwin/arm64, depois de sofrer muito tentando usar o `psycopg2` e alguns de seus monstrinhos,
  como `aiopg`, achei essa alternativa muito boa.
- Docker/Docker Compose: Porque eu não quero instalar docker no meu computador e porque dizer 'roda no meu container' é
  mais fancy do que 'roda na minha máquina'.
- PyCharm/SonarLint: Foi o que usei pra formatar e guiar o estilo de código.

## Solução

O projeto é basicamente um serviço CRUD para os discos `DiscCrud`, um mais simples para cadastrar/atualizar
clientes `CustomerService`, e mais um pra fazer um pedido `PurchaseOrderService`. Cada um desses serviços tem um
repositório, e o `PurchaseOrderService` consome os repositórios dos outros (poderia criar outra interface só
pro `PurchaseOrderService`? Sim, em um escopo maior). O FastAPI basicamente chama esse serviço, que é puxado por meio
do "container" (grandes aspas aqui) de injeção de dependência dele e trata algumas exceções pra enviar o código HTTP
certo e tal. As "camadas" lidando com requisições, gateway pro BD e aplicação estão razoavelmente desacopladas.

E sim, faltam testes automatizados, num escopo maior ou projeto real, incluiria. Mas testar só o CRUD e uma operação que
é insert + update, ia parecer mais um sanity check.

E estão faltando consultas dos pedidos também, mas seguiria o modelo de consulta de discos, talvez colocasse uns índices
nas datas e id de usuário (já que as requisições de pedidos provavelmente seriam de um certo usuário e os últimos X
pedidos, até uma certa data ou ordenado por data), mas daí num contexto real é preciso discutir com o cliente/PO/PM/sei
lá quem antes.

Agora sobre o teste de estresse e controle de concorrência no endpoint de vendas:

- O problema é essencialmente receber muitas requisições e não deixar o sistema vender mais discos do que tem em
  estoque. Em segundo plano também é interessante que os usuários não fiquem levando 500 toda hora.
- Consistência:
    - Otimista: Tentar fazer o que precisa ser feito, mas se alguém tiver mexido na linha do DB que armazena o disco,
      aborta. Claramente, vai dar um monte de erros a qualquer momento que tiver mais de 1 usuário tentando comprar a
      mesma coisa em um curto intervalo de tempo.
    - Lock/Pessimisita: Travar a linha do DB que armazena o disco com um `select for update`, fazer o que precisa ser
      feito e liberar. Tem um certo overhead, mas o postgres aguenta bem, então é o padrão. Testei isso com um
      connection pool de vários tamanhos, e até com só 1 conexão deu resultados muito bons.
    - Assíncrono (Não implementado): Registrar o pedido numa base de dados qualquer (pode ser o postgres, dynamodb, um
      txt no google drive de algúem) com um status 'PENDENTE' ou algo do tipo e depois publicar numa fila uma requisição
      pra "separar" o pedido, entende-se separar por decrementar o estoque e atualizar o pedido pra 'SEPARADO' ou
      similar. É o que produziria o maior throughput, porque o pedido seria basicamente um ping na fila e um insert, sem
      locks nem nada, pode deixar isso no worker que for consumir essas mensagens pra separar os pedidos. Daria até pra
      ter um modelo híbrido com circuit breaker que tenta separar o pedido ainda na requisição e já devolver pro usuário
      que o pedido foi separado e tá tudo OK (HTTP 200 OK), e se demorar muito pra conseguir o lock, quebra o circuito e
      passa a mandar pra fila mesmo (HTTP 202 ACCEPTED) daí.

Aliás, também seria interessante adicionar um OpenTelemetry pra ver o tempo consumido entre chamadas ao postgres via
Jaeger/Tempo e uns contadores via Prometheus pra ajustar uns parâmetros tipo quantidade de conexões, eventualmente
quantidade de réplicas um deployment e o quanto precisaria escalar o postgres.

## Instruções

### Metal

1. Instalar dependências (em `requirements.txt`, com Python 3.8+)
2. Configurar DB com migrations, em `db/migrations`
3. Preencher DB com seed, em `db/seed/seed.sql` (Opcional)
4. Executar arquivo `api/main.py` com FastAPI e variáveis de ambiente de acordo com as chamadas em `api/deps.py`.

### Docker

1. `docker-compose -f oci/docker-compose.yml up -d`

## Configurações

- `POSTGRES_HOST`: Endereço do PostgreSQL
- `POSTGRES_PORT`: Porta do PostgreSQL
- `POSTGRES_USER`: Usuário do PostgreSQL
- `POSTGRES_PASSWORD`: Senha do PostgreSQL
- `POSTGRES_DB`: Nome do DB a ser utilizado
- `POSTGRES_SCHEMA`: Nome do schema a ser utilizado
- `USE_OPTIMISTIC_CC`: Se `true`, em transações críticas __não__ haverá locking (`SELECT FOR UPDATE`) no banco de dados
  e utilizarão isolamento `REPEATABLE READ`, caso contrário, utilizará `SELECT FOR UPDATE` e
  isolamento `READ COMMITTED` (lembrando que o PostgreSQL não implementa `READ UNCOMITTED` de fato). Isso naturalmente
  deve produzir mais erros em picos de utilização, definitivamente não é a abordagem adequada, mas achei pertinente ter
  outra referência onde é mais aceitável falhar a requisição, contanto que a consistência não seja afetada.

## Testes

O teste de estresse foi feito com o [Siege](https://formulae.brew.sh/formula/siege), e com o seguinte comando:

```shell
siege -d1 -c90 -t120s --content-type "application/json"  \
'http://localhost:8100/purchase-orders POST {"disc_id": "bcd8a0e9-dc0a-4ae7-a783-458542e2cc39","customer_id": "0e92cf1e-7bc4-4f9e-8eb6-3c88627efecb","quantity": 1}'
```

Esse comando tentará produzir 90 requisições por segundo, por 120 segundos. O relatório produzido pelo siege após
executar esse teste executando o app via docker-compose num Macbook Air M1 (16GB) foi:

```
Lifting the server siege...
Transactions:		        5747 hits
Availability:		      100.00 %
Elapsed time:		      119.87 secs
Data transferred:	        0.38 MB
Response time:		        1.81 secs
Transaction rate:	       47.94 trans/sec
Throughput:		        0.00 MB/sec
Concurrency:		       86.84
Successful transactions:         500
Failed transactions:	           0
Longest transaction:	       10.41
Shortest transaction:	        0.04
```

Outros testes podem ser realizados via um cliente HTTP. O detalhamento dos endpoints pode ser visto em `api/main.py` ou
na pasta `rest-docs`, onde os endpoints estão documentados em formato `har` e podem ser consumidos
pelo [Insomnia REST Client](https://insomnia.rest/).
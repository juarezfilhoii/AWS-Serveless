# Serverless Visitor Counter

API 100% serverless na AWS que conta visitas em tempo real — sem nenhum servidor rodando continuamente, sem custo (dentro do Always Free Tier da AWS).

## 🎯 Objetivo do projeto

Explorar, na prática, a diferença entre infraestrutura tradicional (servidor sempre ligado) e arquitetura serverless (código que roda apenas sob demanda), usando um caso de uso simples e visual: um contador de visitas que incrementa a cada acesso.

## 🏗️ Arquitetura

```
Requisição HTTP
      │
      ▼
Lambda Function URL (endpoint público, HTTPS)
      │
      ▼
AWS Lambda (Python) — processa a requisição
      │
      ▼
DynamoDB — incrementa e persiste o contador
```

| Componente | Serviço | Função |
|---|---|---|
| Endpoint | Lambda Function URL | Link HTTPS público, sem necessidade de API Gateway |
| Processamento | AWS Lambda (Python 3.13) | Executa sob demanda, sem servidor fixo |
| Persistência | DynamoDB | Armazena o contador de forma durável |

## 💰 Custo

Todos os serviços usados fazem parte do **Always Free Tier** da AWS (sem prazo de expiração):

- **Lambda:** 1 milhão de requisições grátis/mês
- **DynamoDB:** 25GB de armazenamento grátis
- **Lambda Function URL:** sem custo adicional

Para o volume de acesso de um projeto de portfólio pessoal, o custo esperado é **US$0,00**.

## 🚀 Como usar

Acesse a URL pública abaixo — cada acesso incrementa o contador:

```
https://mpxupm5p5baqwzxspkkcj2vgii0gvhdy.lambda-url.us-east-1.on.aws/
```

Resposta esperada:
```json
{"visits": 42}
```

## 🛠️ Como replicar

1. **Criar a tabela no DynamoDB**
   - Nome: `visitor-counter`
   - Partition key: `id` (String)
   - Adicionar item inicial: `{"id": "counter", "count": 0}`

2. **Criar a função Lambda**
   - Runtime: Python 3.13
   - Colar o código de [`lambda_function.py`](./lambda_function.py)

3. **Dar permissão de acesso ao DynamoDB**
   - Anexar a policy `AmazonDynamoDBFullAccess` à role de execução da Lambda
   (em produção, recomenda-se restringir a uma policy customizada com permissão apenas de `UpdateItem` na tabela específica)

4. **Criar a Function URL**
   - Configuration → Function URL → Auth type: `NONE`

## 🐛 Problema encontrado e solução

O contador incrementava **2 vezes por acesso** no navegador. Causa: o navegador faz uma segunda requisição automática para `/favicon.ico`, e a Lambda respondia (e incrementava) para qualquer caminho recebido.

**Solução:** filtrar a requisição pelo caminho (`rawPath`), incrementando o contador apenas quando o caminho for exatamente `/`:

```python
path = event.get('rawPath', '/')
if path != '/':
    return {'statusCode': 404, ...}
```

## 📌 Projeto relacionado

Esse projeto complementa um outro projeto de portfólio com arquitetura tradicional (EC2 + Docker + containers sempre ativos): [GLPI Dockerizado](https://github.com/juarezfilhoii/Curso-de-Docker) — juntos, mostram domínio tanto de infraestrutura clássica quanto de arquitetura serverless.

## 📄 Licença

Este projeto está sob a licença MIT — veja [LICENSE](./LICENSE) para mais detalhes.
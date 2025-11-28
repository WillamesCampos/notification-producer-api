# 🔔 Notification System

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.122+-green.svg)](https://fastapi.tiangolo.com/)
[![Kafka](https://img.shields.io/badge/Kafka-7.5.0-orange.svg)](https://kafka.apache.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Sistema de notificações distribuído baseado em arquitetura de microserviços e event-driven, utilizando Apache Kafka como message broker. O sistema permite a publicação e consumo de eventos de notificação de forma assíncrona e escalável.

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Arquitetura](#-arquitetura)
- [Tecnologias](#-tecnologias)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Execução](#-instalação-e-execução)
- [API Endpoints](#-api-endpoints)
- [Formato dos Eventos](#-formato-dos-eventos)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Comandos Úteis](#-comandos-úteis)
- [Roadmap](#-roadmap)
- [Troubleshooting](#-troubleshooting)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

---

## 🎯 Sobre o Projeto

O **Notification System** é uma solução moderna para gerenciamento de notificações em tempo real, construída com arquitetura de microserviços e padrões event-driven. O sistema foi projetado para ser:

- ⚡ **Assíncrono**: Processamento não-bloqueante de eventos
- 🔄 **Escalável**: Arquitetura distribuída com Kafka
- 🛡️ **Resiliente**: Tolerante a falhas com retry automático
- 🚀 **Performático**: FastAPI com suporte nativo a async/await
- 📦 **Containerizado**: Deploy simplificado com Docker Compose

---

## 🏗️ Arquitetura

### Visão Geral

```
┌─────────────────┐
│   Cliente HTTP  │
└────────┬────────┘
         │
         │ HTTP REST
         ▼
┌─────────────────────────────────────┐
│  notification-producer-api          │
│  (FastAPI - Porta 8001)            │
│  - Recebe requisições HTTP          │
│  - Valida payloads                  │
│  - Publica eventos no Kafka         │
└──────────────┬──────────────────────┘
               │
               │ Eventos JSON
               ▼
┌─────────────────────────────────────┐
│  Apache Kafka                       │
│  (Porta 9092/9093)                  │
│  Topic: notifications               │
└──────────────┬──────────────────────┘
               │
               │ Consome eventos
               ▼
┌─────────────────────────────────────┐
│  notification-service (FUTURO)      │
│  - Consome eventos do Kafka         │
│  - Processa notificações            │
│  - Persiste no MongoDB              │
└──────────────┬──────────────────────┘
               │
               │ Dados persistidos
               ▼
┌─────────────────────────────────────┐
│  MongoDB                            │
│  (Porta 27017)                      │
│  Database: notifications_db         │
└─────────────────────────────────────┘
```

### Componentes Principais

#### 1. **notification-producer-api** 🚀
- **Tecnologia**: Python 3.12 + FastAPI
- **Porta**: 8001
- **Responsabilidade**: Expõe API REST para receber e publicar eventos no Kafka
- **Dependências principais**: FastAPI, Uvicorn, aiokafka, Pydantic

#### 2. **Apache Kafka** 📨
- **Versão**: 7.5.0 (Confluent Platform)
- **Portas**: 9092 (interno), 9093 (host)
- **Responsabilidade**: Gerenciar filas de mensagens e distribuir eventos entre serviços
- **Tópicos**: `notifications`

#### 3. **Apache Zookeeper** 🗂️
- **Versão**: 7.5.0 (Confluent Platform)
- **Porta**: 2181
- **Responsabilidade**: Gerenciar metadados e coordenação do cluster Kafka

#### 4. **MongoDB** 🍃
- **Versão**: Latest
- **Porta**: 27017
- **Responsabilidade**: Armazenar notificações processadas
- **Database**: `notifications_db`
- **Credenciais**: `root` / `password`

---

## 🛠️ Tecnologias

### Backend
- **Python 3.12** - Linguagem de programação
- **FastAPI** - Framework web assíncrono moderno
- **Uvicorn** - Servidor ASGI de alta performance
- **aiokafka** - Cliente Kafka assíncrono para Python
- **Pydantic** - Validação de dados e configurações

### Infraestrutura
- **Docker & Docker Compose** - Containerização e orquestração
- **Apache Kafka** - Message broker distribuído
- **Apache Zookeeper** - Coordenação de serviços distribuídos
- **MongoDB** - Banco de dados NoSQL

### Ferramentas
- **uv** - Gerenciador de pacotes Python moderno e rápido

---

## 📁 Estrutura do Projeto

```
notification-producer-api/
├── docker-compose.yaml              # Orquestração de todos os serviços
├── README.md                        # Este arquivo
│
└── notification-system/
    └── services/
        └── notification-producer-api/
            ├── Dockerfile           # Imagem Docker do serviço
            ├── Makefile             # Comandos auxiliares
            ├── pyproject.toml       # Configuração do projeto Python
            ├── uv.lock              # Lock file das dependências
            ├── README.md            # Documentação específica do serviço
            │
            └── src/
                └── notification_producer_api/
                    ├── __init__.py
                    ├── main.py              # Aplicação FastAPI principal
                    ├── config.py            # Configurações e settings
                    │
                    └── infrastructure/
                        ├── __init__.py
                        └── kafka_producer.py  # Cliente Kafka Producer
```

---

## 📦 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Docker** 20.10+ ([Instalação](https://docs.docker.com/get-docker/))
- **Docker Compose** 2.0+ ([Instalação](https://docs.docker.com/compose/install/))
- **Python 3.12+** (opcional, para desenvolvimento local)
- **uv** (opcional, para desenvolvimento local) ([Instalação](https://github.com/astral-sh/uv))

---

## 🚀 Instalação e Execução

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd notification-producer-api
```

### 2. Suba todos os serviços com Docker Compose

```bash
docker-compose up --build
```

Este comando irá:
- ✅ Construir a imagem do `notification-producer-api`
- ✅ Iniciar o Zookeeper
- ✅ Iniciar o Kafka
- ✅ Iniciar o MongoDB
- ✅ Iniciar a API na porta 8001

### 3. Verifique se os serviços estão rodando

Aguarde aproximadamente 30-60 segundos para todos os serviços inicializarem completamente. Você pode verificar os logs:

```bash
docker-compose logs -f
```

### 4. Teste o Health Check

```bash
curl http://localhost:8001/health
```

**Resposta esperada:**
```json
{
  "status": "ok",
  "service": "notification-producer-api"
}
```

### 5. Teste o endpoint raiz

```bash
curl http://localhost:8001/
```

**Resposta esperada:**
```json
{
  "message": "Notification Producer API is running"
}
```

---

## 📡 API Endpoints

**Base URL**: `http://localhost:8001`

### `GET /`
Endpoint raiz que retorna uma mensagem de boas-vindas.

**Exemplo de requisição:**
```bash
curl http://localhost:8001/
```

**Resposta:**
```json
{
  "message": "Notification Producer API is running"
}
```

---

### `GET /health`
Health check do serviço. Útil para monitoramento e verificação de status.

**Exemplo de requisição:**
```bash
curl http://localhost:8001/health
```

**Resposta:**
```json
{
  "status": "ok",
  "service": "notification-producer-api"
}
```

**Status Codes:**
- `200 OK` - Serviço está funcionando corretamente

---

### `POST /events` 🚧
*Endpoint em desenvolvimento*

Publica um evento no tópico Kafka `notifications`.

**Exemplo de requisição:**
```bash
curl -X POST http://localhost:8001/events \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "task.created",
    "user_id": "user-123",
    "payload": {
      "task_title": "Comprar leite",
      "priority": "high"
    }
  }'
```

**Resposta esperada:**
```json
{
  "status": "event published",
  "event_id": "550e8400-e29b-41d4-a716-446655440000",
  "event_type": "task.created"
}
```

---

## 📨 Formato dos Eventos

Os eventos publicados no Kafka seguem o seguinte schema JSON:

```json
{
  "event_id": "550e8400-e29b-41d4-a716-446655440000",
  "event_type": "task.created",
  "user_id": "user-123",
  "timestamp": "2024-01-15T10:30:00Z",
  "payload": {
    "task_title": "Comprar leite",
    "priority": "high",
    "due_date": "2024-01-20"
  }
}
```

### Campos Obrigatórios

- **`event_id`** (string, UUID v4): Identificador único do evento
- **`event_type`** (string): Tipo do evento (ex: `task.created`, `comment.added`, `user.updated`)
- **`user_id`** (string): ID do usuário relacionado ao evento
- **`timestamp`** (string, ISO 8601): Data e hora do evento em formato UTC
- **`payload`** (object): Dados específicos do evento (estrutura variável)

### Tipos de Eventos Sugeridos

- `task.created` - Nova tarefa criada
- `task.updated` - Tarefa atualizada
- `task.completed` - Tarefa completada
- `comment.added` - Comentário adicionado
- `user.mentioned` - Usuário mencionado
- `notification.sent` - Notificação enviada

---

## 🔧 Variáveis de Ambiente

### notification-producer-api

| Variável | Descrição | Valor Padrão |
|----------|-----------|--------------|
| `KAFKA_BROKER_URL` | URL do broker Kafka | `kafka:9092` |
| `KAFKA_BOOTSTRAP_SERVERS` | Lista de servidores Kafka | `["kafka:9092"]` |
| `MONGODB_URL` | URL de conexão do MongoDB | `mongodb://root:password@mongodb:27017` |

### Kafka

| Variável | Descrição | Valor Padrão |
|----------|-----------|--------------|
| `KAFKA_ZOOKEEPER_CONNECT` | Conexão com Zookeeper | `zookeeper:2181` |
| `KAFKA_ADVERTISED_LISTENERS` | Listeners do Kafka | `PLAINTEXT://kafka:9092,PLAINTEXT_HOST://localhost:9093` |

### MongoDB

| Variável | Descrição | Valor Padrão |
|----------|-----------|--------------|
| `MONGO_INITDB_ROOT_USERNAME` | Usuário admin | `root` |
| `MONGO_INITDB_ROOT_PASSWORD` | Senha admin | `password` |

---

## 🛠️ Comandos Úteis

### Gerenciamento de Serviços

**Parar todos os serviços:**
```bash
docker-compose down
```

**Parar e remover volumes (limpar dados):**
```bash
docker-compose down -v
```

**Reconstruir um serviço específico:**
```bash
docker-compose up --build notification-producer-api
```

**Ver logs de um serviço específico:**
```bash
docker-compose logs -f notification-producer-api
docker-compose logs -f kafka
docker-compose logs -f mongodb
docker-compose logs -f zookeeper
```

**Ver logs de todos os serviços:**
```bash
docker-compose logs -f
```

### Acesso aos Containers

**Acessar shell do container da API:**
```bash
docker exec -it notification-producer-api-service bash
```

**Acessar shell do Kafka:**
```bash
docker exec -it kafka bash
```

**Acessar MongoDB shell:**
```bash
docker exec -it mongodb_notification_system mongosh -u root -p password
```

### Kafka - Consumir Mensagens

**Consumir mensagens do tópico `notifications` (dentro do container Kafka):**
```bash
docker exec -it kafka bash
kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic notifications \
  --from-beginning
```

**Listar tópicos:**
```bash
docker exec -it kafka bash
kafka-topics.sh --list --bootstrap-server localhost:9092
```

**Criar um tópico manualmente:**
```bash
docker exec -it kafka bash
kafka-topics.sh \
  --create \
  --bootstrap-server localhost:9092 \
  --topic notifications \
  --partitions 3 \
  --replication-factor 1
```

### MongoDB - Consultas

**Listar databases:**
```bash
docker exec -it mongodb_notification_system mongosh -u root -p password --eval "show dbs"
```

**Acessar database de notificações:**
```bash
docker exec -it mongodb_notification_system mongosh -u root -p password notifications_db
```

---

## 🗺️ Roadmap

### ✅ Fase 1 - Infraestrutura Base (COMPLETO)
- [x] Setup inicial com Docker Compose
- [x] Kafka + Zookeeper configurados
- [x] MongoDB configurado
- [x] notification-producer-api com health check
- [x] Configuração de logging
- [x] Gerenciamento de configurações com Pydantic

### 🚧 Fase 2 - Producer API (EM ANDAMENTO)
- [x] Integração com Kafka Producer
- [x] Configuração de settings
- [ ] Endpoint POST /events para publicar eventos
- [ ] Validação de payloads com Pydantic models
- [ ] Geração automática de UUID para event_id
- [ ] Timestamps ISO 8601 automáticos
- [ ] Tratamento de erros e retry

### 📋 Fase 3 - Consumer Service (PLANEJADO)
- [ ] Criar serviço `notification-consumer`
- [ ] Consumir eventos do tópico `notifications`
- [ ] Processar e transformar eventos em notificações
- [ ] Salvar notificações no MongoDB
- [ ] Expor API REST para listar notificações
- [ ] Filtros e paginação

### 📋 Fase 4 - Features Avançadas (FUTURO)
- [ ] Sistema de retry para eventos falhados
- [ ] Dead Letter Queue (DLQ)
- [ ] Métricas e observabilidade (Prometheus, Grafana)
- [ ] Logging estruturado (ELK Stack)
- [ ] Autenticação e autorização (JWT)
- [ ] Rate limiting
- [ ] Testes unitários e de integração
- [ ] CI/CD pipeline
- [ ] Documentação OpenAPI/Swagger completa

---

## 🔍 Troubleshooting

### Problema: Kafka não conecta

**Sintomas:**
- Erro: `Connection refused` ou `Bootstrap server not available`
- Logs mostram tentativas de conexão falhando

**Soluções:**
1. Aguarde ~30-60 segundos após `docker-compose up` para o Kafka inicializar completamente
2. Verifique se o Zookeeper está rodando: `docker-compose ps zookeeper`
3. Verifique os logs do Kafka: `docker-compose logs kafka`
4. Certifique-se de que a variável `KAFKA_BROKER_URL` está correta

---

### Problema: notification-producer-api não sobe

**Sintomas:**
- Container para imediatamente após iniciar
- Erro de porta já em uso

**Soluções:**
1. Verifique se a porta 8001 não está em uso:
   ```bash
   lsof -i :8001
   # ou
   netstat -tulpn | grep 8001
   ```
2. Verifique os logs: `docker-compose logs notification-producer-api`
3. Reconstrua a imagem: `docker-compose up --build notification-producer-api`

---

### Problema: MongoDB não autentica

**Sintomas:**
- Erro de autenticação ao conectar
- `Authentication failed`

**Soluções:**
1. Verifique as credenciais em `docker-compose.yaml` (padrão: `root` / `password`)
2. Se alterou as credenciais, atualize a variável `MONGODB_URL` no serviço da API
3. Remova o volume e recrie:
   ```bash
   docker-compose down -v
   docker-compose up -d mongodb
   ```

---

### Problema: Erro "Kafka producer não foi inicializado"

**Sintomas:**
- RuntimeError: `Kafka producer not initialized`
- Erro ao tentar publicar evento

**Soluções:**
1. O lifespan do FastAPI gerencia a conexão automaticamente
2. Reinicie o container: `docker-compose restart notification-producer-api`
3. Verifique se o Kafka está acessível: `docker-compose logs kafka`
4. Verifique a conectividade de rede: `docker network inspect notification-producer-api_notification-network`

---

### Problema: Tópico Kafka não existe

**Sintomas:**
- Erro ao publicar: `Topic not found`

**Soluções:**
1. O tópico será criado automaticamente na primeira publicação (se `auto.create.topics.enable=true`)
2. Crie manualmente (veja seção [Comandos Úteis](#-comandos-úteis))
3. Verifique a configuração do Kafka em `docker-compose.yaml`

---

### Problema: Dependências não instalam

**Sintomas:**
- Erro durante `docker-compose build`
- `uv sync` falha

**Soluções:**
1. Verifique se o `uv.lock` está atualizado
2. Limpe o cache do Docker: `docker system prune -a`
3. Reconstrua sem cache: `docker-compose build --no-cache`

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. **Fork** o projeto
2. Crie uma **branch** para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. Abra um **Pull Request**

### Guidelines

- Siga os padrões de código existentes
- Adicione testes para novas funcionalidades
- Atualize a documentação quando necessário
- Use commits descritivos e em português

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👥 Contato / Maintainers

- **Willames Campos** - [willwjccampos@gmail.com](mailto:willwjccampos@gmail.com)

---

## 🙏 Agradecimentos

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno
- [Apache Kafka](https://kafka.apache.org/) - Message broker distribuído
- [Confluent](https://www.confluent.io/) - Plataforma Kafka
- [uv](https://github.com/astral-sh/uv) - Gerenciador de pacotes Python

---

<div align="center">

**⭐ Se este projeto foi útil para você, considere dar uma estrela! ⭐**

</div>

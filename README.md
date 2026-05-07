<<<<<<< HEAD
# knowledge-mesh-ai
Production-grade AI Retrieval Platform built with FastAPI, PostgreSQL + pgvector, semantic search, RAG pipelines, and scalable knowledge ingestion architecture.
=======
# KnowledgeMesh AI

Production-grade AI Retrieval Platform built with FastAPI, PostgreSQL + pgvector, semantic search, RAG pipelines, and scalable knowledge ingestion architecture.

---

# Overview

KnowledgeMesh AI is a backend-focused AI retrieval platform designed to evolve beyond a simple “chat with PDF” application into a scalable knowledge ingestion and semantic retrieval system.

The platform is being architected with production-grade engineering principles including:

* modular backend architecture
* semantic retrieval pipelines
* vector similarity search
* retrieval-augmented generation (RAG)
* scalable ingestion workflows
* multi-source extensibility
* future crawling/indexing pipelines
* maintainable service boundaries
* async-ready infrastructure

The goal of this project is to transition from:

> traditional backend engineering
> to
> production AI systems engineering.

---

# Core Features

## Current Features

* PDF ingestion pipeline
* Text chunking
* Semantic embeddings generation
* PostgreSQL + pgvector vector storage
* Semantic similarity retrieval
* Retrieval-Augmented Generation (RAG)
* Gemini-powered answer generation
* FastAPI backend architecture
* Layered service/repository architecture
* Alembic database migrations
* Metadata-aware chunk storage

---

## Planned Features

* Website ingestion
* Web crawling pipelines
* Scheduled indexing workflows
* Incremental re-indexing
* Multi-user architecture
* Authentication & authorization
* Streaming responses
* Chat history
* Metadata filtering
* Hybrid retrieval
* Reranking pipelines
* Background ingestion workers
* Redis caching
* Docker deployment
* Observability & monitoring
* CI/CD pipelines

---

# Architecture

```text
Frontend
   ↓
FastAPI API Layer
   ↓
Service Layer
   ↓
Repository Layer
   ↓
PostgreSQL + pgvector
```

---

# Project Structure

```text
knowledge-mesh-ai/
│
├── app/
│   ├── api/
│   │   ├── chat_routes.py
│   │   ├── ingestion_routes.py
│   │   └── auth_routes.py
│   │
│   ├── services/
│   │   ├── rag_service.py
│   │   ├── ingestion_service.py
│   │   ├── embedding_service.py
│   │   ├── retrieval_service.py
│   │   ├── llm_service.py
│   │   ├── scraper_service.py
│   │   └── chat_service.py
│   │
│   ├── repositories/
│   │   ├── document_repository.py
│   │   ├── chunk_repository.py
│   │   ├── user_repository.py
│   │   └── chat_repository.py
│   │
│   ├── models/
│   │   ├── schema.py
│   │   └── entities.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── logging_config.py
│   │   └── security.py
│   │
│   └── main.py
│
├── migrations/
├── tests/
├── scripts/
├── data/
├── requirements.txt
├── .env
└── README.md
```

---

# Tech Stack

## Backend

* Python
* FastAPI
* SQLAlchemy
* Alembic

## Database

* PostgreSQL
* pgvector

## AI Stack

* LangChain
* Hugging Face Embeddings
* Gemini LLM

## Embedding Model

* sentence-transformers/all-MiniLM-L6-v2

---

# Engineering Principles

This project emphasizes:

* clean architecture
* separation of concerns
* scalable backend design
* retrieval engineering
* maintainable abstractions
* production-ready patterns
* async-ready infrastructure
* future extensibility

The platform is intentionally designed to avoid tightly coupling logic to PDFs and instead focuses on generalized knowledge ingestion and retrieval workflows.

---

# Retrieval Pipeline

```text
Document
   ↓
Chunking
   ↓
Embedding Generation
   ↓
Vector Storage (pgvector)
   ↓
Semantic Retrieval
   ↓
Context Assembly
   ↓
LLM Response Generation
```

---

# Why This Project Exists

Most tutorials stop at:

* “chat with PDF”
* toy RAG demos
* tightly coupled scripts

This project focuses on:

* production backend architecture
* AI infrastructure thinking
* scalable retrieval systems
* maintainable engineering practices
* platform-oriented design

---

# Future Vision

KnowledgeMesh AI is being designed as a foundation for:

* enterprise knowledge retrieval
* internal AI assistants
* semantic enterprise search
* AI-powered documentation systems
* multi-source retrieval platforms
* scalable AI ingestion infrastructure

---

# Local Setup

## Clone Repository

```bash
git clone https://github.com/your-username/knowledge-mesh-ai.git
cd knowledge-mesh-ai
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/knowledge_mesh
GOOGLE_API_KEY=your_gemini_api_key
```

---

## Run Database Migrations

```bash
alembic upgrade head
```

---

## Start FastAPI Server

```bash
uvicorn app.main:app --reload
```

---

# API Documentation

After starting the server:

* Swagger UI:

```text
http://127.0.0.1:8000/docs
```

* ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# Learning Goals

This project is also a deep learning journey into:

* FastAPI ecosystem
* AI backend engineering
* retrieval systems
* vector databases
* semantic search
* RAG architecture
* scalable backend systems
* production AI infrastructure

---

# License

This project is licensed under the MIT License.
>>>>>>> d536fa34740f0162d3df77210baa9f871b8af8b6

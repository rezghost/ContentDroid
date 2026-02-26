# Content Droid

Content Droid is a distributed video-generation application composed of four main runtime components:

- `web`: a Next.js frontend where a user submits a prompt and tracks the result
- `api`: a Spring Boot service that accepts generation requests and exposes status endpoints
- `rabbitmq`: a queue that decouples request intake from long-running processing
- `processor`: a Python worker that consumes jobs, generates the output video, uploads it, and updates status in the database

The repository also includes PostgreSQL configuration for local development, container definitions, and helper scripts for building and deploying to Google Cloud.

## Architecture

The request flow is:

1. A user submits a prompt from the `web` application.
2. The `web` app calls the `api`.
3. The `api` creates a database record with `PENDING` status.
4. The `api` publishes a message to RabbitMQ.
5. The `processor` consumes the message from RabbitMQ.
6. The `processor` marks the record as `PROCESSING`.
7. The `processor` generates the video, uploads it to Google Cloud Storage, then marks the record as `COMPLETE`.
8. The `web` app polls the `api` for status and, once complete, displays the final video URL.

## Repository Layout

```text
.
├── api/                Spring Boot backend API
├── db/                 Database bootstrap SQL for local development
├── processor/          Python background worker
├── web/                Next.js frontend
├── docker-compose.yml  Local multi-service stack
├── build.sh            Image build helper for GCP
└── deploy.sh           Cloud Run deployment helper
```

## Components

### Web

Location: `web/`

The web application is a Next.js app built with React. It is the user-facing entry point for the system.

Responsibilities:

- render the prompt submission UI
- trigger video generation requests
- poll for generation status
- display the completed video or a failure state
- proxy API calls through Next.js route handlers under `web/app/api`

Key details:

- framework: Next.js 16
- UI stack: React 19, Tailwind CSS, shadcn-style components
- browser requests use same-origin `/api/*` routes so the frontend does not need to call the backend directly from the browser

Relevant files:

- [app-config.ts](/Users/alex/Dev/ContentDroid/web/lib/configurations/app-config.ts)
- [generation-service.ts](/Users/alex/Dev/ContentDroid/web/lib/services/generation-service.ts)
- `web/app/api/`

### API

Location: `api/`

The API is a Spring Boot service that handles synchronous HTTP operations.

Responsibilities:

- receive prompt submission requests
- create and read `videos` records in PostgreSQL
- publish generation jobs to RabbitMQ
- expose status and video URL endpoints for the frontend

Technology:

- Java 25
- Spring Boot 4
- Spring Data JPA
- PostgreSQL
- RabbitMQ Java client

Important behavior:

- the API should stay lightweight
- it should not generate videos directly
- its job is to validate, persist state, enqueue work, and report current status

Relevant files:

- [build.gradle](/Users/alex/Dev/ContentDroid/api/build.gradle)
- [application.yaml](/Users/alex/Dev/ContentDroid/api/src/main/resources/application.yaml)
- [GenerationService.java](/Users/alex/Dev/ContentDroid/api/src/main/java/com/rezghost/content_droid/services/GenerationService.java)

### RabbitMQ

RabbitMQ is the message broker used between the API and the processor.

Responsibilities:

- hold queued generation jobs
- decouple user-facing HTTP latency from long-running processing
- allow the processor to work independently of the API request lifecycle

Why it exists:

- video generation is slow relative to an HTTP request
- the API should respond quickly with a job ID
- the processor should be able to retry, warm up models, and process jobs asynchronously

Operational notes:

- the queue name is typically `videos`
- the API publishes to it
- the processor consumes from it
- consumer count is one of the first signals to check during debugging

Useful RabbitMQ checks:

```bash
sudo rabbitmqctl list_queues -p / name messages_ready messages_unacknowledged consumers
sudo rabbitmqctl list_consumers
sudo rabbitmqctl list_connections name peer_host user state
```

### Processor

Location: `processor/`

The processor is a Python worker that handles the expensive background work.

Responsibilities:

- consume jobs from RabbitMQ
- update database status to `PROCESSING`
- run video generation logic
- upload completed output to Google Cloud Storage
- update database status to `COMPLETE` or `FAILED`

Technology:

- Python 3.11
- `pika` for RabbitMQ
- `pg8000` plus Cloud SQL connector for database access
- Google Cloud Storage client
- the local `text2speech` package and Whisper-related dependencies

Important behavior:

- this is the component that does the actual heavy work
- it is sensitive to CPU, memory, Cloud SQL config, RabbitMQ credentials, and storage permissions
- detailed logs here are the main source of truth when generation appears stalled

Relevant files:

- [main.py](/Users/alex/Dev/ContentDroid/processor/main.py)
- [Dockerfile](/Users/alex/Dev/ContentDroid/processor/Dockerfile)
- [requirements.txt](/Users/alex/Dev/ContentDroid/processor/requirements.txt)

### PostgreSQL

PostgreSQL stores the source of truth for generation state.

Responsibilities:

- store the `videos` table and lifecycle state
- track `PENDING`, `PROCESSING`, `COMPLETE`, and `FAILED`
- store the final `storage_key` for completed videos

During local development, PostgreSQL runs through Docker Compose.

In cloud environments, the system is intended to use Cloud SQL.

## Status Model

At a high level, a video record should move through:

- `PENDING`
- `PROCESSING`
- `COMPLETE`
- `FAILED`

If a request remains stuck in `PENDING`, the likely problem is:

- API published but processor did not consume
- processor never attached to RabbitMQ
- processor failed before updating the database

If a request reaches `PROCESSING` but never completes, the likely problem is:

- generation logic is hanging
- upload failed
- processor crashed mid-job

## Local Development

### Option 1: Run the full stack with Docker Compose

From the repository root:

```bash
docker compose up --build
```

This starts:

- PostgreSQL
- RabbitMQ
- API
- processor
- web

Default local ports:

- web: `3000`
- api: `8080`
- postgres: `5432`
- rabbitmq AMQP: `5672`
- rabbitmq management: `15672`

### Option 2: Run components manually

This is useful when debugging one service at a time.

API:

```bash
cd api
./gradlew bootRun
```

Web:

```bash
cd web
npm install
npm run dev
```

Processor:

```bash
cd processor
python -u main.py
```

When running services manually, make sure the required environment variables are loaded into the shell first.

**Note:** This may not be working correctly as it's useless for debugging cloud issues

## Security Notes

Files like deployment scripts, secret directories, and environment files may be ignored locally, but they still need careful handling.

Do not commit:

- service account keys
- real `.env` files
- production passwords
- private infrastructure credentials

Rotate any credentials that were ever stored in example files or shared in logs, terminals, or screenshots.

## Comments on Current Design

This system is intentionally simple, but there are some issues:

- Processor runs on a spot VM and shuts off randomly
  - Cost saving measure since this is a side project
  - I may update this in the future
- The system design has serious design/security flaws, too many to get into here
  - There were intentionally ignored in the interest of time

Overall, this project is mostly an exercise in the viability of AI assisted coding and to test out various system design concepts

## Summary

Content Droid is a queued, asynchronous media pipeline:

- `web` is the user interface
- `api` accepts requests and reports state
- `rabbitmq` transports work between services
- `processor` performs the expensive generation work
- `postgres` stores the truth about job status

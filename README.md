Event-Driven Financial Transaction Logging System

This project implements a mandatory 3-tier/layered architecture (API, Messaging, Data) for the SENG315/451 course, focusing on an Asynchronous (Event-Driven) Microservice design for reliable financial transaction logging.

PROJECT GOAL AND ARCHITECTURE

The primary goal is to demonstrate a scalable and resilient system by utilizing Apache Kafka as a message queue, preventing direct synchronous writes to the database from the API layer.

Core Architecture: Asynchronous Flow

The system operates as a robust, non-blocking pipeline between the following components:

[API] FastAPI (Producer): Receives the transaction request (POST) and immediately sends the data to Kafka. Returns an instant 202 Accepted response.

[Messaging] Apache Kafka: Acts as the central event broker, securely holding the transaction message in a queue.

[Worker] Python Consumer: Continuously monitors the Kafka queue, processes the message, and performs the heavy database operation.

[Data] PostgreSQL & SQLAlchemy: Provides persistent data management using an Object-Relational Mapper (ORM).

TECHNOLOGIES AND LAYERS

Layer

Technology

Description

API Layer

Python FastAPI & Pydantic

Provides the RESTful interface, handles request validation, and acts as the Kafka Producer.

Messaging Layer

Apache Kafka

Ensures asynchronous, high-throughput, and fault-tolerant communication between services.

Data Layer

PostgreSQL & SQLAlchemy

SQL database engine and ORM used for persistent storage and data query (read operations).

Simulation

Pandas & Requests

Used to read CSV data and simulate realistic high-volume transaction traffic to the API.

Infrastructure

Docker & Docker Compose

Manages, isolates, and orchestrates all 5 services (API, Worker, Kafka, Zookeeper, DB).

⚙️ SETUP AND EXECUTION

Prerequisites

Docker Desktop: Must be installed and running.

paysim.csv: The simulation dataset file must be present in the project's root directory.

Python Code: Ensure main.py, worker.py, database.py, and seed_data.py are present.

Step-by-Step Execution

Build and Start All Services: This command builds the Python image and starts all 5 containers (Postgres, Zookeeper, Kafka, API, Worker).

docker-compose up --build -d


Seed the Database (Initial Data): Load the initial 100 transactions from the CSV into PostgreSQL.

docker-compose exec api python seed_data.py


Attach the Worker: Start the consumer process which listens to Kafka and writes to the DB.

docker-compose exec worker python worker.py


(Note: Use docker-compose logs -f worker in a separate terminal to view the process logs in real-time.)

TESTING SCENARIOS

The API automatically exposes interactive documentation via Swagger UI.

1. Read/Reporting Control (Data Layer Validation)

Tests the Data Layer's ability to be queried directly (Synchronous read operation).

Action

Command / URL

Expected Result

View Report

GET on http://localhost:8000/reports

A list of 100 transactions with status: Historical (from seed_data.py) must be displayed.

2. Live Transaction Flow (Asynchronous POST Test)

Tests the core Event-Driven Pipeline (API ➡️ Kafka ➡️ Worker ➡️ DB).

Step

Action

Observation

Expected Result

A. Send Request

Use Swagger UI (POST /transaction) and send valid JSON data.

API Logs (Terminal)

Must return a non-blocking 202 Accepted status immediately.

B. Process

Wait 3-5 seconds.

Worker Logs

Must show Mesaj Yakalandı and ✅ DB'ye Kaydedildi! logs.

C. Verify

Re-run GET /reports.

Browser

The newly posted transaction must appear with status: Completed.

3. High-Volume Simulation (Optional)

Run the simulation script to test Kafka's queueing and the Worker's parallel processing capabilities.

python simulate.py


(Observe the Worker log window: Transactions should be processed sequentially and recorded successfully.)

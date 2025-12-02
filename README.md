# Event-Driven Financial Transaction Logging System

This project is an **event-driven, asynchronous financial transaction logging system** built with **FastAPI**, **Apache Kafka**, and **PostgreSQL**.  
It consists of three main components:

- **API Service (FastAPI Producer):** Receives transactions and publishes Kafka events.  
- **Kafka Messaging Layer:** Queues events for asynchronous processing.  
- **Worker Service (Python Consumer):** Consumes messages from Kafka and writes to PostgreSQL.

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker Desktop**
- **Python 3.10+** (only needed if running the simulation manually)
- **paysim.csv** dataset placed in the project root directory

---

## Getting Started

### Clone the Repository

```bash
git clone <repository-url>
cd seng315
  Configure Environment & Database
All database and Kafka configurations are handled inside Docker Compose and database.py.

Your PostgreSQL connection string (internal Docker network) must be:

python
coppied code
# database.py
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgres:5432/financedb"
Make sure the following files exist in the root directory:

main.py (API Producer)

worker.py (Kafka Consumer)

database.py

seed_data.py

docker-compose.yml

paysim.csv

  Running the Application
1 Start Infrastructure
Starts all required services: Postgres, Zookeeper, Kafka, API, Worker.

bash
coppied code
docker-compose up --build -d
2 Seed Initial Data
Loads 100 initial transactions into the PostgreSQL database.

bash
coppied code
docker-compose exec api python seed_data.py
3️ Start the Worker (Kafka Consumer)
bash
coppied code
docker-compose exec worker python worker.py
(You can run the logs in another terminal:)

bash
coppied code
docker-compose logs -f worker
  Testing
  1. Read/Reporting Test
Tests the synchronous reporting endpoint from the database.

Open in browser:

bash
coppied code
GET http://localhost:8000/reports
Expected Output:

A list of 100 historical transactions loaded by seed_data.py.

  2. Asynchronous Transaction Flow Test
Open Swagger UI:

bash
coppied code
http://localhost:8000/docs
Send a POST request to /transaction.

Expected Behavior:

Step	Layer	Expected Result
A. Send POST	API Layer	Returns 202 Accepted instantly (non-blocking).
B. Worker	Kafka Consumer	Logs: “Message Received” and “DB Committed”.
C. Verify	Reporting	New transaction appears as Completed.

  3. High-Volume Simulation (Optional)
To simulate large amounts of traffic using the CSV file:

bash
coppied code
python simulate.py
Expected:

Worker processes messages continuously

All records are saved to PostgreSQL

  Architecture
API Layer (FastAPI)
Receives requests

Validates data

Publishes events to Kafka immediately

Messaging Layer (Apache Kafka)
High-throughput event delivery

Persistent message queue

Fault-tolerant design

Worker Layer (Python Consumer)
Listens to Kafka topic

Processes incoming messages

Performs database writes

Data Layer (PostgreSQL + SQLAlchemy)
Stores all historical and completed transactions

Used for report/read queries

Infrastructure (Docker Compose)
Orchestrates all services

Handles networking and container management

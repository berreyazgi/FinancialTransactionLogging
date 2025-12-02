#Event-Driven Financial Transaction Logging System

This project is an event-driven, asynchronous financial transaction logging system built with FastAPI, Apache Kafka, and PostgreSQL.

It consists of three main components:

API Service (FastAPI Producer): Receives transactions and publishes Kafka events.

Kafka Messaging Layer: Queues events for asynchronous processing.

Worker Service (Python Consumer): Consumes messages from Kafka and writes to PostgreSQL.

Prerequisites

Before you begin, ensure you have the following installed:

Docker Desktop

Python 3.10+ (only needed if you will simulate traffic manually)

paysim.csv dataset placed in the project root directory

Getting Started

1. ##Clone the Repository

git clone <repository-url>
cd seng315


2. ##Configure Environment & Database

All database and Kafka configurations are managed inside Docker Compose and database.py.

Your PostgreSQL connection string (internal Docker network) must be:

# database.py
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgres:5432/financedb"


The following files must exist in the root directory:

main.py (API Producer)

worker.py (Kafka Consumer)

database.py

seed_data.py

docker-compose.yml

paysim.csv

Running the Application

1. ##Start Infrastructure

Starts all required services: Postgres, Zookeeper, Kafka, API, Worker.

docker-compose up --build -d


2. ##Seed Initial Data

Seeds the database with 100 initial transactions for reporting tests.

docker-compose exec api python seed_data.py


3.  ##Start the Worker (Kafka Consumer)

docker-compose exec worker python worker.py


(You can also run docker-compose logs -f worker in another terminal to follow real-time logs.)

#Testing

1. ##Read/Reporting Test

Tests the synchronous reporting endpoint from the database.

Open:

GET http://localhost:8000/reports


Expected Output: A list of 100 historical transactions loaded by seed_data.py.

2. ##Asynchronous Transaction Flow Test

Go to Swagger UI:

http://localhost:8000/docs


Send a POST request to /transaction.

Step

 #Layer

Expected Result

A.  ##Send POST

 ##API Layer

Returns 202 Accepted instantly (non-blocking).

B.  ##Worker

 ##Kafka Consumer

Logs: “Message Received” and “DB Committed”.

C. ##Verify

Reporting

New transaction appears as Completed.

3. ##Event-Driven Financial Transaction Logging System

This project is an event-driven, asynchronous financial transaction logging system built with FastAPI, Apache Kafka, and PostgreSQL.

It consists of three main components:

API Service (FastAPI Producer): Receives transactions and publishes Kafka events.

Kafka Messaging Layer: Queues events for asynchronous processing.

Worker Service (Python Consumer): Consumes messages from Kafka and writes to PostgreSQL.

#Prerequisites

Before you begin, ensure you have the following installed:

Docker Desktop

Python 3.10+ (only needed if you will simulate traffic manually)

paysim.csv dataset placed in the project root directory

Getting Started

1. ##Clone the Repository

git clone <repository-url>
cd seng315


2. ##Configure Environment & Database

All database and Kafka configurations are managed inside Docker Compose and database.py.

Your PostgreSQL connection string (internal Docker network) must be:

# database.py
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgres:5432/financedb"


The following files must exist in the root directory:

main.py (API Producer)

worker.py (Kafka Consumer)

database.py

seed_data.py

docker-compose.yml

paysim.csv

Running the Application

1. ##Start Infrastructure

Starts all required services: Postgres, Zookeeper, Kafka, API, Worker.

docker-compose up --build -d


2. ##Seed Initial Data

Seeds the database with 100 initial transactions for reporting tests.

docker-compose exec api python seed_data.py


3. ##Start the Worker (Kafka Consumer)

docker-compose exec worker python worker.py


(You can also run docker-compose logs -f worker in another terminal to follow real-time logs.)

#Testing

1.  ##Read/Reporting Test

Tests the synchronous reporting endpoint from the database.

Open:

GET http://localhost:8000/reports


Expected Output: A list of 100 historical transactions loaded by seed_data.py.

2.  ##Asynchronous Transaction Flow Test

Go to Swagger UI:

http://localhost:8000/docs


Send a POST request to /transaction.

Step

Layer

Expected Result

A.  ##Send POST

  #API Layer

Returns 202 Accepted instantly (non-blocking).

B. ##Worker

 #Kafka Consumer

Logs: “Message Received” and “DB Committed”.

C. ##Verify

Reporting

New transaction appears as Completed.

3. ##High-Volume Simulation (Optional)

If you want to simulate heavy API traffic using the CSV file:

python simulate.py


You should see the Worker processing messages continuously and recording them in PostgreSQL.

Architecture

API (FastAPI): Receives requests and immediately publishes events to Kafka.

Messaging (Apache Kafka): Handles high-throughput, persistent, fault-tolerant message delivery.

Worker (Python Consumer): Listens to Kafka, processes events, and performs DB writes.

Data Layer (PostgreSQL + SQLAlchemy): Used for persistent storage and read/report operations.

Infrastructure (Docker Compose): Orchestrates all containers and internal networking.High-Volume Simulation (Optional)

If you want to simulate heavy API traffic using the CSV file:

python simulate.py


You should see the Worker processing messages continuously and recording them in PostgreSQL.

Architecture

##API (FastAPI): Receives requests and immediately publishes events to Kafka.

##Messaging (Apache Kafka): Handles high-throughput, persistent, fault-tolerant message delivery.

##Worker (Python Consumer): Listens to Kafka, processes events, and performs DB writes.

##Data Layer (PostgreSQL + SQLAlchemy): Used for persistent storage and read/report operations.

##Infrastructure (Docker Compose): Orchestrates all containers and internal networking.

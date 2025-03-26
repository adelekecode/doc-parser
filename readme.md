# Pitch Deck Parser API

## Overview

This project is a **Flask-based web application** that allows users to upload pitch deck documents ( **PDF or PowerPoint** ). The uploaded documents are parsed to extract slide information and metadata, which is then stored in  **MongoDB** . The system utilizes **RabbitMQ** for asynchronous processing and **Redis** for caching document retrieval.

## Features

* **File Upload** : Users can upload PDF or PPTX files.
* **Asynchronous Processing** : Uploaded files are queued in **RabbitMQ** for background processing.
* **Document Parsing** : Extracts slide titles, text content, and metadata using **PyPDF2** for PDFs and **python-pptx** for PowerPoint files.
* **Data Storage** : Extracted data is stored in  **MongoDB** .
* **Document Retrieval** : Users can fetch uploaded documents, with Redis caching enabled for quick access.
* **Health Check Endpoint** : Simple API to verify the service is running.

---

## System Architecture

The project follows a **microservices architecture** with the following components:

* **API Service** : Handles user requests (uploading, retrieving documents).
* **Parser Service** : Processes uploaded documents asynchronously.
* **MongoDB** : Stores parsed document data.
* **Redis** : Caches frequently accessed documents.
* **RabbitMQ** : Message broker for background processing.
* **Nginx** : Reverse proxy for handling API requests.

---

## Technologies Used

* **Flask** (Python Web Framework)
* **MongoDB** (NoSQL Database)
* **Redis** (Caching Layer)
* **RabbitMQ** (Message Queue)
* **Docker & Docker Compose** (Containerization)
* **Nginx** (Reverse Proxy)
* **PyPDF2** & **python-pptx** (Document Parsing)

---

## Installation & Setup

### Prerequisites

Ensure you have the following installed:

* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

### Clone Repository

```sh
git clone https://github.com/adelekecode/doc-parser.git
cd doc-parser
```

### Environment Variables

Create a `.env` file in the project root with the following:

```env
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY="random-secret-keys"
PORT=5000
UPLOAD_FOLDER=/documents

# MongoDB Configuration
MONGO_URI=mongodb://mongo:27017/pitch_deck_parser

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# RabbitMQ Configuration
RABBITMQ_HOST=doc-parser-rabbitmq-1
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASS=guest

```

---

## Running the Project

### Start Services

Run the following command to start all services:

```sh
docker-compose up --build -d
```

This will:

* Build the **API Service**
* Build the **Parser Service**
* Start  **MongoDB** ,  **Redis** , and **RabbitMQ**
* Start **Nginx** as a reverse proxy

### Verify Running Containers

```sh
docker ps
```

You should see the following services running:

* **api** (Flask backend)
* **parser** (Background processing)
* **mongo** (Database)
* **redis** (Cache)
* **rabbitmq** (Message queue)
* **nginx** (Reverse proxy)

---

## Project Host

```
curl -I http://0.0.0.0:5000/api/v1

```

## API Endpoints

### 1. Health Check

**Check if the API is running**

```sh
GET /health/
```

**Response:**

```json
{
  "status": "ok"
}
```

### 2. Upload a Document

**Endpoint to upload a document (PDF/PPTX)**

```sh
POST /upload/
```

**Request:** (Multipart Form Data)

```sh
curl -X POST http://localhost/upload/ \
  -F "file=@path/to/document.pdf"
```

**Response:**

```json
{
  "message": "Document uploaded successfully and queued for processing",
  "document_id": "b1234f56-7890-1234-abcd-567890efghij",
  "filename": "document.pdf"
}
```

### 3. Retrieve All Documents

**Get a list of all uploaded documents (sorted by most recent first)**

```sh
GET /documents/
```

**Response:**

```json
[
  {
  "document_id": "b1234f56-7890-1234-abcd-567890efghij",
  "original_filename": "document.pdf",
  "file_path": "/documents/cca7164f-b145-4cdf-9539-4ae9c5ad5ce7.pdf",
  "file_type": "pdf"
  "upload_timestamp": {
	"$date": "2025-03-26T18:26:18.335Z"
   },
  "total_slides": 10,
  "slides": [...],
  "metadata": {...}
}

]
```

### 4. Retrieve a Specific Document

**Fetch document details (cached in Redis)**

```sh
GET /documents/<document_id>/
```

**Response:**

```json
{
  "document_id": "b1234f56-7890-1234-abcd-567890efghij",
  "original_filename": "document.pdf",
  "file_path": "/documents/cca7164f-b145-4cdf-9539-4ae9c5ad5ce7.pdf",
  "file_type": "pdf"
  "upload_timestamp": {
	"$date": "2025-03-26T18:26:18.335Z"
   },
  "total_slides": 10,
  "slides": [...],
  "metadata": {...}
}
```

### 5. Download an Uploaded File

**Access uploaded files directly**

```sh
GET /documents/<filename>
```

---

## Stopping the Project

To stop the running containers:

```sh
docker-compose down
```

---

## Deployment

For production, ensure that:

* The `.env` file contains  **secure credentials** .
* Persistent **volumes** are configured for MongoDB and RabbitMQ.
* The `nginx.conf` is optimized for load balancing.

---

## Troubleshooting

### Check Logs

To view logs for a specific service:

```sh
docker-compose logs -f api
```

### Restart a Service

If a service crashes, restart it using:

```sh
docker-compose restart api
```

---

## License

This project is licensed under the MIT License.

---

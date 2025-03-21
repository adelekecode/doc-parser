
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a worker script
RUN echo '#!/usr/bin/env python\n\
import os\n\
import json\n\
import pika\n\
from app import create_app\n\
from app.services.document_parser import DocumentParser\n\
from app.db.models import save_document_data\n\
from app.utils.exceptions import UnsupportedFileError, ParsingError\n\
\n\
app = create_app(os.getenv("FLASK_ENV", "default"))\n\
app_context = app.app_context()\n\
app_context.push()\n\
\n\
def callback(ch, method, properties, body):\n\
    message = json.loads(body)\n\
    document_id = message["document_id"]\n\
    file_path = message["file_path"]\n\
    file_extension = message["file_extension"]\n\
    original_filename = message["original_filename"]\n\
    \n\
    try:\n\
        # Parse the document\n\
        parser = DocumentParser()\n\
        doc_data = parser.parse(file_path, file_extension)\n\
        \n\
        # Save data to database\n\
        doc_metadata = {\n\
            "document_id": document_id,\n\
            "original_filename": original_filename,\n\
            "file_path": file_path\n\
        }\n\
        save_document_data(doc_metadata, doc_data)\n\
        print(f"Processed document {document_id}")\n\
    except Exception as e:\n\
        print(f"Error processing document {document_id}: {str(e)}")\n\
    finally:\n\
        ch.basic_ack(delivery_tag=method.delivery_tag)\n\
\n\
# Connect to RabbitMQ\n\
connection = pika.BlockingConnection(\n\
    pika.ConnectionParameters(\n\
        host=app.config["RABBITMQ_HOST"],\n\
        port=app.config["RABBITMQ_PORT"],\n\
        credentials=pika.PlainCredentials(\n\
            app.config["RABBITMQ_USER"],\n\
            app.config["RABBITMQ_PASS"]\n\
        )\n\
    )\n\
)\n\
channel = connection.channel()\n\
\n\
# Declare queue\n\
channel.queue_declare(queue="document_processing", durable=True)\n\
\n\
# Set up consumer\n\
channel.basic_qos(prefetch_count=1)\n\
channel.basic_consume(queue="document_processing", on_message_callback=callback)\n\
\n\
print("Parser worker started. Waiting for messages...")\n\
channel.start_consuming()\n' > worker.py

RUN chmod +x worker.py

# Run the worker
CMD ["python", "worker.py"]


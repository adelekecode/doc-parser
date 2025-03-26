import os
import uuid
from flask import request, jsonify, current_app, send_from_directory

from werkzeug.utils import secure_filename
from app.api import api_bp
from app.services.document_parser import DocumentParser
from app.db.models import save_document_data
from app.utils.exceptions import UnsupportedFileError, ParsingError
import pika
import json
from datetime import timedelta




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']





@api_bp.route('/health/', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200




@api_bp.route('/uploads/<filename>', methods=['GET'])
def get_uploaded_file(filename):

    ## Would allow users access uploaded files, directly from path
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)




@api_bp.route('/upload/', methods=['POST'])
def upload_document():

    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Secure filename and generate a unique ID for the document
        document_id = str(uuid.uuid4())
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        
        # Create upload folder if it doesn't exist
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Save file to disk
        filename = f"{document_id}.{file_extension}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Send message to queue for asynchronous processing
        try:
            # Connect to RabbitMQ
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=current_app.config['RABBITMQ_HOST'],
                    port=current_app.config['RABBITMQ_PORT'],
                    credentials=pika.PlainCredentials(
                        current_app.config['RABBITMQ_USER'], 
                        current_app.config['RABBITMQ_PASS']
                    )
                )
            )
            channel = connection.channel()
            
            # Declare queue
            channel.queue_declare(queue='document_processing', durable=True)
            
            # Prepare message
            message = {
                'document_id': document_id,
                'file_path': file_path,
                'original_filename': original_filename,
                'file_extension': file_extension
            }
            
            # Publish message
            channel.basic_publish(
                exchange='',
                routing_key='document_processing',
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                )
            )
            
            connection.close()
            
            return jsonify({
                'message': 'Document uploaded successfully and queued for processing',
                'document_id': document_id,
                'filename': original_filename
            }), 202
            
        except Exception as e:
            # In case of queue connection error, process synchronously
            try:
                # Parse the document
                parser = DocumentParser()
                doc_data = parser.parse(file_path, file_extension)
                
                # Save data to database
                doc_metadata = {
                    'document_id': document_id,
                    'original_filename': original_filename,
                    'file_path': file_path
                }
                save_document_data(doc_metadata, doc_data)
                
                return jsonify({
                    'message': 'Document uploaded and processed successfully',
                    'document_id': document_id,
                    'filename': original_filename
                }), 201
                
            except UnsupportedFileError as e:
                # Clean up the file
                if os.path.exists(file_path):
                    os.remove(file_path)
                    
                return jsonify({'error': str(e)}), 415
                
            except ParsingError as e:
                # Clean up the file
                if os.path.exists(file_path):
                    os.remove(file_path)
                return jsonify({'error': str(e)}), 422
                
            except Exception as e:
                # Clean up the file
                if os.path.exists(file_path):
                    os.remove(file_path)
                return jsonify({'error': f'An error occurred: {str(e)}'}), 500
    
    return jsonify({'error': 'File type not allowed'}), 415

@api_bp.route('/documents', methods=['GET'])
def get_documents():
    from app import mongo
    # Get documents from MongoDB
    documents = list(mongo.db.documents.find({}, {'_id': 0}))
    return jsonify(documents), 200

@api_bp.route('/documents/<document_id>', methods=['GET'])
def get_document(document_id):
    from app import mongo, redis_client
    
    # Try to get from cache first
    cached_doc = redis_client.get(f"document:{document_id}")
    if cached_doc:
        return jsonify(json.loads(cached_doc)), 200
    
    # Get from MongoDB if not in cache
    document = mongo.db.documents.find_one({'document_id': document_id}, {'_id': 0})
    if not document:
        return jsonify({'error': 'Document not found'}), 404
    
    # Cache the document for future requests
    redis_client.setex(
        f"document:{document_id}", 
        timedelta(minutes=30),  # Cache for 30 minutes
        json.dumps(document)
    )
    
    return jsonify(document), 200

import datetime
from app import mongo




def save_document_data(document_metadata, document_data):
    """
    Save document metadata and parsed data to MongoDB
    
    Args:
        document_metadata (dict): Metadata about the document
        document_data (dict): Parsed data from the document
        
    Returns:
        str: The document ID
    """
    now = datetime.datetime.utcnow()
    
    document = {
        'document_id': document_metadata['document_id'],
        'original_filename': document_metadata['original_filename'],
        'file_path': document_metadata['file_path'],
        'file_type': document_metadata['original_filename'].rsplit('.', 1)[1].lower(),
        'upload_timestamp': now,
        'total_slides': document_data['total_slides'],
        'slides': document_data['slides'],
        'metadata': document_data['metadata']
    }
    
    result = mongo.db.documents.insert_one(document)
    return document['document_id']

def get_document_by_id(document_id):
    """
    Retrieve a document by its ID
    
    Args:
        document_id (str): The document ID
        
    Returns:
        dict: The document data or None if not found
    """
    document = mongo.db.documents.find_one({'document_id': document_id}, {'_id': 0})
    return document





def get_all_documents():
    """
    Retrieve all documents
    
    Returns:
        list: List of documents
    """
    documents = list(mongo.db.documents.find({}, {'_id': 0}))


    return documents
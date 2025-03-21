
from app.services.pdf_parser import PDFParser
from app.services.pptx_parser import PPTXParser
from app.utils.exceptions import UnsupportedFileError, ParsingError



class DocumentParser:



    def __init__(self):
        
        self.parsers = {
            'pdf': PDFParser(),
            'pptx': PPTXParser()
        }
    
    def parse(self, file_path, file_extension):
        """
        Parse the document based on its extension
        
        Args:
            file_path (str): Path to the document file
            file_extension (str): Extension of the file (pdf or pptx)
            
        Returns:
            dict: Extracted data from the document
            
        Raises:
            UnsupportedFileError: If the file extension is not supported
            ParsingError: If there's an error during parsing
        """
        if file_extension not in self.parsers:
            raise UnsupportedFileError(f"Unsupported file format: {file_extension}")
        
        try:
            return self.parsers[file_extension].parse(file_path)
        except Exception as e:
            raise ParsingError(f"Error parsing {file_extension.upper()} document: {str(e)}")

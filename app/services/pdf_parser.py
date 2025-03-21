import PyPDF2
import re
import os
from app.utils.exceptions import ParsingError

class PDFParser:
    def parse(self, file_path):
        """
        Parse PDF document and extract relevant information
        
        Args:
            file_path (str): Path to the PDF file
            
        Returns:
            dict: Extracted data from the PDF
            
        Raises:
            ParsingError: If there's an error during parsing
        """
        if not os.path.exists(file_path):
            raise ParsingError(f"File not found: {file_path}")
        
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)
                
                # Extract document metadata
                metadata = {}
                if reader.metadata:
                    for key, value in reader.metadata.items():
                        if key.startswith('/'):
                            metadata[key[1:]] = value
                
                # Extract content from each page/slide
                slides = []
                for i in range(num_pages):
                    page = reader.pages[i]
                    text = page.extract_text()
                    
                    # Try to extract title (first line or first sentence)
                    title = None
                    if text:
                        lines = text.split('\n')
                        if lines:
                            title = lines[0].strip()
                            # Limit title length
                            if len(title) > 100:
                                title = title[:97] + "..."
                    
                    # Check for images (simple heuristic based on if the page has XObject)
                    has_images = '/XObject' in page.get_object() if hasattr(page, 'get_object') else False
                    
                    # Check for charts (simple heuristic - look for words like "chart", "graph", "figure")
                    has_charts = bool(re.search(r'chart|graph|figure|diagram', text.lower())) if text else False
                    
                    slides.append({
                        'slide_number': i + 1,
                        'title': title,
                        'content': text,
                        'has_images': has_images,
                        'has_charts': has_charts
                    })
                
                return {
                    'total_slides': num_pages,
                    'slides': slides,
                    'metadata': metadata
                }
                
        except Exception as e:
            raise ParsingError(f"Error parsing PDF: {str(e)}")

class UnsupportedFileError(Exception):
    """Raised when the file format is not supported"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Unsupported file format: {self.message}"
   

class ParsingError(Exception):
    """Raised when there's an error during parsing"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Error parsing document: {self.message}"

class DatabaseConnectionError(Exception):
    """Raised when there's an error connecting to the database"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Database connection error: {self.message}"
    
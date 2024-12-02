from log_message import LogMessage
from log_appender import LogAppender

class FileAppender(LogAppender):
    
    def __init__(self, path):
        self.file_path = path
    
    def append(self, message: LogMessage):
        with open(self.file_path, "a") as log_file:
            log_file.write(str(message))

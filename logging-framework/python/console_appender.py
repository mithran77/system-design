from log_message import LogMessage
from log_appender import LogAppender

class ConsoleAppender(LogAppender):

    def append(self, message: LogMessage):
        print(message)

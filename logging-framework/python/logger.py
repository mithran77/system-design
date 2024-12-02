from logger_config import LoggerConfig
from console_appender import ConsoleAppender
from log_message import LogMessage
from log_level import LogLevel

class Logger:
    _instance = None

    def __init__(self):
        if Logger._instance is not None:
            raise("Logger is a Singleton")
        else:
            Logger._instance = self
            self.config = LoggerConfig(LogLevel.DEBUG, ConsoleAppender())
    
    @staticmethod
    def get_instance():
        if Logger._instance is None:
            Logger()
        return Logger._instance

    def set_config(self, config):
        self.config = config

    def log(self, level, message):
        if self.config.get_level().value <= level.value:
            log_message = LogMessage(level, message)
            self.config.get_appender().append(log_message)

    def debug(self, message):
        self.log(LogLevel.DEBUG, message)

    def info(self, message):
        self.log(LogLevel.INFO, message)

    def warn(self, message):
        self.log(LogLevel.WARNING, message)

    def error(self, message):
        self.log(LogLevel.ERROR, message)

    def fatal(self, message):
        self.log(LogLevel.FATAL, message)

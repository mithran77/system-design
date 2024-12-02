class LoggerConfig:
    def __init__(self, level, appender):
        self.level = level
        self.log_appender = appender

    def get_level(self):
        return self.level

    def set_level(self, level):
        self.level = level

    def get_appender(self):
        return self.log_appender

    def set_appender(self, appender):
        self.log_appender = appender

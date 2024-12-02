from log_message import LogMessage
from log_appender import LogAppender
import psycopg2

class DatabaseAppender(LogAppender):
    def __init__(self, username, password, db_url):
        self.username = username
        self.pasword = password
        self.db_url = db_url

    def append(self, message: LogMessage):
        try:
            connection = psycopg2.connect(self.db_url, self.username, self.password)
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO logs (level, message, timestamp) VALUES (%s, %s, %s)",
                (message.get_level(), message.get_message(), message.get_timestamp())
            )
            connection.commit()
            cursor.close()
            connection.close()

        except psycopg2.Error as e:
            print(f"Error: {e}")

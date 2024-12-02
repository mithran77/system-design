from subscriber import Subscriber

class PrintSubscriber(Subscriber):
    def __init__(self, name):
        self.name = name

    def on_message(self, message):
        print(f"Received message {message.get_content()}")

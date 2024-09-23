# SOLID Refresher

## 1. Single Responsibility

> A class should have one, and only one, reason to change.

If it has a single responsibility it will have small sets of related member variables and methods, making maintaince easier and reducing the chance of bugs due to complex method interdepencies.

```
class UserManager:
    def authenticate_user(self, username, password):
        # Authentication logic

    def update_user_profile(self, user_id, new_profile_data):
        # Profile update logic

    def send_email_notification(self, user_email, message):
        # Send email logic
```

UserManager could be split into 3 different classes, each handling specific responsibilities.

```
class UserManager:
    def authenticate_user(self, username, password):
        # Authentication logic

class UserProfileManager:
    def update_user_profile(self, user_id, new_profile_data):
        # Profile update logic

class EmailNotificationManager:
    def send_email_notification(self, user_email, message):
        # Send email logic
```

## 2. Open Close

> Software entities (classes, modules, functions, etc.) should be open for extension, but closed for modification.

Software entities should be designed such that in order to introduce new functionality we should be able to add new code without modifying existing code, primarily because changing existing code increases the chances of introducing bugs.

```
class ShapeCalculator:
    def calculate_area(shape):
        if shape.type == "Rectangle":
            return shape.width * shape.height
        if shape.type == "Circle"
            return 3.14 * shape.radius * shape.radius

    def calculate_perimeter(shape):
        if shape.type == "Rectangle":
            return 2 * (shape.width + shape.height)
        if shape.type == "Circle"
            return 2 * 3.14 * shape.radius
```
Can be improved by defining a Shape interface and defining each shape as a concrete class implementing the Shape interface.
```
from abc import abstractmethod, ABC

class Shape(ABC):
    @abstractmethod
    def area(self):
        raise NotImplementedError

    @abstractmethod
    def perimeter(self):
        raise NotImplementedError

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius * self.radius

    def perimeter(self):
        return 2 * 3.14 * self.radius
```

## 3. Liskov Substitution
> Objects of a superclass should be replaceable with objects of its subclasses without affecting the correctness of the program.

This means, if there is a base class and multiple derived classes, you should be able to substitute anywhere that expects the base class, with an instance of any of the derived classes and it should not break the program.
```
class Vehicle:
    def start_engine(self):
        raise NotImplementedError

class Car(Vehicle):
    def start_engine(self):
        print("Starting engine!")

class Cycle(Vehicle):
    def start_engine(self):
        # Invalid because cycle has no engine
        pass
```
start_engine() could be changed to a more generic start(), that would be better suited across all derived classes.
```
class Vehicle:
    def start(self):
        raise NotImplementedError

class Car(Vehicle):
    def start(self):
        print("Starting engine!")

class Cycle(Vehicle):
    def start(self):
        print("Starting pedaling!")
```

## 4. Interface Segregration
> No client should be forced to depend on interfaces they don't use

Interfaces should be generic enough and decomposed such that no users of the interface should need to implement some methods but not others.
```
class MediaPlayer:
    def play_audio(self, audio_file):
        raise NotImplementedError

    def play_video(self, video_file):
        raise NotImplementedError

    def stop_audio(self):
        raise NotImplementedError

    def stop_video(self):
        raise NotImplementedError

    def adjust_audio_volume(self, volume):
        raise NotImplementedError

    def adjust_video_brightness(self, brightness):
        raise NotImplementedError
```
we could segregate MediaPlayer interface into AudioPlayer and VideoPlayer, allowing for concrete classes implementing either of the interfaces or both.
```
class AudioPlayer:
    def play_audio(self, audio_file):
        raise NotImplementedError

    def stop_audio(self):
        raise NotImplementedError

    def adjust_audio_volume(self, volume):
        raise NotImplementedError

class VideoPlayer:
    def play_video(self, video_file):
        raise NotImplementedError

    def stop_video(self):
        raise NotImplementedError

    def adjust_video_brightness(self, brightness):
        raise NotImplementedError

class MP3Player(AudioPlayer):
    def play_audio(self, audio_file):
        # Play mp3 audio

    def stop_audio(self):
        # Stop audio playing

    def adjust_audio_volume(self, volume):
        # Adjust volume

class AviVideoPlayer(VideoPlayer):
    def play_video(self, video_file):
        # Play avi video

    def stop_video(self):
        # Stop video playing

    def adjust_video_brightness(self, brightness):
        # Adjust video brightness

class MultimediaPlayer(AudioPlayer, VideoPlayer):
    # Implements methods for both AudioPlayer and VideoPlayer interfaces
```

## 5. Dependency Inversion
> High-level modules should not depend on Low-level modules, both should depend on abstractions

We would like to have the high-level modules depend on interfaces rather than concrete classes. This makes the code more reusaable.

```
class GmailClient:
    def send_email(self, recepient, subject, body):
        # Logic to send email using gmail API

class EmailService:
    def __init__(self):
        self.client = GmailClient()
    
    def send_email(self, recepient, subject, body):
        self.client.send_email(recepient, subject, body)
```
Here EmailService is tightly coupled with GmailClient, this is a violation of DIP.
We can introduce a new interface EmailClient, that EmailService depends on. Also low-level classes GmailClient and OutlookClient depend on the EmailClient interface.
```
class EmailClient:
    def send_email(self, recepient, subject, body):
        raise NotImplementedError

class GmailClient(EmailClient):
    def send_email(self, recepient, subject, body):
        # Logic to send email using Gmail API

class OutlookClient(EmailClient):
    def send_email(self, recepient, subject, body):
        # Logic to send email using Outlook API

class EmailService:
    def __init__(self, client):
        self.client = client

    def send_email(self, recepient, subject, body):
        self.client.send_email(recepient, subject, body)

#
gmail_client = GmailClient()
email_service = EmailService(gmail_client)
email_service.send_email(...)
```

#### Additional Resources:
1. https://medium.com/backticks-tildes/the-s-o-l-i-d-principles-in-pictures-b34ce2f1e898


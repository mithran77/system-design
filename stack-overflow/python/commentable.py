from abc import abstractmethod
from comment import Comment

class Commentable:
    @abstractmethod
    def add_comment(self, comment: Comment):
        pass

    @abstractmethod
    def get_comments(self):
        pass

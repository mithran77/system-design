from datetime import datetime

from comment import Comment
from vote import Vote
from votable import Votable
from commentable import Commentable


class Answer(Votable, Commentable):
    
    def __init__(self, author, question, content):
        self.id = id(self)
        self.author = author
        self.question = question
        self.content = content
        self.creation_date = datetime.now()
        self.votes = []
        self.comments = []
        self.is_accepted = False

    def vote(self, user, value: int):
        if value not in [1, -1]:
            raise ValueError("Vote value must be +1 or -1")
        self.votes = [v for v in self.votes if v.user != user]
        self.votes.append(Vote(user, value))
        self.author.update_reputation(value * 10)

    def get_vote_count(self):
        cnt = 0
        for v in self.votes:
            cnt += v.value
        return cnt

    def add_comment(self, comment: Comment):
        self.comments.append(comment)

    def get_comments(self):
        return self.comments.copy()

    def accept(self):
        if self.is_accepted:
            raise ValueError("Answer must not already be accepted")
        self.is_accepted = True
        self.author.update_reputation(15)


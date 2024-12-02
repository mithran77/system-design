from datetime import datetime

from answer import Answer
from comment import Comment
from tag import Tag
from vote import Vote
from votable import Votable
from commentable import Commentable


class Question(Votable, Commentable):

    def __init__(self, author, title, content, tags):
        self.id = id(self)
        self.author = author
        self.title = title
        self.content = content
        self.creation_date = datetime.now()
        self.answers = []
        self.tags = [Tag(name) for name in tags]
        self.votes = []
        self.comments = []

    def add_answer(self, answer: Answer):
        if answer in self.answers:
            raise ValueError("Answer must not exist")
        self.answers.append(answer)

    def vote(self, user, value: int):
        if value not in [1, -1]:
            raise ValueError("Vote value must be +1 or -1")
        self.votes = [v for v in self.votes if v.user != user]
        self.votes.append(Vote(user, value))
        self.author.update_reputation(value * 5)

    def get_vote_count(self):
        cnt = 0
        for v in self.votes:
            cnt += v.value
        return cnt

    def add_comment(self, comment: Comment):
        self.comments.append(comment)

    def get_comments(self):
        return self.comments.copy()


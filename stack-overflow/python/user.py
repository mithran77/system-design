from question import Question
from answer import Answer
from comment import Comment


class User:

    def __init__(self, user_id, username, email):
        self.id = user_id
        self.username = username
        self.email = email
        self.reputation = 0
        self.questions = []
        self.answers = []
        self.comments = []

    def ask_question(self, title, content, tags):
        question = Question(self, title, content, tags)
        self.questions.append(question)
        self.update_reputation(5)
        return question

    def answer_question(self, question: Question, content: str):
        answer = Answer(self, question, content)
        question.add_answer(answer)
        self.answers.append(answer)
        self.update_reputation(10)
        return answer

    def comment_on(self, commentable, content: str):
        comment = Comment(self, content)
        commentable.add_comment(content)
        self.comments.append(comment)
        self.update_reputation(2)
        return comment

    def update_reputation(self, value):
        self.reputation += value
        self.reputation = max(0, self.reputation) # not go below 0

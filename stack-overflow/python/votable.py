from abc import abstractmethod

class Votable:
    @abstractmethod
    def vote(self, user, value: int):
        pass

    @abstractmethod
    def get_vote_count(self):
        pass

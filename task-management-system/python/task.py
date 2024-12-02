from task_status import TaskStatus

class Task:
    def __init__(self, id, title, description, due_date, priority, assigned_user):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = TaskStatus.PENDING
        self.assigned_user = assigned_user

    def get_id(self):
        return self.id

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def get_description(self):
        return self.description

    def set_description(self, description):
        self.description = description

    def get_due_date(self):
        return self.due_date

    def set_due_date(self, due_date):
        self.due_date = due_date

    def get_priority(self):
        return self.priority

    def set_priority(self, priority):
        self.priority = priority

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_assigned_user(self):
        return self.assigned_user

    def set_assigned_user(self, user):
        self.assigned_user = user

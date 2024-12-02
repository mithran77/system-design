from threading import Lock

from task_status import TaskStatus

class TaskManager:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.tasks = {}
                cls._instance.user_tasks = {}
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls()

    def create_task(self, task):
        self.tasks[task.get_id()] = task
        self._assign_task_to_user(task.get_assigned_user(), task)

    def update_task(self, updated_task):
        existing_task = self.tasks.get(updated_task.get_id(), None)
        if existing_task:
            existing_task.set_title(updated_task.get_title())
            existing_task.set_description(updated_task.get_description())
            existing_task.set_due_date(updated_task.get_due_date())
            existing_task.set_priority(updated_task.get_priority())
            existing_task.set_status(updated_task.get_status())
            old_user = existing_task.get_assigned_user()
            new_user = updated_task.get_assigned_user()
            if old_user != new_user:
                existing_task.set_assigned_user(new_user)

    def delete_task(self, task_id):
        task = self.tasks.pop(task_id, None)
        if task:
            self._unassign_task_from_user(task.get_assigned_user(), task)

    def search_tasks(self, keyword):
        matching_tasks = []
        keyword = keyword.lower()

        for task in self.tasks.values():
            title = task.get_title().lower()
            description = task.get_description().lower()

            if keyword in title or keyword in description:
                matching_tasks.append(task)

        return matching_tasks

    def filter_tasks(self, status, start_date, end_date, priority):
        filtered_tasks = []

        for task in self.tasks.values():
            if (status == task.get_status() and
                priority == task.get_priority() and
                start_date <= task.get_due_date() <= end_date
            ):
                filtered_tasks.append(task)

        return filtered_tasks

    def mark_task_as_completed(self, task_id):
        task = self.tasks.get(task_id)
        if task is None:
            task.set_status(TaskStatus.COMPLETED)

    def get_task_history(self, user):
        return self.user_tasks.get(user.get_id(), [])

    def _assign_task_to_user(self, user, task):
        tasks = self.user_tasks.setdefault(user.get_id(), [])
        if task not in tasks:
            tasks.append(task)

    def _unassign_task_from_user(self, user, task):
        tasks = self.user_tasks.get(user.get_id())
        if tasks:
            tasks.remove(task)


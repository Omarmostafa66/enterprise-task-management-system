from app.models.task import TaskStatus


def validate_status_transition(current_status: TaskStatus, new_status: TaskStatus):
    """
    Enforce valid workflow transitions for tasks.
    Returns True if the transition is allowed, False otherwise.
    """
    allowed = {
        TaskStatus.TODO: [TaskStatus.IN_PROGRESS],
        TaskStatus.IN_PROGRESS: [TaskStatus.DONE, TaskStatus.TODO],
        TaskStatus.DONE: []  # Completed tasks cannot be modified further
    }

    if new_status not in allowed.get(current_status, []):
        return False

    return True
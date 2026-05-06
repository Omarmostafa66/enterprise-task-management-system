from app.models.task import TaskStatus

def validate_status_transition(current_status: TaskStatus, new_status: TaskStatus):
    allowed = {
        TaskStatus.TODO: [TaskStatus.IN_PROGRESS],
        TaskStatus.IN_PROGRESS: [TaskStatus.DONE, TaskStatus.TODO],
        TaskStatus.DONE: [] # المنتهي لا يعدل
    }
    if new_status not in allowed.get(current_status, []):
        return False
    return True
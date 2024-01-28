tasks = list(range(100))
import random

random.shuffle(tasks)
threads = 16


from wmeijer_utils.multithreading import parallelize_tasks_2

from dataclasses import dataclass


@dataclass
class MyObj:
    a: int
    b: int
    c: int
    d: int


def handle(task: int, task_id: int, worker_index: int, total_tasks: int | str):
    print(f"{task=}, {task_id=}, {worker_index=}, {total_tasks=}")
    # return [task, task_id, worker_index, total_tasks]
    # return "asdf"
    # return {"t": task, "tid": task_id, "wid": worker_index, 'tot': total_tasks}
    return MyObj(task, task_id, worker_index, total_tasks)


results = parallelize_tasks_2(tasks, handle, thread_count=threads, return_results=True)
# print(list(results))

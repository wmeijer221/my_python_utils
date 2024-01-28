from dataclasses import dataclass
import unittest

from wmeijer_utils.multithreading import parallelize_tasks_2


THREAD_COUNT = 8
WORK_LOAD = 1000


@dataclass
class MyObject:
    task: int
    task_id: int 
    worker_id: int 
    total_tasks: int | str


def return_task(task, task_id, worker_id, total_tasks):
    return task

def return_dict(task, task_id, worker_id, total_tasks):
    return {
        "task": task,
        "task_id": task_id,
        "worker_id": worker_id,
        "total_tasks": total_tasks,
        "constant": "my_constant",
    }

def return_object(task, task_id, worker_id, total_tasks):
    return MyObject(task, task_id, worker_id, total_tasks)


class TestMultithreading(unittest.TestCase):
    def test_paralellize_tasks_no_results(self):
        tasks = range(WORK_LOAD)

        results = parallelize_tasks_2(
            tasks, return_task, thread_count=THREAD_COUNT, return_results=False
        )

        results = list(results)

        assert len(results) == 0, "Did not expect to receive results."

    def test_paralellize_tasks_with_primitive_results(self):
        tasks = range(WORK_LOAD)

        results = parallelize_tasks_2(
            tasks, return_task, thread_count=THREAD_COUNT, return_results=True
        )

        results = list(results)

        assert len(results) == WORK_LOAD, f"Expected {WORK_LOAD} results, received {len(results)}."

        tasks = set(tasks)
        results = set(results)
        assert len(tasks.intersection(results)) == WORK_LOAD, "Incorrect results"

    def test_paralellize_countable_tasks_with_dict_results(self):
        tasks = list(range(WORK_LOAD))

        results = parallelize_tasks_2(
            tasks, return_dict, thread_count=THREAD_COUNT, return_results=True
        )

        # Result size test
        results = list(results)
        assert len(results) == WORK_LOAD, "Incorrect number of results."

        # Content test.
        valid_worker_ids = set(range(0, THREAD_COUNT))
        results = sorted(results, key=lambda element: element["task"])
        for result, task in zip(results, tasks):
            assert result["task"] == task, f'Mismatch in tasks {result['task']} does not match {task}.'
            assert result['worker_id'] in valid_worker_ids, f"Worker ID {result['worker_id']} is invalid."
            assert result['total_tasks'] == len(tasks), f'Expected {len(tasks)}, received {result['total_tasks']}'
            assert result['constant'] == 'my_constant'

    def test_paralellize_uncountable_tasks_with_dict_results(self):
        tasks = range(WORK_LOAD)

        results = parallelize_tasks_2(
            tasks, return_dict, thread_count=THREAD_COUNT, return_results=True
        )

        # Result size test
        results = list(results)
        assert len(results) == WORK_LOAD, "Incorrect number of results."

        # Content test.
        valid_worker_ids = set(range(0, THREAD_COUNT))
        results = sorted(results, key=lambda element: element["task"])
        for result, task in zip(results, tasks):
            assert result["task"] == task, f'Mismatch in tasks {result['task']} does not match {task}.'
            assert result['worker_id'] in valid_worker_ids, f"Worker ID {result['worker_id']} is invalid."
            assert result['total_tasks'] == "unknown", f'Expected {len(tasks)}, received {result['total_tasks']}'
            assert result['constant'] == 'my_constant'

    def test_paralellize_tasks_with_object_results(self):
        tasks = range(WORK_LOAD)

        results = parallelize_tasks_2(
            tasks, return_object, thread_count=THREAD_COUNT, return_results=True
        )

        # Result size test
        results = list(results)
        assert len(results) == WORK_LOAD, "Incorrect number of results."

        # Content test.
        valid_worker_ids = set(range(0, THREAD_COUNT))
        valid_task_ids = set(range(0, WORK_LOAD))
        used_task_ids = set()
        results = sorted(results, key=lambda element: element.task)
        for result, task in zip(results, tasks):
            assert isinstance(result, MyObject), "Received incorrect object type."
            assert result.task == task, f'Mismatch in tasks {result['task']} does not match {task}.'
            assert result.worker_id in valid_worker_ids, f"Worker ID {result['worker_id']} is invalid."
            assert result.total_tasks == "unknown", f'Expected {len(tasks)}, received {result['total_tasks']}'
            assert result.task_id in valid_task_ids, f'Task ID {result.task_id} is invalid.'
            assert result.task_id not in used_task_ids, f"Task ID {result.task_id} is used twice."
            used_task_ids.add(result.task_id)

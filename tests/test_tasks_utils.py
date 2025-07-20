from datetime import datetime

from hyperhelix.core import HyperHelix
from hyperhelix.node import Node
from hyperhelix.tasks.task import Task
from hyperhelix.tasks import task_manager, sprint_planner


def test_tasks_workflow():
    g = HyperHelix()
    task = Task(id='t1', description='demo', due=datetime.utcnow())
    task_manager.create_task(g, task)
    task_manager.assign_task(g, 't1', 'alice')
    assert g.nodes['t1'].payload.assigned_to == 'alice'
    plan = sprint_planner.sprint_plan(g)
    assert plan == ['t1']

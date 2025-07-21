from __future__ import annotations

from fastapi import APIRouter, Depends, Body, HTTPException
from typing import List

from ..dependencies import get_graph
from ...core import HyperHelix
from ...tasks.task import Task
from ...tasks import task_manager, sprint_planner
from ..schemas import TaskIn, TaskOut

router = APIRouter()


@router.post('/tasks', response_model=TaskOut)
def create_task(task: TaskIn, graph: HyperHelix = Depends(get_graph)) -> TaskOut:
    if task.id in graph.nodes:
        raise HTTPException(status_code=400, detail='Task exists')
    data = Task(**task.dict())
    task_manager.create_task(graph, data)
    return TaskOut(**task.dict())


@router.post('/tasks/{task_id}/assign')
def assign_task_endpoint(
    task_id: str,
    user: str = Body(..., embed=True),
    graph: HyperHelix = Depends(get_graph),
) -> dict[str, str]:
    if task_id not in graph.nodes:
        raise HTTPException(status_code=404, detail='Not found')
    task_manager.assign_task(graph, task_id, user)
    return {'task': task_id}


@router.get('/tasks', response_model=List[TaskOut])
def list_tasks(graph: HyperHelix = Depends(get_graph)) -> List[TaskOut]:
    tasks: List[TaskOut] = []
    for node in graph.nodes.values():
        if isinstance(node.payload, Task):
            tasks.append(TaskOut(**node.payload.__dict__))
    return tasks


@router.get('/tasks/plan', response_model=List[str])
def sprint_plan_endpoint(graph: HyperHelix = Depends(get_graph)) -> List[str]:
    return sprint_planner.sprint_plan(graph)


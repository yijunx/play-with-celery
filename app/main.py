from celery import Celery
from uuid import uuid4


app = Celery("tasks", broker="amqp://rabbitmq:5672")


if __name__ == "__main__":
    task_id = task_id=str(uuid4())
    app.send_task(
        name="tasks1.do_it",
        task_id=task_id,
        kwargs={
            "name": "wow",
            "hihi": "yes"
        },
        queue="my-celery-queue1"
    )

    task_id = task_id=str(uuid4())
    app.send_task(
        name="tasks2.do_it",
        task_id=task_id,
        kwargs={
            "name": "wow2",
            "hihi": "yes2"
        },
        queue="my-celery-queue2"
    )
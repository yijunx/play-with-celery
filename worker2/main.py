from celery import Celery


app = Celery("tasks2", broker="amqp://rabbitmq:5672")


@app.task()
def do_it(name: str, hihi: str):
    print(name, hihi)


if __name__ == "__main__":
    app.worker_main(
        argv=[
            "worker",
            "--loglevel=info",
            "--queues",
            "my-celery-queue2"
        ]
    )
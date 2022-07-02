import time
from celery import Celery


app = Celery("tasks1", broker="amqp://rabbitmq:5672")


@app.task()
def do_it(name: str, hihi: str):
    print(name, hihi)


@app.task()
def do_it_slow(name: str, hihi: str):
    print("doing it slow")
    time.sleep(5)
    print("done")
    print(name, hihi)


if __name__ == "__main__":
    app.worker_main(argv=["worker", "--loglevel=info", "--queues", "my-celery-queue1"])

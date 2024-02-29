from celery import Celery
import requests
from logging import getLogger


app = Celery("tasks3", broker="amqp://rabbitmq:5672")
logger = getLogger(__name__)

class CustomError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


@app.task(autoretry_for=(CustomError,), retry_backoff=True, retry_kwargs={'max_retries': 5})
def do_it(**kwargs):
    r = requests.get("http://mock-service:5000")
    # this mockserivce has 50% changce to return 500
    if r.status_code != 200:
        logger.info(f"request's status is {r.status_code}")
        raise CustomError(msg="well the service is down, will retry in exponential time")

if __name__ == "__main__":
    app.worker_main(argv=["worker", "--loglevel=info", "--queues", "my-celery-queue2"])

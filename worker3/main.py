from celery import Celery, Task
from celery.worker.request import Request
import requests
from logging import getLogger
from requests.exceptions import ConnectionError


app = Celery("tasks3", broker="amqp://rabbitmq:5672")
logger = getLogger(__name__)


class MyRequest(Request):
    "A minimal custom request to log failures and hard time limits."

    def on_timeout(self, soft, timeout):
        super(MyRequest, self).on_timeout(soft, timeout)
        if not soft:
            hard_time_msg = f"A hard timeout was enforced for task {self.task.name}"
            logger.warning(hard_time_msg)
            info = self.info()["kwargs"]

            # report_worker_status_to_dataset_management(
            #     status="Failed",
            #     targets=[info["created_by"]],
            #     message="User file size exceeds limit for profiling and data-type inference",
            # )

    def on_failure(self, exc_info, send_failed_event=True, return_ok=False):
        """triggered when get killed, to handle the signal 9"""
        super().on_failure(
            exc_info, send_failed_event=send_failed_event, return_ok=return_ok
        )
        info = self.info()["kwargs"]
        logger.warning(f"well it failed...")
        # report_worker_status_to_dataset_management(
        #     status="Failed",
        #     targets=[info["created_by"]],
        #     message="User file size exceeds limit for profiling and data-type inference. Please manually update the data types, thanks!",
        # )


class MyTask(Task):
    Request = MyRequest  # you can use a FQN 'my.package:MyRequest'



class RelatedServiceReturn500(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class CannotEstablishConn(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


@app.task(
    base=MyTask, 
    autoretry_for=(RelatedServiceReturn500,), 
    retry_backoff=True, 
    retry_kwargs={'max_retries': 5}
)
def do_it(**kwargs):
    # this mockserivce has 50% changce to return 500
    try:
        r = requests.get("http://mock-service:5000")
        if r.status_code != 200:
            logger.info(f"request's status is {r.status_code}")
            raise RelatedServiceReturn500(msg="well the service is not ok")
    except ConnectionError:
        raise CannotEstablishConn(msg="something wrong with internet")

if __name__ == "__main__":
    app.worker_main(argv=["worker", "--loglevel=info", "--queues", "my-celery-queue2"])

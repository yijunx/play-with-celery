# ------------------------------------------------------------------------------------------------------------
# Copyright (c) UCARE.AI Pte Ltd. All rights reserved.
# ------------------------------------------------------------------------------------------------------------
from flask import Flask, request, Response, abort
import logging
import random
import string

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
logger =  logging.getLogger(__name__)


@app.route("/", methods=["GET"])
def get_patient():
    httpcode = random.choice([500, 200])
    logger.info(f"http code is {httpcode}")
    return "hello", httpcode


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

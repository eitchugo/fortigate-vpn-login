# -*- coding: utf-8 -*-
"""
    fortigate_vpn_login.webserver
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Web Server to receive requests from the SAML provider. Credits goes to the werkzeug
    documentation.

    <https://werkzeug.palletsprojects.com/en/2.3.x/serving/#shutting-down-the-server>
"""
import multiprocessing
import logging
from werkzeug import Request, Response, run_simple
from fortigate_vpn_login import logger

logging.getLogger('werkzeug').setLevel(logging.ERROR)

queue = multiprocessing.Queue()


def get_token(q: multiprocessing.Queue, host: str = "127.0.0.1", port: int = 8020) -> None:
    """
    Opens a web server on `localhost:8020`, listens to a request searching for the `id`
    parameter. The value is then put inside the global queue.

    Args:
        q (multiprocessing.Queue): queue object to put the value of the request parameter
        host (str|Optional): hostname or ip address to bind to the webserver
        port (int|Optional): port number to bind to the webserver
    """
    @Request.application
    def app(request: Request) -> Response:
        logger.debug(f"Putting value in the queue: {request.args['id']}")
        q.put(request.args['id'])
        return Response('', 204)

    logger.debug(f"Running web server on {host}:{port}")
    run_simple(host, port, app)


def run() -> multiprocessing.Process:
    """
    Runs the web server (`get_token` method) in a separate process.

    Returns:
        multiprocessing.Process: the Process object running the method
    """
    global queue
    p = multiprocessing.Process(target=get_token, args=(queue,))
    logger.debug('Starting another process to run the webserver')
    p.start()
    return p


def return_token() -> str:
    """
    Blocks the process while waiting for the token in the global queue.
    """
    global queue
    print("Waiting for the token...")
    token = queue.get(block=True)
    logger.debug(f"Got token: {token}")
    return (token)


def quit(p: multiprocessing.Process) -> None:
    """
    Terminates a process.

    Args:
        p (multiprocessing.Process): the Process object which will be terminated.
    """
    logger.debug('Terminating the web server process')
    p.terminate()

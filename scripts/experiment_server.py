#!/usr/bin/env python3

# %*% Experiment metainfo and time synchronization server.
#
# It receives 3 types of commands:
# * time:<float>  -> Tells the service the local time for the subprocess for sync reasons.
# * set:key:value -> Sets an arbitrary variable associated with this connection to the
#                    specified value, can be used to share arbitrary data generated at
#                    startup between nodes just before starting the experiment.
# * ready         -> Indicates that this specific instance has ending sending its info
#                    and its ready to start.
#
# When the all of the instances we are waiting for are all ready, all the information will
# be sent back to them in the form of a JSON document. After this, a "go" command will
# be sent to indicate that they should start running the experiment.
#
# Example of an expected exchange:
# [connection is opened by the client]
# -> time:1378479678.11
# -> set:asdf:ooooo
# -> ready
# <- id:0
# <- {"0": {"host": "127.0.0.1", "time_offset": -0.94, "port": 12000, "asdf": "ooooo"}, "1": {"host": "127.0.0.1", "time_offset": "-1378479680.61", "port": 12001, "asdf": "ooooo"}, "2": {"host": "127.0.0.1", "time_offset": "-1378479682.26", "port": 12002, "asdf": "ooooo"}}
# <- go
# [Connection is closed by the server]
import logging
from asyncio import ensure_future, get_event_loop
from os import environ

from gumby.log import setupLogging
from gumby.sync import ExperimentServiceFactory


# @CONF_OPTION SYNC_PORT: Port where we should listen on. (required)

if __name__ == '__main__':
    setupLogging()

    expected_subscribers = int(environ['INSTANCES_TO_RUN'])
    experiment_start_delay = float(environ['SYNC_EXPERIMENT_START_DELAY'])
    server_port = int(environ['SYNC_PORT'])

    loop = get_event_loop()
    logger = logging.getLogger("experiment_server")
    logger.info("Creating experiment server on port %d", server_port)
    ensure_future(loop.create_server(ExperimentServiceFactory(expected_subscribers, experiment_start_delay),
                                     host="0.0.0.0", port=server_port))
    loop.exit_code = 0
    loop.run_forever()
    loop.close()
    exit(loop.exit_code)

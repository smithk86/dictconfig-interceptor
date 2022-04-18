from dictconfig_interceptor import dictConfigCallbacks

import logging
import logging.config
import warnings
from typing import Dict

import pytest


test_config = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {"format": "%(asctime)s %(levelname)-8s %(name)-15s %(message)s"}
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "ERROR",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "standard",
            "level": "DEBUG",
            "filename": "/tmp/test_logging518.log",
            "mode": "w",
        },
    },
    "root": {"handlers": ["console", "file"], "level": "NOTSET"},
}


def test_logging_config():
    # confirm attributes about the logging setup prior to running dictConfig()
    assert logging.root.level == 30
    assert len(logging.root.handlers) == 4

    # load config with a context manager
    logging.config.dictConfig(test_config)

    # confirm attributes from test_config are setup
    assert logging.root.level == 0
    assert len(logging.root.handlers) == 2
    assert type(logging.root.handlers[0]).__name__ == "StreamHandler"
    assert type(logging.root.handlers[1]).__name__ == "FileHandler"
    assert logging.root.handlers[1].baseFilename == "/tmp/test_logging518.log"


def test_config_callback():
    with dictConfigCallbacks() as callbacks:

        @callbacks
        def config_callback(config):
            assert isinstance(config, Dict)
            assert config["version"] == 1
            warnings.warn("config_callback() was executed", RuntimeWarning)

        with pytest.warns(RuntimeWarning, match=r"config_callback\(\) was executed"):
            logging.config.dictConfig(test_config)

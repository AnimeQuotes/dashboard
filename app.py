import importlib
import inspect
import os

import flask
from mongoengine import connect
from werkzeug.exceptions import HTTPException

from utils import get_config, handle_exception, template_filters


class App(flask.Flask):
    def __init__(self):
        super().__init__(__name__)
        self.config.from_object(get_config())
        self.register_error_handler(HTTPException, handle_exception)

        self._load_blueprints()
        self._load_template_filters()

        # db connection
        connect(
            os.environ.get("DB_NAME"),
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT"),
            username=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            authentication_source=os.environ.get("DB_AUTH_SOURCE")
        )

    def _load_blueprints(self):
        for root, dirs, filenames in os.walk("blueprints"):
            for fn in filenames:
                if not fn.endswith(".py"):
                    continue

                module = importlib.import_module(root.replace(os.sep, ".") + "." + fn[:-3])
                blueprint = inspect.getmembers(module, lambda o: isinstance(o, flask.Blueprint))[0][1]
                self.register_blueprint(blueprint)

    def _load_template_filters(self):
        filters = inspect.getmembers(
            template_filters,
            lambda o: inspect.isfunction(o) and o.__name__.startswith("filter_")
        )
        for f in filters:
            self.add_template_filter(f[1], f[0][7:])

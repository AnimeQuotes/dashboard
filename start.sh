#!/bin/bash
gunicorn -b 127.0.0.1:5000 -w 4 -k gevent main:app
#!/bin/bash
killall -s INT uwsgi
uwsgi --yaml uwsgi.yaml
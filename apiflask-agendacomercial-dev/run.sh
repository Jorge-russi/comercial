#!/bin/bash
export FLASK_APP=/home/xubuntu/ApiCajasanAgendaComercial/src/app.py
export FLASK_DEBUG=0
export PRJS_CONF_FILE=/home/xubuntu/ApiCajasanAgendaComercial/config.properties
. /home/xubuntu/ApiCajasanAgendaComercial/venv/bin/activate
flask run --host=0.0.0.0 --port=5001 --debugger

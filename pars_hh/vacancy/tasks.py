from pars_hh.celery import app

from .hh_api import Results

@app.task
def res_pars(vac, reg, id):
    Results(vac, reg, id).parsing()

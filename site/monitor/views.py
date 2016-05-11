'''
rtp.site.monitor.views

author | Immanuel Washington

Functions
---------
db_objs | gathers database objects for use
index | shows main page
stream_plot | streaming plot example
data_hist | creates histogram
obs_table | shows observation table
file_table | shows file table
day_summary_table | shows day summary table
'''
from flask import render_template, flash, redirect, url_for, request, g, make_response, Response, jsonify
from rtp.site.flask_app import monitor_app as app, monitor_db as db
import dbi as rdbi
from sqlalchemy import func

def db_objs():
    '''
    outputs database objects

    Returns
    -------
    tuple:
        object: database interface object
        object: observation table object
        object: file table object
        object: log table object
    '''
    dbi = rdbi.DataBaseInterface()
    obs_table = rdbi.Observation
    file_table, log_table = rdbi.File
    log_table = rdbi.Log

    return dbi, obs_table, file_table, log_table

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    '''
    start page of the website
    grabs time data

    Returns
    -------
    html: index
    '''
    dbi, obs_table, file_table, log_table = db_objs()

    with dbi.session_scope() as s:
        pass

    return render_template('index.html')

@app.route('/stream_plot', methods = ['GET', 'POST'])
def stream_plot():
    '''
    generate streaming data

    Returns
    -------
    '''
    dbi, obs_table, file_table, log_table = db_objs()

    with dbi.session_scope() as s:
        pass

    return jsonify({'count': file_count})

@app.route('/data_hist', methods = ['POST'])
def data_hist():
    '''
    generate histogram for data

    Returns
    -------
    html: histogram
    '''
    dbi, obs_table, file_table, log_table = db_objs()

    with dbi.session_scope() as s:
        pass

    return render_template('data_hist.html')

@app.route('/obs_table', methods = ['POST'])
def obs_table():
    '''
    generate observation table for killed and failed observations

    Returns
    -------
    html: observation table
    '''
    dbi, obs_table, file_table, log_table = db_objs()
    with dbi.session_scope() as s:
        failed_obs = s.query(obs_table)\
                      .filter(obs_table.current_stage_in_progress == 'FAILED')\
                      .order_by(obs_table.current_stage_start_time)\
                      .all()
        killed_obs = s.query(obs_table)\
                      .filter(obs_table.current_stage_in_progress == 'KILLED')\
                      .order_by(obs_table.current_stage_start_time)\
                      .all()

    return render_template('obs_table.html', failed_obs=failed_obs, killed_obs=killed_obs)

@app.route('/file_table', methods = ['GET', 'POST'])
def file_table():
    '''
    generate file table for histogram bar

    Returns
    -------
    html: file table
    '''
    dbi, obs_table, file_table, log_table = db_objs()
    with dbi.session_scope() as s:
        file_query = s.query(file_table).join(obs_table)\
                      .filter((obs_table.current_stage_in_progress != 'FAILED') | (obs_table.current_stage_in_progress.is_(None)))\
                      .filter((obs_table.current_stage_in_progress != 'KILLED') | (obs_table.current_stage_in_progress.is_(None)))\
                      .filter(obs_table.status != 'NEW')\
                      .filter(obs_table.status != 'COMPLETE')\
                      .filter(obs_table.current_pid > 0)\
                      .order_by(obs_table.current_stage_start_time)
        working_FILEs = file_query.all()


    return render_template('file_table.html', working_FILEs=working_FILEs)

@app.route('/day_summary_table', methods=['POST'])
def day_summary_table():
    '''
    summary of data in main databases

    Returns
    -------
    html: day summary table
    '''
    dbi, obs_table, file_table, log_table = db_objs()

    with dbi.session_scope() as s:
        pass

    return render_template('day_summary_table.html')

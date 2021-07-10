from flask import Blueprint, request
import json
import os
from server.main import jobs
from server.main.rq_helpers import get_job_from_id

main_blueprint = Blueprint("main", __name__)


# Default route
@main_blueprint.route('/', methods=['GET'])
def default():
    return json.dumps('Application is working')


# Register Details
@main_blueprint.route('/registerdetails', methods=['POST'])
def registerdetails():
    record = request.form.to_dict()
    record['age'] = int(record['age'])
    if record['caseno']==None or record['age']==None or record['gender']==None or record['date']==None or record['name']==None:
        return json.dumps("Check the values"), 400
    
    job = jobs.storedetails.delay(record['caseno'], record['name'], record['age'],  record['gender'], record['date'])
    return json.dumps({'JobID': job.id, 'status':'Success'}), 200


# Store autopsy data
@main_blueprint.route('/store', methods=['POST'])
def store():
    record = request.form.to_dict()
    if record['caseno']==None or record['img']==None or record['pdf']==None or record['audio']==None:
        return json.dumps("Check the values"), 400

    img = jobs.storedoc.delay('img', record['caseno'])
    with open(os.path.join('uploads', 'img'), 'w') as d:
        d.write(record['img'])
        d.close()

    pdf = jobs.storedoc.delay('pdf', record['caseno'])
    with open(os.path.join('uploads', 'pdf'), 'w') as d:
        d.write(record['pdf'])
        d.close()

    audio = jobs.storedoc.delay('audio', record['caseno'])
    with open(os.path.join('uploads', 'audio'), 'w') as d:
        d.write(record['audio'])
        d.close()

    return json.dumps({'Image': img.id, 'Audio':audio.id, 'PDF':pdf.id, 'status':'Success'}), 200


# Get all cases
@main_blueprint.route('/getcases', methods=['GET'])
def getcases():
    resobj = {0: jobs.getcases()}
    return json.dumps(resobj)


# Retreive case details
@main_blueprint.route('/retrieve', methods=['GET'])
def retrieve():
    caseno = request.args.get('caseno')
    doctype = request.args.get('doctype')
    if caseno==None or doctype==None:
        return "Not a valid request", 400

    return json.dumps(jobs.retrieve_data(caseno, doctype)), 200


# Get status of the enqued jobs
@main_blueprint.route('/getstatus', methods=['GET'])
def getstatus():
    id = request.args.get('jobid')
    if id==None:
        return "Not a valid request", 400

    job = get_job_from_id(id)

    if job:
        response_object = {
            'status':job.get_status(),
            'result':job.result,
            'execution info': job.exc_info
        }
        status_code = 200
    else:
        response_object = {"message": "job not found"}
        status_code = 500

    return json.dumps(response_object), status_code
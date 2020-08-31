from flask import Flask, request
from flask_babel import Babel, gettext


# Setup app
app = Flask(__name__)
babel = Babel(app)


# Global (BAD!) app state
assignment_id_acc = 0
assignments = {}


@app.route('/assignment/<int:assignment_id>', methods=['GET'])
def assignment_get(assignment_id):
    global assignments
    if not assignment_id in assignments:
        return {
            'status': 404,
            'msg': gettext('requested assignment does not exist')
        }, 404
    else:
        return {
            'status': 200,
            'msg': gettext('here is your assignment'),
            'assignment': assignments[assignment_id]
        }


@app.route('/assignment', methods=['POST'])
def assignment_post():
    global assignments
    global assignment_id_acc

    assignment_id_acc += 1
    data = request.json

    if data is not dict:
        return {
            'status': 400,
            'msg': gettext('invalid or missing assignment data')
        }, 400
    
    data['id'] = assignment_id_acc
    assignments[assignment_id_acc] = data

    return {
        'status': 200,
        'msg': gettext('assignment added'),
        'assignment_id': assignment_id_acc
    }


@app.route('/assignment/<int:assignment_id>', methods=['PATCH'])
def assignment_patch(assignment_id):
    global assignments
    if assignment_id not in assignments:
        return { 
            'status': 404,
            'msg': gettext('requested assignment does not exist')
        }, 404
    
    data = request.json
    
    if data is not dict:
        return {
            'status': 400,
            'msg': gettext('invalid assignment data')
        }, 400
    
    for key in data:
        assignments[key] = data
    
    return {
        'status': 200,
        'msg': gettext('assignment updated')
    }


@app.route('/assignments', methods=['GET'])
def assignments_get():
    global assignments
    
    result = list(assignments.values())

    return {
        'status': 200,
        'msg': gettext('here are your assignments'),
        'assignments': result
    }
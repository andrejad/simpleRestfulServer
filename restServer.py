# Main script of the RESTful web services server. Exposes several CRUD methods over the dable dataT
# (described in dbService.py). See *.sh scripts for running in hohup mode.
# Dependencies: flask, flask_restful

import dbService
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse

# Starting the server, Flask library, port 5000
app = Flask(__name__)
api = Api(app)

# Setting up the parser for input REST json parameters.
# Each pargument must be defined in the parser setup here.
# http://flask-restful.readthedocs.io/en/0.3.5/reqparse.html
# why and how to use method request.get_json(force=true): http://stackoverflow.com/questions/30491841/python-flask-restful-post-not-taking-json-arguments
#
parser = reqparse.RequestParser()
parser.add_argument('message', required=True, help="Message cannot be blank!", location = 'args')
parser.add_argument('owner', required=True, help="Owner must be supplied!", location = 'args')
parser.add_argument('priority', type=int, required=True, location = 'args') #not mandatory, default 1
parser.add_argument('taskId', type=int, location = 'args') #not mandatory, default 1

# For browser call http://127.0.0.1:5000/ this will display the list of REST methods exposed.
# For "new" and "update" functions there is an alternative with curl linux command and how to use it.
@app.route('/')
def index():
    print ("5000:/ (list of api's)")
    dl = ['/alldata', '/owner/<string:owner>', '/get/<int:rowid>', '/new ('+newCurl+')', '/update ('+updateCurl+')', '/del/<string:rowid>']
    return jsonify(dl)

# Fetches all data from the table in database (there is only one table)
# and returns a JSON structure (check with http://127.0.0.1:5000/)
class FetchDataT(Resource):
    def get(self):
        print ("FetchDataT()")
        d = dbService.getAllDataT(0)
        dl = dbService.rowsToListDict(d)
        return jsonify(dl)

# Returns data from the table that has column value <owner>
class GetByOwner(Resource):
    def get(self, owner):
        print ("GetByOwner(" + owner + ")")
        d = dbService.getAllByOwner(owner, 0)
        dl = dbService.rowsToListDict(d)
        return jsonify(dl)

# Returns a single record from the table, based on unique rowid.
class GetByRowId(Resource):
    def get(self, rowid):
        print ("GetByRowId(" + str(rowid) + ")")
        d = dbService.getById(rowid)
        dl = dbService.rowsToListDict(d)
        return jsonify(dl)

# Inserts a new record in the table. 
class InsertNew(Resource):
    def put(self):
        json_data = request.get_json(force=True)
        print ("InsertNew(", json_data['owner'], json_data['priority'], json_data['message'], ")")
        d = dbService.putNewTask(json_data['owner'], json_data['priority'], json_data['message'])
        return jsonify(d)

# Updates a record referenced as rowid (primary key). Other paramters are optional.
class UpdateRec(Resource):
    def put(self):
        json_data = request.get_json(force=True)
        print ("UpdateRec(", json_data['taskId'], json_data['owner'], json_data['priority'], json_data['message'], ")")
        # TODO: validation
        d = dbService.updateDataT(json_data['taskId'], json_data['owner'], json_data['priority'], json_data['message'])
        return jsonify(d)                

# Deletes a record in the table referenced as rowid.
class DeleteRec(Resource):
    def get(self, rowid):
        print ("DeleteRec(" + rowid + ")")
        d = dbService.deleteTask(rowid)        
        return jsonify(d)

# Assigning methods to the URL endpoints.
#
# return all rows (max 100)
api.add_resource(FetchDataT, '/alldata')
#
# return one record
api.add_resource(GetByOwner, '/owner/<string:owner>')
#
# return one record
api.add_resource(GetByRowId, '/get/<int:rowid>')
#
# curl -H "Content-Type: application/json" -X PUT -d '{"owner":"bob","priority":"2","message":"testing insert new"}' http://82.168.90.36:5000/new
newCurl = """curl -H "Content-Type: application/json" -X PUT -d '{"owner":"bob","priority":2,"message":"testing insert new"}' http://127.0.0.1:5000/new"""
api.add_resource(InsertNew, '/new')
#
# curl -H "Content-Type: application/json" -X PUT -d '{"rowid":"1","owner":"bob","priority":"2","message":"testing update"}' http://82.168.90.36:5000/update
updateCurl = """curl -H "Content-Type: application/json" -X PUT -d '{"taskId":"1","owner":"bob","priority":"2","message":"testing update"}' http://127.0.0.1:5000/update"""
api.add_resource(UpdateRec, '/update')
#
# delete a record
api.add_resource(DeleteRec, '/del/<string:rowid>')

# Running the server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

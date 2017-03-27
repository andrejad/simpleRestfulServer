import dbApp
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse

hueip = "192.168.2.2"

app = Flask(__name__)
api = Api(app)

# http://flask-restful.readthedocs.io/en/0.3.5/reqparse.html
parser = reqparse.RequestParser()
parser.add_argument('message', required=True, help="Message cannot be blank!")
parser.add_argument('owner', required=True, help="Owner must be supplied!")
parser.add_argument('priority', type=int) #not mandatory, default 1
parser.add_argument('taskId', type=int) #not mandatory, default 1

@app.route('/')
def index():
    print ("5000:/ (list of api's)")
    dl = ['/alldata', '/owner/<string:owner>', '/get/<int:rowid>', '/new ('+newCurl+')', '/update ('+updateCurl+')', '/del/<string:rowid>']
    return jsonify(dl)

class FetchDataT(Resource):
    def get(self):
        print ("FetchDataT()")
        d = dbApp.getAllDataT(0)
        dl = dbApp.rowsToListDict(d)
        return jsonify(dl)

class GetByOwner(Resource):
    def get(self, owner):
        print ("GetByOwner(" + owner + ")")
        d = dbApp.getAllByOwner(owner, 0)
        dl = dbApp.rowsToListDict(d)
        return jsonify(dl)

class GetByRowId(Resource):
    def get(self, rowid):
        print ("GetByRowId(" + str(rowid) + ")")
        d = dbApp.getById(rowid)
        dl = dbApp.rowsToListDict(d)
        return jsonify(dl)

class InsertNew(Resource):
    def put(self):
        args = parser.parse_args()
        print(args)
        if args['priority'] == "":
            args['priority'] = 1
            print ("Using default priority = 1")
        print ("InsertNew(", args['owner'], args['priority'], args['message'], ")")
        d = dbApp.putNewTask(args['owner'], args['priority'], args['message'])
        return jsonify(d)

class UpdateRec(Resource):
    def put(self):
        args = parser.parse_args()
        #print (args);
        print ("UpdateRec(", str(args['taskId']), args['owner'], args['priority'], args['message'], ")")
        # TODO: validation
        d = dbApp.updateDataT(args['taskId'], args['owner'], args['priority'], args['message'])
        return jsonify(d)        

class DeleteRec(Resource):
    def get(self, rowid):
        print ("DeleteRec(" + rowid + ")")
        d = dbApp.deleteTask(rowid)        
        return jsonify(d)

# return all rows (max 100)
api.add_resource(FetchDataT, '/alldata')

# return one record
api.add_resource(GetByOwner, '/owner/<string:owner>')

# return one record
api.add_resource(GetByRowId, '/get/<int:rowid>')

# curl -H "Content-Type: application/json" -X PUT -d '{"owner":"bob","priority":"2","message":"testing insert new"}' http://82.168.90.36:5000/new
newCurl = """curl -H "Content-Type: application/json" -X PUT -d '{"owner":"bob","priority":"2","message":"testing insert new"}' http://127.0.0.1:5000/new"""
api.add_resource(InsertNew, '/new')

# curl -H "Content-Type: application/json" -X PUT -d '{"rowid":"1","owner":"bob","priority":"2","message":"testing update"}' http://82.168.90.36:5000/update
updateCurl = """curl -H "Content-Type: application/json" -X PUT -d '{"taskId":"1","owner":"bob","priority":"2","message":"testing update"}' http://127.0.0.1:5000/update"""
api.add_resource(UpdateRec, '/update')

# delete a record
api.add_resource(DeleteRec, '/del/<string:rowid>')

# hue: x1TM0J5xWoDuec20vBdB18lw1nI3pAa00Uhz7zpi
# hueip = "192.168.2.2"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

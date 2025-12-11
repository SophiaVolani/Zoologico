from src.config import *
from src.service.common_service import *
from src.model.person import *
from src.model.car import *
from src.utils import *


# default route
@app.route('/')
def index():
    return "Welcome to the API. Use /persons and /cars endpoints."

# --- POST's (creation) ---

# generic object creation: auxiliar function
def create_simple_object(mclass, data):
    try:
        myjson = {"result": "ok"}               # prepare some default answer
        user = create_object(mclass, **data)    # try to create the object
        response = serialize_model(user)        # prepare an answer with the serialized object
        myjson.update({"details": response})    # add the serialized object to the answer
        return myjson                           # return the answer
    except Exception as ex:
        print(f"Error during object creation: {ex}")
        return {"result":"error", "details":f"error during object creation: {ex}"}
    
@app.route('/persons', methods=['POST'])
def create_person():
    data = request.json                         # get the data
    answer = create_simple_object(Person, data)   # try to create the object
    return jsonify(answer), 201 if answer["result"] == "ok" else 500 # return created or internal error

@app.route('/cars', methods=['POST'])
def create_cars():
    data = request.json                         # get the data
    answer = create_simple_object(Car, data)   # try to create the object
    return jsonify(answer), 201 if answer["result"] == "ok" else 500 # return created or internal error
        
# --- GET's LIST ---

# auxiliar function
def get_objects_helper(mclass):
    try:
        myjson = {"result": "ok"}   
        objs = get_objects(mclass)                   # get all objects
        response = [serialize_model(u) for u in objs]  # serialize the objects
        myjson.update({"details": response})            # add the serialized object to the answer
        return myjson
    except Exception as ex:
        print(f"Error during {mclass} listing: {ex}")
        return {"result": "error", "details": f"error during {mclass} listing: {ex}"}

@app.route('/persons', methods=['GET'])
def list_persons():
    myjson = get_objects_helper(Person)
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 500

@app.route('/cars', methods=['GET'])
def list_cars():
    myjson = get_objects_helper(Car)
    return jsonify(myjson), 200 if myjson['result'] == 'ok' else 500

# --- DELETE's ---

def delete_object(mclass, obj_id):
    try:
        myjson = {"result": "ok"}  # prepare a "good" default answer :-)   
    
        obj = get_object_by_attribute(mclass, "id", obj_id)
        if not obj:
            return {"result": "error", "details": f"{mclass}({obj_id}) not found "}
        db.session.delete(obj)
        db.session.commit()
        myjson.update({"details": "ok"})
        return myjson
    except Exception as ex:
        print(f"Error during hard delete of object {mclass} with id {obj_id}: {ex}")
        return {"result": "error", "details": f"error during object ({mclass}) exclusion: {ex}"}

@app.route('/persons/<int:obj_id>', methods=['DELETE'])
def delete_person(obj_id):
    myjson = delete_object(Person, obj_id)
    return jsonify(myjson), 204 if myjson['result'] == 'ok' else 500

@app.route('/cars/<int:obj_id>', methods=['DELETE'])
def delete_car(obj_id):
    myjson = delete_object(Car, obj_id)
    return jsonify(myjson), 204 if myjson['result'] == 'ok' else 500

print("Routes loaded successfully.")

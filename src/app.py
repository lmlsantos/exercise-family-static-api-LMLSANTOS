"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# endpoint that gets all members of the family
@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# endpoint that gets a member of the family
@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    members = jackson_family.get_member(id)
    return jsonify(members), 200

#endpoint that adds a new member to the family
@app.route('/add/member', methods=['POST'])
def add_member():
    member = request.json
    jackson_family.add_member(member)
    if not member:
        return jsonify({"error":"No family member was found"}), 400
    return jsonify("A family member was added"), 200

#endpoint that deletes a member of the family
@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = jackson_family.delete_member(id)
    return jsonify({"done":"true"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

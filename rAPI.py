from flask import Flask, jsonify, request, make_response
from flask_restful import Resource
from datacollection import data_collection

app = Flask(__name__)
# Documentation for Home Page
tasks = [
    {
        'url': '/',
        'Method': 'GET',
        'Description': 'returns the API documentation'
    },
    {
        'url': '/solr_db_content',
        'Method': 'POST',
        'data': 'Json format of features',
        'Description': 'Json response from Solr'
    }
]


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status': 404}), 404)


@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'error': 'Internal server Error', 'status': 500}), 500)


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad Request Error, Please give valid input', 'status': 400, }), 400)


@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': 'Method not allowed , this URL takes POST method ', 'status': 405}), 405)


def make_error(status_code, message):
    response = jsonify({
        'status': status_code,
        'error': message,
    })
    response.status_code = status_code
    return response


class bitWise(Resource):
    # Index of API
    @app.route("/")
    def index():
        return jsonify({'docs': tasks})

    @app.route("/solr_db_content", methods=["GET"])
    def getjsonresponse():
        keyword = request.args.get('query')
        if request.args.get('content_type'):
            content_type = request.args.get('content_type')
        else:
            content_type = ""
        if request.args.get('num_doc'):
            num_doc = request.args.get('num_doc')
        else:
            num_doc = ""
        result = data_collection(keyword, content_type, num_doc)
        return jsonify(result['len_content'], result['final_out'])


if __name__ == "__main__":
    app.run(debug=True)

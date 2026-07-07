from extract_data import *
#from agent_gemini import Agent
from agent_openai import Agent
from RAG_model import *
import os
from model_methods import *
from model_methods import query_tracker
from error_handling import *
from flask import Flask, request, jsonify,  Response
from flask_cors import CORS
from config import SECRET_FLASK_KEY

app = Flask(__name__)
app.secret_key = SECRET_FLASK_KEY

CORS(app, supports_credentials=True) 

agent = Agent()
queryTracker = query_tracker()

global MAX_OPEN_MODEL_ALLOWED
MAX_OPEN_MODEL_ALLOWED = 5

global OPEN_MODELS
OPEN_MODELS = {}

@app.route('/api/models', methods=['GET'])
def get_available_models():
    models_list = show_models()

    return jsonify({"models": models_list})


def search_in_cache(my_model) :

    if my_model not in OPEN_MODELS.keys():

        document_chunks, data_library = choose_models(my_model, False)

        if len(OPEN_MODELS) == MAX_OPEN_MODEL_ALLOWED :
            model_to_remove = None
            min_queries = -1

            for model in OPEN_MODELS.keys() :
                if min_queries == -1 :
                    model_to_remove = model
                    min_queries = OPEN_MODELS[model]['queries_hit']
            
                else :
                    if OPEN_MODELS[model]['queries_hit'] < min_queries :
                        min_queries = OPEN_MODELS[model]['queries_hit']
                        model_to_remove = model

            OPEN_MODELS.pop(model_to_remove)

        OPEN_MODELS[my_model] = {
            'doc_chunks' : document_chunks,
            'data_lib' : data_library,
            'queries_hit' : 0
        }

@app.route('/api/query', methods = ['POST'])
def read_query():
    query_info_json = request.get_json()

    my_model = query_info_json.get('model')
    curr_query = query_info_json.get('query')

    print(my_model)
    print(curr_query)

    search_in_cache(my_model)

    queryTracker.set_model(my_model)
    queryTracker.set_query(curr_query)

    OPEN_MODELS[my_model]['queries_hit'] +=1

    return jsonify({"status ": "success", "model_used" : my_model, "received_query" :  curr_query}), 200


@app.route('/api/reply', methods = ['GET'])
def answer_query():

    for model in OPEN_MODELS.keys() :
        print(model)

    current_model = queryTracker.get_model()
    print(f"current model i am using {current_model}")

    curr_query = queryTracker.get_query()

    curr_data_lib = OPEN_MODELS[current_model]['data_lib']
    curr_doc_chunks = OPEN_MODELS[current_model]['doc_chunks']

    query_related_info = give_query_related_context(curr_query, curr_data_lib, curr_doc_chunks)

    print(query_related_info)

    route = agent.run("Router", curr_query)

    answer = agent.run(route, curr_query, query_related_info, queryTracker.get_history())

    queryTracker.set_history(curr_query, answer)

    payload = {
        'answer' : answer
    }
    return Response(response = json.dumps(payload), mimetype="application/json")


def append_model(model_name, document) :
    if model_name in OPEN_MODELS.keys():
        OPEN_MODELS.pop(model_name)
    
    model_dir = choose_models(model_name, True)

    only_append = True
    document_chunks, new_chunks_to_appends = chunk_doc(document, model_dir, only_append)
    data_library = place_chunk_in_vector_space(new_chunks_to_appends, model_dir, only_append)

def create_new_model(document, new_model_name) :
    dir_path = make_model(new_model_name)

    only_append = False
    document_chunks = chunk_doc(document, dir_path, only_append)
    data_library = place_chunk_in_vector_space(document_chunks, dir_path, only_append)

@app.route('/api/file', methods = ['POST'])
def create_append_model() :
    uploaded_file = request.files.get('file')
    model_name = request.form.get('model')
    new_model_name = request.form.get('newModelName')

    try :
        document = extract_Data(uploaded_file)
        if model_name == "Make new model" :
            create_new_model(document, new_model_name)

        else :
            append_model(model_name, document)

        return jsonify({'status' : 'received'}), 200
    
    except Exception as error :
        print(str(error))
        return jsonify({'error' : str(error)}), 400
    

if __name__ == "__main__":
    app.run(debug=True, port=5000) 
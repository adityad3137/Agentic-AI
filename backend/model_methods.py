from pathlib import Path
import os
import json
import faiss
from collections import deque
from config import DIR_PATH as dir_path

def show_models() :
    model_name = []
    for folder in Path(dir_path).iterdir():
        if folder.is_dir():
            model_name.append(folder.name)
    
    return model_name

def choose_models(model_chosen, pass_dir_name : bool):

    for folder in Path(dir_path).iterdir():
        if folder.is_dir() and folder.name == model_chosen :
            new_folder_path = os.path.join(dir_path, folder)

            if pass_dir_name == True :
                return new_folder_path

            with open(os.path.join(new_folder_path, "chunks.json"), "r") as f:
                doc_chunks = json.load(f)
            
            data_library = faiss.read_index(os.path.join(new_folder_path, "data_lib.index"))

            return doc_chunks, data_library
    
    raise FileNotFoundError(f"Model: {model_chosen} not found in existing model list")

def make_model(model_name):
    new_folder_path = os.path.join(dir_path, model_name)

    Path(new_folder_path).mkdir(parents=True, exist_ok=True)

    return new_folder_path

class query_tracker :
    _model_name = None
    _query = None
    _prev_conversations = deque()
    MAX_PREV_CONVERSATIONS_ALLOWED = 2

    @classmethod
    def set_model(cls, my_model) :
        if cls._model_name != my_model :
            cls._prev_conversations.clear()
            cls._model_name = my_model
    
    def get_model(cls) :
        return cls._model_name
    
    def set_query(cls, curr_query) :
        cls._query = curr_query
    
    def get_query(cls) :
        return cls._query
    
    def set_history(cls, query, answer):
        if len(cls._prev_conversations) == cls.MAX_PREV_CONVERSATIONS_ALLOWED:
            cls._prev_conversations.popleft()
        
        cls._prev_conversations.append({query : answer})
    
    def get_history(cls) :
        return cls._prev_conversations
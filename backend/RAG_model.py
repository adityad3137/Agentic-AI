from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os

def chunk_doc(document, dir_path, only_append : bool) :
    text_chunk = []

    split_doc = document.split()
    size_of_doc = len(split_doc)
    index = 0
    chunk_number = 0
    MAX_WORDS_PER_CHUNK = 500
    WORDS_FOR_CONTEXT = 50

    while index < size_of_doc :

        current_wordcnt = 0
        text_chunk.append("")

        if chunk_number > 0 :
            index -= WORDS_FOR_CONTEXT
    
        while current_wordcnt < MAX_WORDS_PER_CHUNK and index < size_of_doc :
            text_chunk[chunk_number] += split_doc[index] + " "
            index += 1
            current_wordcnt += 1

        chunk_number += 1

    if(only_append == False):
        with open(os.path.join(dir_path, "chunks.json"), "w") as f:
            json.dump(text_chunk, f, indent = 4)
        
        return text_chunk
    
    else :
        with open(os.path.join(dir_path, "chunks.json"), "r") as f:
                doc_chunks = json.load(f)
        
        doc_chunks += text_chunk

        with open(os.path.join(dir_path, "chunks.json"), "w") as f:
            json.dump(doc_chunks, f, indent = 4)

        return doc_chunks, text_chunk

def place_chunk_in_vector_space(text_chunk, dir_path, only_append : bool) :

    model = SentenceTransformer("all-MiniLM-L6-v2")

    raw_embeddings = model.encode(text_chunk)
    tabulated_embeddings = np.array(raw_embeddings).astype('float32')

    if only_append == False :
        data_library = faiss.IndexFlatL2(384)

    else :
        data_library = faiss.read_index(os.path.join(dir_path, "data_lib.index"))
    
    data_library.add(tabulated_embeddings)

    faiss.write_index(data_library, os.path.join(dir_path, "data_lib.index"))

    return data_library

def give_query_related_context(query, data_library, document_chunks) :

    model = SentenceTransformer("all-MiniLM-L6-v2")

    query_list = [query]

    query_embedding = model.encode(query_list)
    query_embedding_structured = np.array(query_embedding).astype('float32')

    k = 5
    distance, indices = data_library.search(query_embedding_structured, k)

    print(indices)

    filtered_indices = indices[indices > -1]

    query_related_info = ""
    for ind in filtered_indices:
        query_related_info += document_chunks[ind] + "\n\n"

    return query_related_info
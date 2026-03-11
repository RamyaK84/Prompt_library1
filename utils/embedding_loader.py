import numpy as np
import json
import os

_model = None
_embeddings = None
_prompt_ids = None

def get_model():
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            print(f"Warning: Could not load sentence-transformers model: {e}")
            _model = None
    return _model

def get_prompt_embeddings(prompts):
    global _embeddings, _prompt_ids
    if _embeddings is None:
        model = get_model()
        if model is None:
            return None, None
        texts = [f"{p['title']} {p['category']} {p['preview']} {' '.join(p.get('tags', []))}" for p in prompts]
        _embeddings = model.encode(texts)
        _prompt_ids = [p['id'] for p in prompts]
    return _embeddings, _prompt_ids

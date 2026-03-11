from utils.prompt_loader import load_prompts
from utils.embedding_loader import get_model, get_prompt_embeddings
import numpy as np

def semantic_search(query, top_k=5):
    prompts = load_prompts()
    model = get_model()
    if model is None:
        # Fallback to keyword search
        from services.search_service import keyword_search
        return keyword_search(query)[:top_k]
    query_embedding = model.encode([query])
    embeddings, prompt_ids = get_prompt_embeddings(prompts)
    if embeddings is None:
        from services.search_service import keyword_search
        return keyword_search(query)[:top_k]
    from sklearn.metrics.pairwise import cosine_similarity
    scores = cosine_similarity(query_embedding, embeddings)[0]
    top_indices = np.argsort(scores)[::-1][:top_k]
    results = []
    for idx in top_indices:
        pid = prompt_ids[idx]
        for p in prompts:
            if p['id'] == pid:
                results.append({**p, 'similarity': float(scores[idx])})
                break
    return results

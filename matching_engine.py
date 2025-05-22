import numpy as np
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from models import MatchResult, CandidateProfile
from utils import preprocess_text

class MatchingEngine:
    """Motor de matching entre candidatos e vagas"""
    
    def __init__(self):
        # Configuração ULTRA LOW MEMORY (2-4GB RAM)
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            min_df=2,
            max_df=0.95,
            stop_words='english',
            ngram_range=(1, 1),
            dtype=np.float32
        )
    
    def find_best_matches(self, candidates: List[CandidateProfile], vagas: Dict, top_n: int = 10) -> List[MatchResult]:
        """Encontra os melhores matches entre candidatos e vagas"""
        if not candidates:
            raise ValueError("Nenhum candidato carregado")
        
        cv_texts = [c.cv_processed for c in candidates]
        vaga_texts = []
        vaga_ids = []
        
        for id_vaga, data in vagas.items():
            titulo = data.get("informacoes_basicas", {}).get("titulo_vaga", "")
            if titulo:
                processed_title = preprocess_text(titulo)
                vaga_texts.append(processed_title)
                vaga_ids.append(id_vaga)
        
        if not vaga_texts:
            raise ValueError("Nenhuma vaga com título encontrada")
        
        cv_matrix = self.vectorizer.fit_transform(cv_texts)
        vaga_matrix = self.vectorizer.transform(vaga_texts)
        
        similarities = self._calculate_similarities_batched(cv_matrix, vaga_matrix)
        
        matches = []
        for i, candidate in enumerate(candidates):
            best_match_idx = similarities[i].argmax()
            matches.append(MatchResult(
                candidato_id=candidate.id,
                vaga_id=vaga_ids[best_match_idx],
                similaridade=float(similarities[i][best_match_idx])
            ))
        
        del cv_matrix, vaga_matrix, similarities
        
        return sorted(matches, key=lambda x: x.similaridade, reverse=True)[:top_n]
    
    def _calculate_similarities_batched(self, cv_matrix, vaga_matrix, batch_size: int = 25):
        """Calcula similaridades em lotes para economizar memória"""
        n_candidates = cv_matrix.shape[0]
        n_vagas = vaga_matrix.shape[0]
        similarities = np.zeros((n_candidates, n_vagas), dtype=np.float32)
        
        for i in range(0, n_candidates, batch_size):
            end_i = min(i + batch_size, n_candidates)
            batch_similarities = cosine_similarity(cv_matrix[i:end_i], vaga_matrix)
            similarities[i:end_i] = batch_similarities.astype(np.float32)
        
        return similarities
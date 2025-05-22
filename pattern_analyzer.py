import numpy as np
from typing import List, Dict
from collections import Counter, defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from models import CandidateProfile

class PatternAnalyzer:
    """Analisador de padrões de candidatos bem-sucedidos"""
    
    def __init__(self, stop_words: set):
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            min_df=2,
            max_df=0.95,
            stop_words='english',
            ngram_range=(1, 1),
            dtype=np.float32
        )
        self.n_clusters = 2
        self.kmeans = None
        self.stop_words = stop_words
    
    def analyze_successful_patterns(self, candidates: List[CandidateProfile], prospects: Dict) -> Dict:
        """Analisa padrões de candidatos bem-sucedidos usando clustering"""
        successful_ids = set()
        for data in prospects.values():
            for prospect in data.get("prospects", []):
                if prospect.get("situacao_candidado") == "Encaminhado ao Requisitante":
                    successful_ids.add(str(prospect.get("codigo", "")))
        
        successful_candidates = [c for c in candidates if c.id in successful_ids]
        
        if len(successful_candidates) < self.n_clusters:
            successful_candidates = candidates[:25]
        
        if len(successful_candidates) > 25:
            successful_candidates = successful_candidates[:25]
        
        cv_texts = [c.cv_processed for c in successful_candidates]
        cv_matrix = self.vectorizer.fit_transform(cv_texts)
        
        self.kmeans = KMeans(
            n_clusters=min(self.n_clusters, len(successful_candidates)), 
            random_state=42, 
            n_init=3,
            max_iter=50,
            algorithm='elkan'
        )
        
        if cv_matrix.shape[0] * cv_matrix.shape[1] < 50000:
            clusters = self.kmeans.fit_predict(cv_matrix.toarray())
        else:
            clusters = self.kmeans.fit_predict(cv_matrix)
        
        for i, candidate in enumerate(successful_candidates):
            candidate.cluster_id = int(clusters[i])
        
        cluster_keywords = self._extract_cluster_keywords(successful_candidates)
        
        del cv_matrix
        
        return {
            "candidates": [c.id for c in successful_candidates],
            "clusters": clusters.tolist(),
            "keywords": cluster_keywords
        }
    
    def _extract_cluster_keywords(self, candidates: List[CandidateProfile], top_k: int = 5) -> Dict[int, List[str]]:
        """Extrai palavras-chave mais importantes por cluster"""
        cluster_keywords = defaultdict(list)
        
        for candidate in candidates:
            if candidate.cluster_id is not None:
                words = candidate.cv_processed.split()
                filtered_words = [
                    word for word in words 
                    if word not in self.stop_words and len(word) > 2
                ]
                cluster_keywords[candidate.cluster_id].extend(filtered_words)
        
        result = {}
        for cluster_id, words in cluster_keywords.items():
            word_counts = Counter(words)
            result[cluster_id] = [word for word, _ in word_counts.most_common(top_k)]
        
        return result
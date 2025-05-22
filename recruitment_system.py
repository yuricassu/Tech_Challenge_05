import warnings
from typing import List, Dict
from models import MatchResult, CandidateProfile
from data_loader import DataLoader
from matching_engine import MatchingEngine
from pattern_analyzer import PatternAnalyzer
from utils import setup_nltk

warnings.filterwarnings('ignore')

class RecruitmentSystem:
    """Sistema principal de recrutamento e matching"""
    
    def __init__(self):
        self.max_candidates_batch = 50
        self.max_text_length = 500
        
        self.candidates = []
        self.vagas = {}
        self.prospects = {}
        self.stop_words = setup_nltk()
        
        # Inicializa componentes
        self.data_loader = DataLoader(self.max_candidates_batch)
        self.matching_engine = MatchingEngine()
        self.pattern_analyzer = PatternAnalyzer(self.stop_words)
    
    def load_data_from_files(self):
        """Carrega dados dos arquivos da pasta files"""
        success, message, candidates, vagas, prospects = self.data_loader.load_data_from_files()
        
        if success:
            self.candidates = candidates
            self.vagas = vagas
            self.prospects = prospects
        
        return success, message
    
    def find_best_matches(self, top_n: int = 10) -> List[MatchResult]:
        """Encontra os melhores matches entre candidatos e vagas"""
        return self.matching_engine.find_best_matches(self.candidates, self.vagas, top_n)
    
    def analyze_successful_patterns(self) -> Dict:
        """Analisa padrões de candidatos bem-sucedidos usando clustering"""
        return self.pattern_analyzer.analyze_successful_patterns(self.candidates, self.prospects)
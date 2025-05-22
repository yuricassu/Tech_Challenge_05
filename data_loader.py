import json
import os
from typing import Dict, List, Tuple
from models import CandidateProfile
from utils import preprocess_text

class DataLoader:
    """Classe responsável pelo carregamento e processamento dos dados"""
    
    def __init__(self, max_candidates_batch: int = 50):
        self.max_candidates_batch = max_candidates_batch
    
    def load_data_from_files(self) -> Tuple[bool, str, List[CandidateProfile], Dict, Dict]:
        """Carrega dados dos arquivos da pasta files"""
        try:
            # Define os caminhos dos arquivos
            base_path = "files"
            applicants_path = os.path.join(base_path, "applicants.json")
            vagas_path = os.path.join(base_path, "vagas.json")
            prospects_path = os.path.join(base_path, "prospects.json")
            
            # Verifica se os arquivos existem
            if not all(os.path.exists(path) for path in [applicants_path, vagas_path, prospects_path]):
                missing_files = [path for path in [applicants_path, vagas_path, prospects_path] if not os.path.exists(path)]
                return False, f"Arquivos não encontrados: {missing_files}", [], {}, {}
            
            # Lê os arquivos JSON
            with open(applicants_path, 'r', encoding='utf-8') as f:
                applicants = json.load(f)
            
            with open(vagas_path, 'r', encoding='utf-8') as f:
                vagas = json.load(f)
            
            with open(prospects_path, 'r', encoding='utf-8') as f:
                prospects = json.load(f)
            
            # Processa candidatos
            candidates = self._process_candidates(applicants)
            return True, f"Carregados: {len(candidates)} candidatos, {len(vagas)} vagas", candidates, vagas, prospects
            
        except Exception as e:
            return False, f"Erro ao carregar dados: {e}", [], {}, {}
    
    def _process_candidates(self, applicants: Dict) -> List[CandidateProfile]:
        """Processa dados dos candidatos em lotes para economizar memória"""
        candidates = []
        processed_count = 0
        
        for id_candidato, data in applicants.items():
            cv_text = data.get("cv_pt", "")
            if cv_text:
                if processed_count >= self.max_candidates_batch:
                    break
                    
                candidates.append(CandidateProfile(
                    id=id_candidato,
                    cv_processed=preprocess_text(cv_text),
                    cv_original=cv_text[:500]
                ))
                processed_count += 1
                
        return candidates
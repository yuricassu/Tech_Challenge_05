from dataclasses import dataclass
from typing import Optional

@dataclass
class MatchResult:
    """Classe para armazenar resultados de matching"""
    candidato_id: str
    vaga_id: str
    similaridade: float

@dataclass
class CandidateProfile:
    """Perfil do candidato com informações processadas"""
    id: str
    cv_processed: str
    cv_original: str
    cluster_id: Optional[int] = None
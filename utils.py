import re
import nltk
from nltk.corpus import stopwords

def setup_nltk():
    """Configura NLTK e baixa recursos necessários"""
    try:
        nltk.download('stopwords', quiet=True)
        return set(stopwords.words('portuguese'))
    except:
        return set()

def preprocess_text(text: str, max_length: int = 500) -> str:
    """Pré-processa texto removendo caracteres especiais e convertendo para minúsculas"""
    if not text:
        return ""
    
    text = text.lower()
    
    if len(text) > max_length:
        text = text[:max_length]
        
    text = re.sub(r'[^a-zA-Z0-9\sáàâãéèêíìîóòôõúùûç]', '', text)
    
    words = text.split()
    words = [w for w in words if len(w) > 2]
    
    return ' '.join(words)
import streamlit as st
import pandas as pd
from typing import List
from models import MatchResult

def initialize_session_state():
    """Inicializa variáveis do session state"""
    if 'recruitment_system' not in st.session_state:
        st.session_state.recruitment_system = None
    if 'matches' not in st.session_state:
        st.session_state.matches = None
    if 'cluster_analysis' not in st.session_state:
        st.session_state.cluster_analysis = None
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = False

def render_matches_tab():
    """Renderiza a aba de análise de matches"""
    st.header("🔍 Análise de Matches")
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        top_n = st.slider("Número de matches", 5, 20, 16)
        
        if st.button("🎯 Analisar Matches", type="primary"):
            with st.spinner("Analisando matches..."):
                st.session_state.matches = st.session_state.recruitment_system.find_best_matches(top_n)
    
    with col1:
        if st.session_state.matches:
            st.subheader(f"🏆 Top {len(st.session_state.matches)} Matches")
            
            # Cria DataFrame para exibição
            matches_data = []
            for i, match in enumerate(st.session_state.matches, 1):
                matches_data.append({
                    "Ranking": i,
                    "Candidato ID": match.candidato_id,
                    "Vaga ID": match.vaga_id,
                    "Similaridade": f"{match.similaridade:.3f}"
                })
            
            df = pd.DataFrame(matches_data)
            st.dataframe(df, use_container_width=True)

def render_patterns_tab():
    """Renderiza a aba de análise de padrões"""
    st.header("📈 Padrões de Candidatos Bem-sucedidos")
    
    if st.button("🔬 Analisar Padrões", type="primary"):
        with st.spinner("Analisando padrões de sucesso..."):
            st.session_state.cluster_analysis = st.session_state.recruitment_system.analyze_successful_patterns()
    
    if st.session_state.cluster_analysis:
        st.subheader("🎯 Clusters Identificados")
        
        for cluster_id, keywords in st.session_state.cluster_analysis["keywords"].items():
            with st.expander(f"Cluster {cluster_id}"):
                st.write("**Palavras-chave principais:**")
                st.write(", ".join(keywords))
        
        # Estatísticas
        st.subheader("📊 Estatísticas")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Candidatos Analisados", len(st.session_state.cluster_analysis["candidates"]))
        
        with col2:
            st.metric("Clusters Formados", len(st.session_state.cluster_analysis["keywords"]))
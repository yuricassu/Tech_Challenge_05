import streamlit as st
from recruitment_system import RecruitmentSystem
from ui_components import initialize_session_state, render_matches_tab, render_patterns_tab

def main():
    """Função principal do Streamlit"""
    st.set_page_config(
        page_title="Sistema de Recrutamento IA",
        page_icon="🎯",
        layout="wide"
    )
    
    initialize_session_state()
    
    st.title("🎯 Sistema de Recrutamento com IA")
    st.markdown("**Matching de candidatos e análise de padrões**")
    
    # Carregamento automático dos dados
    if not st.session_state.data_loaded:
        with st.spinner("Carregando dados automaticamente..."):
            st.session_state.recruitment_system = RecruitmentSystem()
            success, message = st.session_state.recruitment_system.load_data_from_files()
            
            if success:
                st.session_state.data_loaded = True
                st.success(message)
            else:
                st.error(message)
                st.stop()
    
    # Tabs principais
    tab1, tab2 = st.tabs(["🔍 Análise de Matches", "📈 Padrões de Sucesso"])
    
    with tab1:
        render_matches_tab()
    
    with tab2:
        render_patterns_tab()
    
    # Footer
    st.markdown("---")
    st.markdown("**Sistema de Recrutamento com IA** - Configuração Ultra Low Memory para otimização de recursos")

if __name__ == "__main__":
    main()
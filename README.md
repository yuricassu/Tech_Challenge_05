# Tech_Challenge_05

## Grupo 25

### Membros:
- Yuri Cassu
- Leonardo Adelmo Souza
- Diogo Abreu de Siqueira
- Karen dos Santos

## Link Streamlit:
https://techchallenge05-data-analytics-grupo-25.streamlit.app/

## Link do Vídeo do projeto:
https://www.youtube.com/watch?v=lkF8NyNznTk

## 🎯 Sistema de Recrutamento com IA

Um sistema inteligente de matching entre candidatos e vagas que utiliza algoritmos de Machine Learning e Processamento de Linguagem Natural para otimizar processos de recrutamento.

## 📁 Estrutura do Projeto

```
recruitment-ai-system/
├── app.py                    # Aplicação principal
├── models.py                 # Classes de dados
├── utils.py                  # Funções utilitárias
├── data_loader.py            # Carregamento de dados
├── matching_engine.py        # Motor de matching
├── pattern_analyzer.py       # Análise de padrões
├── recruitment_system.py     # Sistema principal
├── ui_components.py          # Componentes de interface
├── requirements.txt          # Dependências
├── README.md                 # Este arquivo
└── files/                    # Pasta de dados
    ├── applicants.json       # Dados dos candidatos
    ├── vagas.json            # Dados das vagas
    └── prospects.json        # Dados de prospects
```

## ⚡ Otimizações de Performance

### Configurações de Baixa Memória

- **TF-IDF limitado:** Máximo de 500 features
- **Processamento em lotes:** 25-50 candidatos por vez
- **Texto truncado:** Máximo de 500 caracteres
- **Clustering otimizado:** K-Means com configurações eficientes

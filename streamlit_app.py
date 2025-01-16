import streamlit as st
import pandas as pd

# --------------------- Configurazione della Pagina ---------------------
st.set_page_config(
    page_title="Data Agent",
    page_icon="💬",
    layout="wide"  # Imposta il layout su wide
)

# --------------------- Iniezione CSS Personalizzato per Schema di Colori e Estetica ---------------------
def inject_css():
    st.markdown("""
    <style>
    /* Definisci la palette di colori */
    :root {
        --primary-color: #2C3E50; /* Dark Blue for primary elements */
        --secondary-color: #3498DB; /* Blue for buttons and highlights */
        --accent-color: #E74C3C; /* Red for accents and alerts */
        --background-color: #FFFFFF; /* White background */
        --text-color: #2C3E50; /* Dark text */
        --light-gray: #ECF0F1; /* Light gray for borders and backgrounds */
        --box-shadow: rgba(0, 0, 0, 0.1);
    }

    /* Stile della Barra Laterale */
    .css-1d391kg {
        background-color: var(--light-gray);
    }

    /* Stile di Intestazione e Titolo */
    .css-1aumxhk {
        color: var(--primary-color);
    }

    /* Stile dei Pulsanti */
    .stButton>button {
        background-color: var(--secondary-color);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        transition: background-color 0.3s;
    }

    .stButton>button:hover {
        background-color: var(--primary-color);
        color: white;
    }

    /* Stile dell'Header dell'Espanditore */
    .css-1r6slb0 .streamlit-expanderHeader {
        color: var(--primary-color);
    }

    /* Stile dei Link */
    a {
        color: var(--secondary-color);
        text-decoration: none;
    }

    a:hover {
        text-decoration: underline;
        color: var(--accent-color);
    }

    /* Stile del Footer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: var(--background-color);
        color: var(--text-color);
        text-align: center;
        padding: 10px;
        border-top: 1px solid var(--light-gray);
    }

    /* Etichette delle Checkbox */
    .stCheckbox label {
        color: var(--text-color);
    }

    /* Bordo dei Campi di Testo e Aree di Testo */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        border: 1px solid var(--light-gray);
        border-radius: 5px;
        padding: 8px;
        color: var(--text-color);
        background-color: #FFFFFF;
    }

    /* Stile dei Pulsanti di Download */
    .stDownloadButton>button {
        background-color: var(--secondary-color);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 8px 16px;
    }

    .stDownloadButton>button:hover {
        background-color: var(--primary-color);
        color: white;
    }

    /* Stile dei Messaggi della Chat */
    .user-message {
        background-color: #F0F8FF; /* Alice Blue */
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 80%;
        align-self: flex-end;
        box-shadow: 2px 2px 5px var(--box-shadow);
        color: var(--text-color);
    }

    .assistant-message {
        background-color: #FAFAD2; /* Light Goldenrod Yellow */
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 80%;
        align-self: flex-start;
        box-shadow: 2px 2px 5px var(--box-shadow);
        color: var(--text-color);
    }

    .chat-container {
        display: flex;
        flex-direction: column;
    }

    /* Scrollbar per la Cronologia delle Chat */
    .sidebar-chat-history {
        max-height: 300px;
        overflow-y: auto;
        padding-right: 10px;
    }

    /* Stile per le Domande Suggerite */
    .suggested-questions a {
        display: block;
        margin-bottom: 5px;
        font-size: 14px;
        padding: 8px;
        background-color: #EBF5FB; /* Light Blue */
        border-radius: 5px;
        transition: background-color 0.3s;
        color: var(--primary-color);
    }

    .suggested-questions a:hover {
        background-color: #D6EAF8; /* Slightly darker light blue */
        color: var(--accent-color);
    }

    /* Stile dei Box */
    .box {
        background-color: var(--background-color);
        border: 1px solid var(--light-gray);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 2px 2px 10px var(--box-shadow);
        color: var(--text-color);
    }

    /* Stile per le Domande Correlate */
    .related-question a {
        font-size: 16px;
        color: var(--secondary-color);
    }

    .related-question a:hover {
        color: var(--accent-color);
    }

    /* Stile delle Checkbox */
    .stCheckbox input[type=checkbox] {
        accent-color: var(--secondary-color);
    }

    /* Stile delle Text Area */
    .stTextArea textarea {
        color: var(--text-color);
    }

    /* Stile dei Titoli */
    h1, h2, h3, h4, h5, h6 {
        color: var(--primary-color);
    }

    </style>
    """, unsafe_allow_html=True)

inject_css()

# --------------------- Inizializzazione dello Stato della Sessione ---------------------
# Inizializza le chiavi necessarie in st.session_state
if 'selected_feedback' not in st.session_state:
    st.session_state['selected_feedback'] = []

if 'additional_feedback_expander' not in st.session_state:
    st.session_state['additional_feedback_expander'] = ""

if 'chat_history' not in st.session_state:
    # Prepopola la cronologia della chat con una domanda e risposta iniziale
    st.session_state['chat_history'] = [
        ("user", "Puoi fornirmi la granularità delle tabelle per il bilancio?"),
        ("assistant", """
**Ecco la granularità delle tabelle relative al bilancio:**

| Tabella               | Granularità                                  |
|-----------------------|----------------------------------------------|
| FIN_DATA_Q1_REVENUE   | Dipartimento e mese                          |
| FIN_DATA_Q2_EXPENSES  | Dipartimento, categoria di spesa e trimestre  |
| FIN_DATA_Q3_PROFIT    | Dipartimento, prodotto e anno                |
| FIN_DATA_Q4_ASSETS    | Categoria di asset e mese                    |
| FIN_DATA_Q5_LIABILITIES | Tipo di passività e anno                  |
        """)
    ]

# --------------------- Funzione per Generare Domande Suggerite ---------------------
def generate_suggested_questions(latest_question):
    """
    Genera domande suggerite basate sull'ultima domanda dell'utente.
    In un'applicazione reale, questa potrebbe integrare un modello NLP per generare domande pertinenti.
    Per questo esempio, utilizziamo una logica semplice basata su parole chiave.
    """
    keywords = latest_question.lower().split()
    suggested = set()

    if "data lineage" in keywords:
        suggested.update([
            "Come il data lineage migliora la qualità dei dati nel bilancio?",
            "Quali sono le sfide nell'implementazione del data lineage?",
            "Strumenti avanzati per il data lineage nelle istituzioni finanziarie?"
        ])
    elif "excel" in keywords:
        suggested.update([
            "Come utilizzare Excel per analizzare il data lineage?",
            "Quali sono le migliori pratiche di Excel per la gestione dei dati finanziari?",
            "Integrazione di Excel con sistemi di data lineage"
        ])
    elif "granularità" in keywords:
        suggested.update([
            "Come definire la granularità delle tabelle finanziarie?",
            "Quali sono i vantaggi di una corretta granularità nelle tabelle finanziarie?",
            "Strumenti per gestire la granularità dei dati nelle finanze?"
        ])
    else:
        suggested.update([
            "Cos'è il data lineage e perché è importante per il bilancio?",
            "Come implementare efficacemente il data lineage nelle tabelle finanziarie?",
            "Quali strumenti sono disponibili per monitorare il data lineage in un istituto finanziario?"
        ])

    return list(suggested)[:3]  # Limita a 3 domande

# --------------------- Barra Laterale con Logo, Cronologia Domande e Domande Suggerite ---------------------
with st.sidebar:
    # Aggiungi il logo di Cassa Depositi e Prestiti (CDP)
    logo_url = "https://www.kindpng.com/picc/m/612-6127858_cassa-depositi-e-prestiti-logo-hd-png-download.png"  # URL aggiornato del logo
    st.image(logo_url, use_container_width=True)  # Updated parameter

    st.title("Data Agent")
    st.markdown("**Applicazione di Chatbot con Funzionalità Avanzate**")
    st.markdown("---")

    # Sezione: Cronologia Domande
    st.markdown("### 📜 Cronologia Domande")
    if st.session_state.chat_history:
        with st.container():
            history_container = st.container()
            history_container.markdown('<div class="sidebar-chat-history">', unsafe_allow_html=True)
            for idx, (sender, message) in enumerate(st.session_state.chat_history):
                if sender == "user":
                    history_container.markdown(f"""
                    <div class="box">
                        <strong>Tu:</strong> {message}
                    </div>
                    """, unsafe_allow_html=True)
            history_container.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("Nessuna domanda precedente.")

    st.markdown("---")

    # Sezione: Domande Suggerite
    st.markdown("### 💡 Domande Suggerite")
    if st.session_state.chat_history:
        latest_user_question = next((msg for sender, msg in reversed(st.session_state.chat_history) if sender == "user"), "")
        suggested_questions = generate_suggested_questions(latest_user_question)
    else:
        suggested_questions = [
            "Cos'è il data lineage e perché è importante per il bilancio?",
            "Come implementare efficacemente il data lineage nelle tabelle finanziarie?",
            "Quali strumenti sono disponibili per monitorare il data lineage in un istituto finanziario?"
        ]

    with st.container():
        for question in suggested_questions:
            st.markdown(f"""
            <div class="box suggested-questions">
                <a href="#">{question}</a>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Bottoni Esistenti
    st.markdown("🔍 **Esplora**")
    st.button("Fonti")
    st.button("Domande Correlate")

# --------------------- Contenuto Principale ---------------------
st.title("💬 Data Agent")
st.write("")

# --------------------- Sezione Chatbot ---------------------
# Placeholder per i messaggi della chat
chat_placeholder = st.empty()

# Funzione per generare la risposta dell'assistente
def generate_response(user_input):
    """
    Genera una risposta basata sull'input dell'utente.
    In un'applicazione reale, questa funzione potrebbe integrare un modello NLP o altre logiche di business.
    Per questo esempio, una risposta predefinita focalizzata sulla granularità delle tabelle è usata.
    """
    # Risposta focalizzata sulla granularità delle tabelle con embedded dataframe
    response_text = """
**Ecco la granularità delle tabelle relative al bilancio:**

| Tabella               | Granularità                                  |
|-----------------------|----------------------------------------------|
| FIN_DATA_Q1_REVENUE   | Dipartimento e mese                          |
| FIN_DATA_Q2_EXPENSES  | Dipartimento, categoria di spesa e trimestre  |
| FIN_DATA_Q3_PROFIT    | Dipartimento, prodotto e anno                |
| FIN_DATA_Q4_ASSETS    | Categoria di asset e mese                    |
| FIN_DATA_Q5_LIABILITIES | Tipo di passività e anno                  |
    """

    # Creazione del dataframe per visualizzazione
    data = {
        "Tabella": [
            "FIN_DATA_Q1_REVENUE",
            "FIN_DATA_Q2_EXPENSES",
            "FIN_DATA_Q3_PROFIT",
            "FIN_DATA_Q4_ASSETS",
            "FIN_DATA_Q5_LIABILITIES"
        ],
        "Granularità": [
            "Dipartimento e mese",
            "Dipartimento, categoria di spesa e trimestre",
            "Dipartimento, prodotto e anno",
            "Categoria di asset e mese",
            "Tipo di passività e anno"
        ]
    }
    df = pd.DataFrame(data)

    return response_text, df

# Funzione per visualizzare la cronologia della chat utilizzando st.markdown e st.dataframe
def display_chat():
    if st.session_state.chat_history:
        with chat_placeholder.container():
            for sender, message in st.session_state.chat_history:
                if sender == "user":
                    st.markdown(f'<div class="user-message">{message}</div>', unsafe_allow_html=True)
                else:
                    # Verifica se il messaggio è una tuple con testo e dataframe
                    if isinstance(message, tuple) and len(message) == 2:
                        text, df = message
                        st.markdown(f'<div class="assistant-message">{text}</div>', unsafe_allow_html=True)
                        st.dataframe(df)
                    else:
                        st.markdown(f'<div class="assistant-message">{message}</div>', unsafe_allow_html=True)

# Visualizza la cronologia della chat
display_chat()

# Campo di input per l'utente
user_input = st.text_input("Tu:", key="user_input")

if user_input:
    # Aggiungi la domanda dell'utente alla cronologia
    st.session_state.chat_history.append(("user", user_input))
    
    # Genera la risposta dell'assistente
    assistant_response = generate_response(user_input)
    st.session_state.chat_history.append(("assistant", assistant_response))
    
    # Aggiorna la visualizzazione della chat
    display_chat()

# --------------------- Sezione Fonti con Icone Realistiche e Solo File Excel e PPT ---------------------
with st.expander("📚 Fonti", expanded=False):
    st.markdown("Questi sono i file Excel e PowerPoint che forniscono informazioni dettagliate relative al data lineage delle tabelle finanziarie. Espandi per visualizzare le fonti:")

    # Lista dei file forniti
    all_files = [
        "Financial_Report_Q1_2024.xlsx",
        "Budget_Presentation_Q2_2024.pptx",
        "Annual_Summary_2023.xlsx",
        "Investment_Strategy_2024.pptx",
        "Market_Analysis_2023.xlsx",
        "Strategy_Plan_2024.pptx",
        "Expense_Report_Q3_2024.xlsx",
        "Revenue_Forecast_Q4_2024.xlsx",
        "Operational_Overview_2024.xlsx",
        "Risk_Assessment_2024.xlsx",
        "miscellaneous_notes.txt"
    ]

    # Seleziona solo un file Excel e uno PowerPoint
    selected_files = {
        "excel": "Financial_Report_Q1_2024.xlsx",
        "pptx": "Budget_Presentation_Q2_2024.pptx"
    }

    # Funzione per simulare il recupero delle fonti selezionate
    def get_selected_sources():
        sources = []
        for file_type, file_name in selected_files.items():
            if file_type == "excel":
                publisher = "Finance Analytics Team"
                date = "10 Gennaio 2024"
                summary = f"Descrizione dettagliata del file {file_name}."
            elif file_type == "pptx":
                publisher = "Strategy Department"
                date = "15 Gennaio 2024"
                summary = f"Presentazione dettagliata del file {file_name}."
            else:
                continue  # Salta i tipi di file non supportati
            
            sources.append({
                "title": file_name,
                "link": f"https://example.com/files/{file_name}",
                "summary": summary,
                "publisher": publisher,
                "date": date,
                "file_type": file_type
            })
        return sources

    sources = get_selected_sources()

    # Mappatura dei tipi di file alle icone realistiche
    file_icons = {
        "excel": "https://img.icons8.com/color/48/000000/microsoft-excel-2019--v1.png",
        "pptx": "https://img.icons8.com/color/48/000000/microsoft-powerpoint-2019--v1.png"
    }

    # Visualizza ogni fonte selezionata con l'icona appropriata e link mock
    for source in sources:
        icon_url = file_icons.get(source["file_type"], "https://img.icons8.com/ios-filled/50/000000/file.png")  # Icona di default se il tipo di file non è trovato
        # Costruisci il markdown con l'icona e il titolo cliccabile
        source_markdown = f"""
        <div class="box">
            <div style="display: flex; align-items: center;">
                <img src="{icon_url}" alt="{source['file_type']} icon" style="width:24px;height:24px;margin-right:10px;">
                <a href="{source['link']}" target="_blank" style="font-size: 18px; text-decoration: none; color: var(--secondary-color);">{source['title']}</a>
            </div>
            <div style="margin-left:34px; margin-top:10px;">
                <strong>Editore:</strong> {source['publisher']}<br>
                <strong>Data:</strong> {source['date']}<br>
                <strong>Sintesi:</strong> {source['summary']}
            </div>
        </div>
        """
        st.markdown(source_markdown, unsafe_allow_html=True)

# --------------------- Sezione Feedback con Espanditore ---------------------
with st.expander("🛠️ Fornisci Feedback", expanded=False):
    st.markdown("**Aiutaci a Migliorare Questa Risposta**")
    st.markdown("Seleziona tutte le opzioni applicabili:")

    # Opzioni di feedback
    feedback_options = {
        "imprecise": "⚠️ Impréciso",
        "not_updated": "🔄 Non aggiornato",
        "too_short": "📏 Troppo breve",
        "too_long": "📜 Troppo lungo",
        "harmful_offensive": "🚨 Danno o offensivo",
        "not_useful": "❌ Non utile"
    }

    # Disposizione delle checkbox in tre colonne
    cols = st.columns(3)
    for idx, (key, label) in enumerate(feedback_options.items()):
        with cols[idx % 3]:
            if st.checkbox(label, key=f"checkbox_{key}"):
                if key not in st.session_state['selected_feedback']:
                    st.session_state['selected_feedback'].append(key)
            else:
                if key in st.session_state['selected_feedback']:
                    st.session_state['selected_feedback'].remove(key)

    # Area di testo per feedback aggiuntivo
    additional_feedback = st.text_area("Come possiamo migliorare la risposta? (Opzionale)", height=100, key="additional_feedback_expander")

    # Pulsanti Invia e Annulla
    submit_cancel_cols = st.columns(2)
    with submit_cancel_cols[0]:
        if st.button("Invia Feedback", key="submit_feedback_expander"):
            if st.session_state['selected_feedback']:
                # Gestisci il feedback (es. salva nel database o invia tramite email)
                st.success("Grazie per il tuo feedback!")
                # Resetta lo stato del feedback
                st.session_state['selected_feedback'] = []
                st.session_state['additional_feedback_expander'] = ""
                st.experimental_rerun()
            else:
                st.warning("Per favore, seleziona almeno un'opzione di feedback.")
    with submit_cancel_cols[1]:
        if st.button("Annulla Feedback", key="cancel_feedback_expander"):
            st.session_state['selected_feedback'] = []
            st.session_state['additional_feedback_expander'] = ""
            st.experimental_rerun()

# --------------------- Sezione Domande Correlate ---------------------
st.subheader("🔗 Domande Correlate")
related_questions = [
    "Cos'è il data lineage e perché è importante per il bilancio?",
    "Come implementare efficacemente il data lineage nelle tabelle finanziarie?",
    "Quali strumenti sono disponibili per monitorare il data lineage in un istituto finanziario?"
]
for question in related_questions:
    st.markdown(f"""
    <div class="box related-question">
        <a href="#">{question}</a>
    </div>
    """, unsafe_allow_html=True)

# --------------------- Sezione Footer ---------------------
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: var(--background-color);
    color: var(--text-color);
    text-align: center;
    padding: 10px;
    border-top: 1px solid var(--light-gray);
}
</style>
<div class="footer">
    <p>© 2024 Cassa Depositi e Prestiti (CDP). Tutti i diritti riservati.</p> 
</div>
""", unsafe_allow_html=True)

# 🧠 Math Question Difficulty Estimator (Level 1–5)

This repository implements a **semantic search + LLM-based pipeline** to estimate the **difficulty level (1–5)** of a given **math question and answer pair**.

---

## 🧩 Overview

The system works by combining:

- **🔍 Qdrant** as a semantic search engine to retrieve similar labeled problems.
- **🧠 OpenAI GPT** as a reasoning model to predict difficulty, using retrieved examples as context.

---

## 📥 Input

You provide a new **math problem (question + answer)**.  
The system returns a **difficulty score (1 to 5)**.

---

## 🧪 Example Flow

```text
Input:
Q: What is the derivative of x^3?
A: 3x^2

→ Output: Difficulty level: 2
```

---

## 📈 RAG Pipeline – Dataflow Diagram

```mermaid
flowchart TD
    A(["📥 Input: New Math Question + Answer"] --> B["🔎 Embed QA with SentenceTransformer"])
    B --> C(["📚 Search Similar Problems in Qdrant"])
    C --> D(["📦 Retrieve Top-k QA Pairs with Labels"])
    D --> E(["🧠 Build Prompt with Context"])
    E --> F(["🤖 Query GPT Model (OpenAI)"])
    F --> G(["📊 GPT Outputs Difficulty: 1–5"])
    G --> H(["✅ Return Prediction to User / API"])

    style A fill:#E3F2FD,stroke:#1E88E5,stroke-width:2px
    style B fill:#E8F5E9,stroke:#43A047,stroke-width:2px
    style C fill:#FFFDE7,stroke:#FBC02D,stroke-width:2px
    style D fill:#FFF3E0,stroke:#FB8C00,stroke-width:2px
    style E fill:#F3E5F5,stroke:#8E24AA,stroke-width:2px
    style F fill:#E1F5FE,stroke:#039BE5,stroke-width:2px
    style G fill:#E8EAF6,stroke:#3F51B5,stroke-width:2px
    style H fill:#E0F7FA,stroke:#00ACC1,stroke-width:2px
```

---

## 📦 Dataset

Training and test sets are available here:

- [hendrycks_math_train.csv](https://storage.googleapis.com/remilon-public-forever/hendrycks_math_train.csv)
- [hendrycks_math_test.csv](https://storage.googleapis.com/remilon-public-forever/hendrycks_math_test.csv)

---

## 🛠 Tech Stack

- 🐍 Python 3.11+
- 🧠 OpenAI GPT (Chat API)
- 📦 Qdrant (vector database)
- 🧰 SentenceTransformers
- 📊 Pandas, Scikit-learn, FastAPI, Streamlit (optional)

---

## 📁 Project Structure

```bash
.
├── src/
│   ├── 01_ingest_qdrant.py   # Ingest to vector DB (Qdrant)
│   ├── vector_search.py      # Search  vectors & ormat GPT prompt with context
│   ├── FAQStudy_streamlit.py # Call OpenAI & parse Final Streamlit App
├── data/                     # Dataset files
├── requirements.txt
├── Docker                    # Dockerfile
└── README.md
```

---

## 🚀 How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Load your dataset and index it in Qdrant:

```python
python src/01_ingest_qdrant.py
python src/qdrant_client.py
```

3. Run a Streamlit App:

```python
streamlit run src/FAQStudy_streamlit.py.py
```

4. See te result at:

[Study Lab - Math Difficulty Level Estimator](https://advp-ai-services-study-lab-math-difficulty-level-estimator.tqe5vc.easypanel.host)

---

## 🔮 Future Improvements

- Fine-tune an LLM using the labeled training set

---

## 👨‍💻 Author

Built by [@radianvp] — as part of the **Applied Generative AI Engineer Challenge**.

---

## 📝 License

MIT License — feel free to fork and improve.
import streamlit as st
import vector_search as vs
import os
from qdrant_client import QdrantClient
from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

qdrant_url = os.getenv("QDRANT_URL")

# Streamlit config
st.set_page_config(layout="wide")
st.title("📘 Study.com – Math Difficulty Level Estimator")

# Summary
st.markdown("""
Welcome to the Math Problem Complexity Identifier!  
This app uses vector search and OpenAI to estimate the difficulty level of math problems on a scale from 1 (very easy) to 5 (very hard).

🔍 You can try problems from areas such as:

- Algebra → "Solve for x: 3x + 2 = 11"
- Geometry → "What is the area of a circle with radius 5?"
- Calculus → "Differentiate f(x) = x² · sin(x)"
- Number Theory → "Prove that there are infinitely many prime numbers"

Just type your math problem below and get its estimated difficulty level.

---
""")

# Table of Examples with Difficulty Levels
st.markdown("### 📌 Sample Problems and Their Estimated Difficulty Levels taken from `hendrycks_math_train.csv`")
st.table([
    {"Problem": "Convert the point (0,3) in rectangular coordinates to polar coordinates. Enter your answer in the form (r,θ), where r > 0 and 0 ≤ θ < 2π.", "Subject": "Geometry", "Estimated Level (1–5)": 2},
    {"Problem": "Define p = ∑_{k=1}^∞ 1/k² and q = ∑_{k=1}^∞ 1/k³. Find a way to write ∑_{j=1}^∞ ∑_{k=1}^∞ 1/(j+k)³ in terms of p and q.", "Subject": "Series", "Estimated Level (1–5)": 5},
    {"Problem": "If f(x) = (3x - 2)/(x - 2), what is the value of f(-2) + f(-1) + f(0)? Express your answer as a common fraction.", "Subject": "Algebra", "Estimated Level (1–5)": 3},
    {"Problem": "How many positive whole-number divisors does 196 have?", "Subject": "Number Theory", "Estimated Level (1–5)": 3},
    {"Problem": "From a graph of a cross-country team's training run, determine which student has the greatest average speed.", "Subject": "Data Analysis", "Estimated Level (1–5)": 2},
    {"Problem": "What is the domain of f(x) = (2 - x) / log(2 - log(x - 2))? Express your answer in interval notation.", "Subject": "Functions & Logarithms", "Estimated Level (1–5)": 4},
    {"Problem": "Let z = 1 + i and w = (3z + 1)/(5z + 7). Find |w|.", "Subject": "Complex Numbers", "Estimated Level (1–5)": 3},
    {"Problem": "An equiangular octagon has four sides of length 1 and four sides of length √2/2, alternating. What is the area of the octagon?", "Subject": "Geometry", "Estimated Level (1–5)": 5},
    {"Problem": "Given a sequence aₙ defined by a_{i+1} = 1/(1 - a_i), and a₃ = a₁, compute (a₉)^9.", "Subject": "Sequences", "Estimated Level (1–5)": 5},
    {"Problem": "In triangle ABC, altitudes AD and BE intersect at H. Given ∠BAC = 54° and ∠ABC = 52°, find ∠AHB.", "Subject": "Geometry", "Estimated Level (1–5)": 4}
])

st.markdown("---")

st.write("Let's go to identify the complexity level of mathematical problems in areas such as Algebra, Geometry, and others.")
client = QdrantClient(url=qdrant_url) #
openai_client = OpenAI()


# Initialize Langchain's OpenAI Embedding model
#embedding_model = OpenAIEmbeddings()

termino_de_busqueda = st.text_input("Math problem Query?")

if termino_de_busqueda:
    # Create embeddings for the product names
    # query_embeddings = embedding_model.embed_query(termino_de_busqueda) #Hacemos un embedding de la consulta

    search_results = vs.vector_search(client, termino_de_busqueda)
    prompt = vs.build_prompt(termino_de_busqueda, search_results)
    answer = vs.llm(openai_client,prompt)
    
    st.write(answer)

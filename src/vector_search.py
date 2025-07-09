from qdrant_client import models


model_handle = "jinaai/jina-embeddings-v2-small-en"
collection_name = "study-math-faq-v2"

#perform search

def build_prompt(query, search_results):
    prompt_template = """
You are an expert in mathematics education. Below are math problems along with their complexity classification regarding to 
- level 1 to 2 is low
- level 3 is meduum
- level 4 to 5 is high 

Answer the QUESTION based on the CONTEXT from the FAQ database as a reference determine the complexity of the new problem. 
Use only the facts from the CONTEXT when answering the QUESTION.

Classify only as: low, medium, or high. Include level number. Do not explain your answer—just respond with a clasificacion, subject and level in a single tree words.


QUESTION: {question}

CONTEXT: 
{context}
""".strip()

    context = ""
    
    for doc in search_results:
        context = context + f"section: {doc['subject']}\nproblem: {doc['problem']}\ncomplexity: {doc['level']}\n\n"
    
    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt

def vector_search(qd_client, question):
    print('Vector search is working...')
    
    subject = 'Algebra'
    query_points = qd_client.query_points(
            collection_name=collection_name,
            query=models.Document( 
                text=question,
                model=model_handle 
            ),
            #query_filter=models.Filter( # filter by course name
            #    must=[
            #        models.FieldCondition(
            #            key="subject",
            #            match=models.MatchValue(value=subject)
            #        )
            #    ]
            #),
            limit=5,
            with_payload=True 
        )
    results = []

    for point in query_points.points:
        results.append(point.payload)

    return(results)

def llm(openai_client, prompt):
    response = openai_client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content
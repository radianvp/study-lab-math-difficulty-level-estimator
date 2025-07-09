import pandas as pd
import uuid
import os

from qdrant_client import QdrantClient
#from qdrant_client.http import models as rest
from qdrant_client import QdrantClient, models

from dotenv import load_dotenv
load_dotenv()

qdrant_url = os.getenv("QDRANT_URL")


EMBEDDING_DIMENSIONALITY = 512
model_handle = "jinaai/jina-embeddings-v2-small-en"
collection_name = "study-math-faq-v2"

qd_client = QdrantClient(url=qdrant_url) 
collections = qd_client.get_collections()
print(collections)

# Create the collection with specified vector parameters
qd_client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=EMBEDDING_DIMENSIONALITY,  
        distance=models.Distance.COSINE  
    )
)


file_path = './data/hendrycks_math_train.csv'
df_train = pd.read_csv(file_path)

df_train = df_train.head(1000)

# The DataFrame is converted into a list of dictionaries (payloads).
payloads = (
  df_train[["problem", "solution", "level", "subject"]] 
    .fillna("Unknown") 
    .rename(columns={"problem": "problem", 
                     "solution": "solution", 
                     "level": "level",
                     "subject": "subject"}) 
    .to_dict("records")
) 


points = []

for i, doc in enumerate(payloads):
    #text=doc['problem'] + ' ' + doc['solution'] + ' ' + str(doc['level'])
    text=doc['problem'] + ' ' + str(doc['level'])
    vector=models.Document(text=text, model=model_handle)
    point = models.PointStruct(
        id=i,
        vector=vector,
        payload=doc
    )
    points.append(point)


qd_client.upsert(
    collection_name=collection_name,
    points=points
)

# 
print(qd_client.count(collection_name))
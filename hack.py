import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import anthropic
from fastapi import FastAPI, Query




# Initialize FastAPI
app = FastAPI()




# Initialize Claude API
client = anthropic.Client(
  api_key="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"
)




# Load the dataset from the CSV (make sure the CSV is in Downloads)
df = pd.read_csv("chinatown hacks - Sheet1.csv")




# Combine all text fields into one text column for each restaurant
def combine_text(row):
  return " ".join([str(x) for x in row.values if pd.notnull(x)])




df['text'] = df.apply(combine_text, axis=1)




# Generate embeddings for the restaurant data using SentenceTransformer
embedder = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = embedder.encode(df['text'].tolist(), show_progress_bar=True)
embeddings = np.array(embeddings).astype("float32")




# Initialize a FAISS index with the generated embeddings
embedding_dim = embeddings.shape[1]
index = faiss.IndexFlatL2(embedding_dim)
index.add(embeddings)




def retrieve(query, top_k=3):
  """Return the top k matching restaurant texts for the given query."""
  query_embedding = embedder.encode([query]).astype("float32")
  distances, indices = index.search(query_embedding, top_k)
  return df.iloc[indices[0]]['text'].tolist()




def answer_query(query):
  # Retrieve relevant restaurant texts
  retrieved_docs = retrieve(query, top_k=3)
  context = "\n".join(retrieved_docs)




  prompt = f"""
Human: Read the data from the spreadsheet and crawl the website links for the menus to answer the questions.
Restaurant details:
{context}




Question: {query}




Answer in the following format:
<Restaurant Name> / <Google Maps link>
If a Google Maps link is not available, just provide the restaurant name.




Assistant:"""




  response = client.completions.create(
      prompt=prompt,
      model="claude-2",
      max_tokens_to_sample=150,
      temperature=0.7,
  )




  return response.completion.strip()




@app.get("/recommend")
def recommend(query: str = Query(..., description="Ask for a Chinatown restaurant recommendation")):
  return {"response": answer_query(query)}




# To run the backend, use: uvicorn hack:app --reload




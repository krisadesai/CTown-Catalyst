import streamlit as st
import requests




st.markdown(
  """
  <style>
  body {
      background: url('https://media.istockphoto.com/id/516368158/photo/san-francisco-chinatown.jpg?s=612x612&w=0&k=20&c=5VKoZGS71pinuAse6Ms5eTyBaBuV_SAgjy9g-lpsfic=') no-repeat center center fixed;
      background-size: cover;
      font-family: 'Noto Serif SC', serif;
      margin: 0;
      padding: 0;
  }
  .stApp {
      background-color: rgba(255, 249, 205, 0.85);
      padding: 2rem;
      border-radius: 10px;
      color: #FF0000;
  }
  h1 {
      text-align: center;
      font-size: 3rem;
      text-shadow: 1px 1px 2px #FFF;
      color: #FF0000;
  }
  .stMarkdown, p, div, label {
      color: #FF0000;
  }
  .stTextInput > div > div > input {
      background-color: rgba(255, 255, 255, 0.9);
      border-radius: 5px;
      border: 1px solid #ccc;
      padding: 10px;
      color: #FF0000;
  }
  .stButton > button {
      background-color: #FFC107;
      color: #FF0000;
      font-weight: bold;
      border-radius: 5px;
      padding: 10px 20px;
      border: none;
      box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
      cursor: pointer;
  }
  .stButton > button:hover {
      background-color: #FFEB3B;
  }
  </style>
  """,
  unsafe_allow_html=True
)




st.title("Chinatown Restaurant Recommender 🍜")
st.markdown("Welcome to the Chinatown Restaurant Recommender. Discover the best local spots for authentic dishes in Chinatown!")




query = st.text_input("Enter your restaurant query (e.g., 'cheapest dumplings in Chinatown'):")




if st.button("Get Recommendation"):
  if query.strip():
      try:
          response = requests.get(f"http://127.0.0.1:8000/recommend?query={query}")
          if response.status_code == 200:
              st.success(response.json()["response"])
          else:
              st.error("Failed to retrieve recommendations. Try again.")
      except Exception:
          st.error("Error connecting to the backend. Make sure it's running.")









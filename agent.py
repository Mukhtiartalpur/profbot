# agent.py

from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

class ProfBotAgent:
    def __init__(self, vectorstore):
        self.llm = ChatGroq(
            model_name="llama3-8b-8192",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=vectorstore.as_retriever()
        )

    def answer_theory(self, query):
        return self.qa_chain.run(query)

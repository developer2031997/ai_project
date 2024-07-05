import os
from pinecone import Pinecone, ServerlessSpec
from langchain.vectorstores import Pinecone as LangChainPinecone
from langchain_openai import OpenAIEmbeddings

# Initialize Pinecone instance
pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

# Ensure the index exists or create it if necessary
index_name = os.getenv("PINECONE_INDEX_NAME")
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,  # Update the dimension as per your model
        metric='cosine',  # or 'euclidean', as per your needs
        spec=ServerlessSpec(
            cloud='aws',
            region=os.getenv("PINECONE_ENV_NAME")  # Update to your region
        )
    )

# Use LangChain Pinecone with the existing index
vector_store = LangChainPinecone.from_existing_index(
    index_name,
    OpenAIEmbeddings()
)

def build_retriever(chat_args):
    search_kwargs= {"filter" :{"pdf_id": chat_args.pdf_id}}
    return vector_store.as_retriever(
        search_kwargs=search_kwargs
    )
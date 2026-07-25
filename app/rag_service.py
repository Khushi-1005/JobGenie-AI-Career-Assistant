import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

# Load .env
load_dotenv()


class RAGServices:

    def __init__(self):

        self.gemini_key = os.getenv("GEMINI_API_KEY")

        if not self.gemini_key:
            raise ValueError("Missing Gemini API key")

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=self.gemini_key
        )
        self.vector_store = Chroma(
            collection_name="resume_collection",
            embedding_function=self.embeddings,
            persist_directory="./resume_vector_db"
        )

    def process_and_create_embeddings(self):

        file_path = r"D:\KHUSHII\AgenticAI\job_search_agent\assets\AI_Developer_Resume.pdf"

        print("Current file path:", file_path)
        print("File exists:", os.path.exists(file_path))

        loader = PyPDFLoader(file_path)
        pages = loader.load()

        print(f"Loaded {len(pages)} pages")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=128
        )

        chunks = splitter.split_documents(pages)

        print(f"Created {len(chunks)} chunks")

        self.vector_store.add_documents(chunks)

        print("Embeddings created successfully!")

    def get_retriever(self):

        return self.vector_store.as_retriever(
            search_kwargs={"k": 5}
        )


if __name__ == "__main__":

    print("Starting RAG Service...")

    rag_services = RAGServices()

    print("Processing PDF...")

    rag_services.process_and_create_embeddings()

    retriever = rag_services.get_retriever()

    print("Retriever created successfully!")
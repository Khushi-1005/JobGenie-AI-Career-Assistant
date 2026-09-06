import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma


# Load .env
load_dotenv()


class RAGServices:

    def __init__(self, collection_name: str = "resume_collection"):
        self.gemini_key = os.getenv("GEMINI_API_KEY")

        if not self.gemini_key:
            raise ValueError("Missing Gemini API key")

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=self.gemini_key
        )

        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=f"./resume_vector_db_{collection_name}"
        )

    def process_and_create_embeddings(self, file_path: str):
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

    def query_resume(self, question: str, k: int = 3) -> str:
        """
        Search the resume's vector store for chunks relevant to question.
        Returns the matched text joined together, ready to hand to an LLM.
        """

        results = self.vector_store.similarity_search(
            question,
            k=k
        )

        if not results:
            return "No relevant information found in the resume."

        return "\n\n".join(
            doc.page_content for doc in results
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(
            search_kwargs={"k": 5}
        )


if __name__ == "__main__":
    print("Starting RAG Service...")

    rag_services = RAGServices()

    print("RAG Service initialized successfully!")
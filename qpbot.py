import os # for file paths and db dir
from langchain_community.document_loaders import PyPDFLoader # for PDFs
from docx import Document # for doc or docx 
from langchain_text_splitters import RecursiveCharacterTextSplitter # to create chunks
from langchain_chroma import Chroma # VectorDB
# from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings # embedding_function
from langchain_community.embeddings import SentenceTransformerEmbeddings  # embedding_function
import requests, json # to interact with LLM via ollama running locally
import logging, argparse
import warnings # to ignore warnings

warnings.filterwarnings("ignore")
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 300)
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2") #, show_progress=True)
OLLAMA_API_URL = "http://localhost:11434/api/chat"
chromadb_dir = os.path.join(os.getcwd(), "chromadb_dir")

def setup_logging(log_level):
    """
    Configures logging with the given log level.
    """
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def check_if_file_is_valid(file_path, file_extension):
    if os.path.isfile(file_path) and file_extension.lower() in ['.pdf', '.docx']:
        logging.debug("File exist and is supported.")
        return True
    else :
        raise Exception("Either file don't exist or is not supported - give full file path for your document (as of now supported - csv, pdf, doc or docx).")

def process_pdf_and_store_in_vector_db(file_path):
    loaded_pdf = PyPDFLoader(file_path).load()
    splitted_text = text_splitter.split_documents(loaded_pdf)
    
    db = Chroma.from_documents(documents=splitted_text, embedding=embedding_function, persist_directory=chromadb_dir)
    
    logging.debug(f"{db._collection.count()} {len(splitted_text)}")

def process_docx_and_store_in_vector_db(file_path):
    docx = Document(file_path)
    docx_text = "\n".join([p.text for p in docx.paragraphs])
    splitted_text = text_splitter.split_text(docx_text)
    
    db = Chroma.from_texts(texts=splitted_text, embedding=embedding_function, persist_directory=chromadb_dir)
    
    logging.debug(f"{db._collection.count()} {len(splitted_text)}")

def query_db_and_get_context(question):
    if os.path.exists(chromadb_dir):
        db = Chroma(persist_directory=chromadb_dir, embedding_function=embedding_function)
        results = db.similarity_search_with_relevance_scores(query=question, k=3)
        logging.debug(results)
        
        contexts = []
        context_str = ""
        for result in results :
            if 0 <= result[1] <= 1:
                context = result[0].page_content.replace(" \n", " ")
                contexts.append(context)
                context_str = context_str + "\n" + context
        logging.debug(context_str)        
        
        if len(contexts) == 0 :
            return "I don't know the answer."
        else :
            return context_str
    else:
        raise Exception(f"Chromadb path {chromadb_dir} not found.")        

def create_prompt(question, context_str):
    
    prompt = f"""
    * You are chat bot who answers the Question by using the Contexts given to you.
    
    * Contexts :{context_str}
    
    * Question you have to answer based on above Contexts : {question} 
    
    * Your Answer:
    """
    logging.debug(prompt)
    return prompt

def send_prompt_to_llama(prompt, model="llama3.2:latest"):
    """
    Send a prompt to the LLaMA model via Ollama API with streaming disabled.
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False  # Disable streaming to get the full response at once
    }

    # Send request to Ollama
    response = requests.post(OLLAMA_API_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        response_data = response.json()
        logging.debug(json.dumps(response_data, indent=4))
        return response_data["message"].get("content", "No response from model.")
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")
    
def reset_model_context(model="llama3.2:latest"):
    """
    Reset the conversation context of the Ollama LLaMA model.
    """
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": "Resetting the context or conversation. Start fresh."}],
         "stream": False
    }
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        if response.status_code == 200:
            logging.debug("Model context reset successfully.")
        else:
            logging.debug(f"Failed to reset model context: {response.status_code}")
    except Exception as e:
        logging.debug(f"Error resetting model context: {e}")

def main():
    file_path = os.path.abspath(input("Enter full file path for your document (as of now supported - pdf or docx) : "))
    file_name, file_extension = os.path.splitext(file_path)
    check_if_file_is_valid(file_path, file_extension)

    if file_extension.lower() == '.pdf':
        process_pdf_and_store_in_vector_db(file_path)
    elif file_extension.lower() == '.docx':
        process_docx_and_store_in_vector_db(file_path)

    reset_model_context()

    question = ""
    while question.lower() != "bye":
        question = input("\n Enter your question. Enter bye to stop this bot. Your Question : ")
        if question.lower() == "bye":
            return
        context = query_db_and_get_context(question)
        if context != "I don't know the answer.":
            prompt = create_prompt(question, context)
            answer = send_prompt_to_llama(prompt)
            print(answer)
        else:
            print(context)

def app_main(file_path):
    file_name, file_extension = os.path.splitext(file_path)
    check_if_file_is_valid(file_path, file_extension)

    if file_extension.lower() == '.pdf':
        process_pdf_and_store_in_vector_db(file_path)
        reset_model_context()
        return True
    elif file_extension.lower() == '.docx':
        process_docx_and_store_in_vector_db(file_path)
        reset_model_context()
        return True

    return False

def app_get_ans(question):
    context = query_db_and_get_context(question)
    if context != "I don't know the answer.":
        prompt = create_prompt(question, context)
        answer = send_prompt_to_llama(prompt)
        return answer
    else:
        return context


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A RAG ChatBot.")
    parser.add_argument(
        "--log_level",
        type=str,
        default="INFO",
        help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )
    args = parser.parse_args()

    # Setup logging
    setup_logging(args.log_level)

    main()
    

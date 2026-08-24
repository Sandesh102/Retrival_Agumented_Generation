import argparse
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama

from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)


import os
from dotenv import load_dotenv

load_dotenv()

def query_rag(query_text: str):
    # Prepare the DB.
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    if gemini_key:
        from langchain_google_genai import ChatGoogleGenerativeAI
        model = ChatGoogleGenerativeAI(model="gemini-3.6-flash", google_api_key=gemini_key)
    else:
        from langchain_community.llms.ollama import Ollama
        model = Ollama(model="mistral")

    response = model.invoke(prompt)
    if hasattr(response, "content"):
        content = response.content
        if isinstance(content, str):
            response_text = content
        elif isinstance(content, list):
            text_parts = [item.get("text", str(item)) if isinstance(item, dict) else str(item) for item in content]
            response_text = "\n".join(text_parts)
        else:
            response_text = str(content)
    else:
        response_text = str(response)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)
    return response_text


if __name__ == "__main__":
    main()

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

CHROMA_DIR = "./newsbot_chroma"

def store_articles_in_chromadb(articles):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    all_chunks = []
    all_metadatas = []

    for article in articles:
        content = article.get("content") or article.get("description") or ""
        if not content:
            continue

        chunks = splitter.split_text(content)

        for chunk in chunks:
            all_chunks.append(chunk)
            all_metadatas.append({
                "newspaper": article.get("newspaper", "Unknown"),
                "title": article.get("title", ""),
                "url": article.get("url", ""),
                "published_at": article.get("published_at", "")
            })

    if all_chunks:
        vectorstore = Chroma.from_texts(
            texts=all_chunks,
            embedding=embeddings,
            metadatas=all_metadatas,
            persist_directory=CHROMA_DIR
        )
        vectorstore.persist()
        print(f"✅ Stored {len(all_chunks)} chunks in ChromaDB")
    else:
        print("❌ No content to store in ChromaDB")

def answer_question(question):
    try:
        vectorstore = Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=embeddings
        )

        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        relevant_docs = retriever.invoke(question)
        if not relevant_docs:
            return {
                "answer": "No relevant news found for your question.",
                "sources": []
            }

        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        sources = [doc.metadata for doc in relevant_docs]

        prompt = f"""You are NewsBot, an AI newspaper assistant for Indian readers.
Answer the user's question based only on the newspaper content below.
Always mention which newspaper the information came from.
If the answer is not in the content, say 'This was not found in today's newspapers.'
Keep answers concise and clear.

Newspaper Content:
{context}

User Question: {question}"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0
        )

        answer = response.choices[0].message.content

        return {
            "answer": answer,
            "sources": sources
        }

    except Exception as e:
        return {
            "answer": f"Something went wrong: {str(e)}",
            "sources": []
        }
         
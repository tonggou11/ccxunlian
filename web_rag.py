from flask import Flask, render_template, request
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL
import chromadb
from chromadb.utils import embedding_functions
import requests
import os

app = Flask(__name__)

url = DEEPSEEK_BASE_URL + "/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    "Content-Type": "application/json",
}

# 全局变量：存当前数据集 + 对话历史
collection = None
chunks = []
history = []  # 格式: [{"q": "问题", "a": "回答", "sources": ["块1", "块2", "块3"]}]

# Embedding 模型只加载一次（不用每次上传都重新加载）
embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="BAAI/bge-small-zh-v1.5"
)
client = chromadb.PersistentClient(path="./chroma_web_data")


def split_text(text, chunk_size=300, overlap=50):
    """滑动窗口切块"""
    text = " ".join(text.split())  # 清洗空白
    chunks_list = []
    step = chunk_size - overlap
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks_list.append(text[start:end])
        start += step
    return chunks_list


def build_collection(chunks_list):
    """构建向量数据库"""
    global collection
    try:
        client.delete_collection("web_doc")
    except:
        pass

    collection = client.create_collection(
        name="web_doc",
        embedding_function=embed_fn,
    )

    for i, chunk in enumerate(chunks_list):
        collection.add(
            documents=[chunk],
            ids=[str(i)],
        )


def call_ai(question, relevant_chunks):
    """把资料 + 问题发给 DeepSeek"""
    context = "\n---\n".join(relevant_chunks)

    system_prompt = (
        "你是一个知识库问答助手。请严格根据以下资料回答用户的问题。"
        "如果资料中没有相关信息，请诚实地说'资料中没有找到相关内容'，不要编造。"
    )

    user_prompt = f"资料：\n{context}\n\n问题：{question}"

    body = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    return data["choices"][0]["message"]["content"]


@app.route("/", methods=["GET", "POST"])
def index():
    global chunks, history
    result = ""
    question = ""
    sources = []
    chunk_count = len(chunks)

    if request.method == "POST":
        action = request.form.get("action", "")

        # 上传文件
        if action == "upload" and "file" in request.files and request.files["file"].filename:
            file = request.files["file"]
            text = file.read().decode("utf-8")
            chunks = split_text(text)
            build_collection(chunks)
            chunk_count = len(chunks)
            history = []   # 上传新文档清空旧对话

        # 提问
        elif action == "ask":
            question = request.form.get("question", "")
            if question.strip() and collection:
                search_results = collection.query(
                    query_texts=[question],
                    n_results=3,
                )
                sources = search_results["documents"][0]
                result = call_ai(question, sources)
                # 保存到历史
                history.append({"q": question, "a": result, "sources": sources})

    return render_template(
        "rag.html",
        result=result,
        question=question,
        chunk_count=chunk_count,
        history=history,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

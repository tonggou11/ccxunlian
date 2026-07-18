import requests
import sys
import chromadb
from chromadb.utils import embedding_functions
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

sys.stdout.reconfigure(encoding="utf-8")

url = DEEPSEEK_BASE_URL + "/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    "Content-Type": "application/json",
}


# ============ 第一步：加载 + 切块 ============

def load_and_split(filepath, chunk_size=300, overlap=50):
    """
    滑动窗口切块，带重叠。
    chunk_size=300：每块 300 字
    overlap=50：相邻两块重叠 50 字
    比如：块1=0~300字，块2=250~550字，块3=500~800字...
    这样一句话即使刚好在 300 字的边界上，也不会被切断。
    """
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # 去掉多余空白，让全文连成一片
    text = " ".join(text.split())

    chunks = []
    step = chunk_size - overlap   # 每次滑动的步长
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]    # Python 切片：text[0:300] 取前 300 个字符
        chunks.append(chunk)
        start += step              # 窗口往后滑

    return chunks


# ============ 第二步：构建语义知识库 ============

def build_knowledge_base(chunks):
    """用真正的 embedding 模型把文字转成向量"""
    client = chromadb.PersistentClient(path="./chroma_data")

    try:
        client.delete_collection("thesis")
    except:
        pass

    # 用中文 embedding 模型（DefaultEmbeddingFunction 是英文的，对中文效果差）
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="shibing624/text2vec-base-chinese"
    )

    collection = client.create_collection(
        name="thesis",
        embedding_function=embed_fn,  # ← 关键：用 AI 模型转向量
    )

    for i, chunk in enumerate(chunks):
        collection.add(
            documents=[chunk],
            ids=[str(i)],
        )

    print(f"语义知识库构建完成！共 {len(chunks)} 块\n")
    return collection


# ============ 第三步：搜索 + 问答 ============

def search(collection, question, top_n=3):
    results = collection.query(
        query_texts=[question],
        n_results=top_n,
    )
    chunks = results["documents"][0]
    distances = results["distances"][0]

    for i, (chunk, dist) in enumerate(zip(chunks, distances)):
        print(f"  语义距离 {dist:.3f}: {chunk[:80]}...")

    return chunks


def ask_with_context(question, chunks):
    context = "\n---\n".join(chunks)

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


# ============ 主程序 ============

print("=" * 50)
print("RAG 智能问答系统（AI Embedding 语义版）")
print("=" * 50)

print("正在加载毕业论文...")
chunks = load_and_split("knowledge.txt")
print(f"已切分为 {len(chunks)} 块")

print("正在构建语义知识库（AI 模型理解每块的意思）...")
collection = build_knowledge_base(chunks)

while True:
    question = input("\n请输入你的问题（输入 quit 退出）：\n> ")
    if question.lower() == "quit":
        print("再见！")
        break

    print("\n正在语义搜索...")
    relevant = search(collection, question)
    print()

    if not relevant:
        print("未找到相关内容。\n")
        continue

    print("AI 正在回答...\n")
    answer = ask_with_context(question, relevant)
    print("-" * 50)
    print(answer)
    print("-" * 50)

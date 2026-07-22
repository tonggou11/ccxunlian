import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL
import requests

app = Flask(__name__)

url = DEEPSEEK_BASE_URL + "/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    "Content-Type": "application/json",
}

# ============ 数据库初始化 ============
conn = sqlite3.connect("interview.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        role     TEXT    NOT NULL,
        created  TEXT    NOT NULL
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS qa_pairs (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER NOT NULL,
        question   TEXT    NOT NULL,
        answer     TEXT,
        feedback   TEXT,
        FOREIGN KEY (session_id) REFERENCES sessions(id)
    )
""")
conn.commit()

# ============ 面试岗位的 System Prompt ============
ROLE_PROMPTS = {
    "python": (
        "你是一位资深 Python 后端面试官。请对候选人进行技术面试。"
        "每次只问一个问题，候选人回答后给出简短点评（2-3句话），然后问下一个问题。"
        "共问5个问题，覆盖：Python基础、数据结构、Web框架、数据库、项目经验。"
        "最后给出总体评分（满分100）和一条改进建议。"
    ),
    "frontend": (
        "你是一位资深前端面试官。请对候选人进行技术面试。"
        "每次只问一个问题，候选人回答后给出简短点评（2-3句话），然后问下一个问题。"
        "共问5个问题，覆盖：HTML/CSS基础、JavaScript核心、框架知识、性能优化、项目经验。"
        "最后给出总体评分（满分100）和一条改进建议。"
    ),
    "ai": (
        "你是一位 AI 应用开发面试官。请对候选人进行技术面试。"
        "每次只问一个问题，候选人回答后给出简短点评（2-3句话），然后问下一个问题。"
        "共问5个问题，覆盖：Python基础、大模型概念、RAG原理、Prompt Engineering、AI项目经验。"
        "最后给出总体评分（满分100）和一条改进建议。"
    ),
    "product": (
        "你是一位产品经理面试官。请对候选人进行面试。"
        "每次只问一个问题，候选人回答后给出简短点评（2-3句话），然后问下一个问题。"
        "共问5个问题，覆盖：需求分析、用户调研、数据驱动、项目管理、产品思维。"
        "最后给出总体评分（满分100）和一条改进建议。"
    ),
}


def call_ai(messages):
    """通用 AI 调用"""
    body = {
        "model": "deepseek-chat",
        "messages": messages,
    }
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    return data["choices"][0]["message"]["content"]


# ============ 路由 ============

@app.route("/")
def index():
    # 查历史面试
    cur.execute("SELECT id, role, created FROM sessions ORDER BY id DESC LIMIT 10")
    sessions = cur.fetchall()
    return render_template("interview.html", sessions=sessions)


@app.route("/api/start", methods=["POST"])
def api_start():
    """开始面试——创建 session + 返回第一个问题"""
    data = request.get_json()
    role = data.get("role", "python")
    prompt = ROLE_PROMPTS.get(role, ROLE_PROMPTS["python"])

    # 建 session
    now = datetime.now().strftime("%m-%d %H:%M")
    cur.execute("INSERT INTO sessions (role, created) VALUES (?, ?)", (role, now))
    conn.commit()
    session_id = cur.lastrowid

    # 让 AI 提第一个问题
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": "请开始面试，提出第一个问题。"},
    ]
    reply = call_ai(messages)

    # 存问题
    cur.execute(
        "INSERT INTO qa_pairs (session_id, question) VALUES (?, ?)",
        (session_id, reply),
    )
    conn.commit()

    return jsonify({
        "session_id": session_id,
        "message": reply,
    })


@app.route("/api/answer", methods=["POST"])
def api_answer():
    """提交答案——返回点评 + 下一个问题 / 最终评价"""
    data = request.get_json()
    session_id = data.get("session_id")
    answer = data.get("answer", "")
    role = data.get("role", "python")
    messages = data.get("messages", [])

    # 把用户回答加进消息历史
    messages.append({"role": "user", "content": answer})
    reply = call_ai(messages)

    # 查找最后一个没有答案的 question，更新它
    cur.execute(
        "SELECT id FROM qa_pairs WHERE session_id = ? AND answer IS NULL ORDER BY id DESC LIMIT 1",
        (session_id,),
    )
    row = cur.fetchone()
    if row:
        cur.execute(
            "UPDATE qa_pairs SET answer = ?, feedback = ? WHERE id = ?",
            (answer, reply, row[0]),
        )
        conn.commit()

    return jsonify({"message": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

from flask import Flask, render_template, request
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL
import requests

app = Flask(__name__)

url = DEEPSEEK_BASE_URL + "/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    "Content-Type": "application/json",
}

# 不同功能的 System Prompt
PROMPTS = {
    "score": "你是一位资深 HR，有10年招聘经验。请对以下简历进行评分（满分100），并给出3条最重要的修改建议。",
    "project": "你是一位简历优化专家。请把以下简历中的项目经历用 STAR 法则改写，更有数据感，保留原意不编造。",
    "self_eval": "你是一位个人品牌专家。请把以下简历中的自我评价改得更精炼有亮点，突出核心竞争力。",
    "intro": "你是一位演讲教练。根据以下简历生成一段30秒的自我介绍，适合面试开场，语气自信不空洞。",
}


def call_ai(system_prompt, user_input):
    body = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
    }
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    return data["choices"][0]["message"]["content"]


@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    resume_text = ""

    if request.method == "POST":
        resume_text = request.form.get("resume", "")
        action = request.form.get("action", "score")
        prompt = PROMPTS.get(action, PROMPTS["score"])

        if resume_text.strip():
            result = call_ai(prompt, resume_text)

    return render_template("index.html", result=result, resume_text=resume_text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

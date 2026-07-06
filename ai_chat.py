import requests
import json
import sys
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

sys.stdout.reconfigure(encoding="utf-8")

url = DEEPSEEK_BASE_URL + "/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    "Content-Type": "application/json",
}

# ③ 存历史消息 —— 每轮对话都记下来
history = []

print("=" * 40)
print("AI 聊天助手（输入 quit 退出）")
print("=" * 40)

while True:                    # ① 跟成绩系统一样的死循环
    user_input = input("\n你：")   # ② 每次问用户要输入
    if user_input.lower() == "quit":
        print("再见！")
        break                  # ③ 跟菜单选 4 一样的退出方式

    history.append({"role": "user", "content": user_input})   # ④ 把用户说的话记下来

    body = {
        "model": "deepseek-chat",
        "messages": history,   # ⑤ 把整段历史发给 AI（这样它有记忆）
    }

    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    reply = data["choices"][0]["message"]["content"]

    history.append({"role": "assistant", "content": reply})   # ⑥ 把 AI 的回复也记下来
    print(f"AI：{reply}")

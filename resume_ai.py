import requests
import sys
import os
from datetime import datetime
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL

sys.stdout.reconfigure(encoding="utf-8")

url = DEEPSEEK_BASE_URL + "/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    "Content-Type": "application/json",
}

# 输出文件夹 —— 所有保存的结果都放这，不跟代码混一起
OUTPUT_DIR = "output"


def call_ai(system_prompt, user_input):
    """封装好的 AI 调用函数"""
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


def save_result(filename, content):
    """保存结果到 output 文件夹，自动加时间戳"""
    # 确保 output 文件夹存在（不存在就创建）
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 文件名格式：简历评分_2026-07-07_14-30-00.txt
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    full_name = f"{filename}_{timestamp}.txt"
    path = os.path.join(OUTPUT_DIR, full_name)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n📁 已保存到：{path}")


def list_saved():
    """列出所有已保存的结果文件"""
    if not os.path.exists(OUTPUT_DIR):
        print("\n还没有保存过任何结果。")
        return

    files = os.listdir(OUTPUT_DIR)
    if not files:
        print("\n还没有保存过任何结果。")
        return

    print(f"\n已保存的结果（{len(files)} 个）：")
    files.sort(reverse=True)  # 最新的排前面
    for i, f in enumerate(files, 1):
        # 去掉 .txt 后缀显示
        print(f"  {i}. {f.replace('.txt', '')}")


# ============ 主程序 ============

print("=" * 50)
print("AI 简历优化助手")
print("=" * 50)
print("请先粘贴你的简历内容（输入 END 结束）：")

lines = []
while True:
    line = input()
    if line.strip().upper() == "END":
        break
    lines.append(line)
resume_text = "\n".join(lines)

if not resume_text.strip():
    print("未输入任何内容，程序退出。")
    sys.exit()

while True:
    print("\n" + "=" * 50)
    print("请选择功能：")
    print("1. 简历评分 + 整体建议")
    print("2. 优化项目经历")
    print("3. 优化自我评价")
    print("4. 生成自我介绍（30秒版）")
    print("5. 修改简历后重新分析")
    print("6. 查看已保存的结果")
    print("7. 退出")
    print("=" * 50)

    choice = input("请选择（1-7）：")

    if choice == "1":
        print("\n正在分析...\n")
        result = call_ai(
            "你是一位资深 HR，有10年招聘经验。请对以下简历进行评分（满分100），"
            "并给出3条最重要的修改建议。",
            resume_text,
        )
        print(result)
        if input("\n是否保存到文件？(y/n)：").lower() == "y":
            save_result("简历评分", result)

    elif choice == "2":
        print("\n正在优化...\n")
        result = call_ai(
            "你是一位简历优化专家。请把以下简历中的项目经历改写得更专业、"
            "更有数据感，用 STAR 法则（情境-任务-行动-结果）。保留原意，不要编造。",
            resume_text,
        )
        print(result)
        if input("\n是否保存到文件？(y/n)：").lower() == "y":
            save_result("项目经历优化", result)

    elif choice == "3":
        print("\n正在优化...\n")
        result = call_ai(
            "你是一位个人品牌专家。请把以下简历中的自我评价部分改写"
            "得更精炼、更有亮点，突出核心竞争力。",
            resume_text,
        )
        print(result)
        if input("\n是否保存到文件？(y/n)：").lower() == "y":
            save_result("自我评价优化", result)

    elif choice == "4":
        print("\n正在生成...\n")
        result = call_ai(
            "你是一位演讲教练。根据以下简历，生成一段30秒的自我介绍，"
            "适合面试开场。语气自信、不空洞。",
            resume_text,
        )
        print(result)
        if input("\n是否保存到文件？(y/n)：").lower() == "y":
            save_result("自我介绍", result)

    elif choice == "5":
        print("\n请重新粘贴你的简历内容（输入 END 结束）：")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        resume_text = "\n".join(lines)

    elif choice == "6":
        list_saved()

    elif choice == "7":
        print("再见！祝找工作顺利 🎉")
        break

    else:
        print("输入错误，请输入 1-7！")

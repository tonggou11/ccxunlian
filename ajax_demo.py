from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("ajax_demo.html")


@app.route("/api/add", methods=["POST"])
def api_add():
    """API 端点——返回 JSON，不返回整个页面"""
    data = request.get_json()     # 拿 JS 发过来的 JSON
    a = data.get("a", 0)
    b = data.get("b", 0)
    time.sleep(1)                 # 模拟等待 AI 回复的延迟
    return jsonify({
        "result": a + b,
        "message": f"计算完成：{a} + {b} = {a + b}",
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

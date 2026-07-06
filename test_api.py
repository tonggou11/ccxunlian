import requests

# 用 Python 发一个请求，代替浏览器访问网站
response = requests.get("https://api.github.com/users/tonggou11")

# 查看返回的内容（JSON 格式的数据）
data = response.json()
print("用户名：", data["login"])
print("公开仓库数：", data["public_repos"])

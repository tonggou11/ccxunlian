import sqlite3

# ============ 连接数据库 ============
conn = sqlite3.connect("contacts.db")   # 没有这个文件就自动创建
cur = conn.cursor()

# ============ 建表（启动时执行一次）============
cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        name    TEXT    NOT NULL,
        phone   TEXT    NOT NULL
    )
""")
conn.commit()   # 立即生效

# 查一下表里现在有多少条
cur.execute("SELECT COUNT(*) FROM contacts")
count = cur.fetchone()[0]
print(f"数据库中已有 {count} 条联系人")

# ============ 主程序 ============

while True:
    print("=" * 30)
    print("通讯录管理系统")
    print("=" * 30)
    print("1. 添加联系人")
    print("2. 查看所有联系人")
    print("3. 搜索联系人")
    print("4. 退出")
    print("=" * 30)

    choice = input("请选择（1-4）：")

    if choice == "1":
        name = input("请输入联系人姓名：")
        phone = input("请输入联系人电话：")
        # INSERT INTO 表名 (列1, 列2) VALUES (值1, 值2)
        # ? 是占位符，防止 SQL 注入（跟 f-string 拼字符串的效果一样但更安全）
        cur.execute(
            "INSERT INTO contacts (name, phone) VALUES (?, ?)",
            (name, phone),
        )
        conn.commit()   # 插入/修改/删除后必须 commit，不然白干
        print(f"{name} 的电话 {phone} 已添加！")

    elif choice == "2":
        cur.execute("SELECT id, name, phone FROM contacts")
        rows = cur.fetchall()   # 拿到所有结果行
        if len(rows) == 0:
            print("还没有联系人，请先添加！")
        else:
            print("ID\t姓名\t电话")
            print("-" * 30)
            for row in rows:
                print(f"{row[0]}\t{row[1]}\t{row[2]}")

    elif choice == "3":
        search_name = input("请输入要搜索的姓名：")
        # SELECT ... WHERE name = ?   →  只查名字匹配的那条
        cur.execute(
            "SELECT id, name, phone FROM contacts WHERE name = ?",
            (search_name,),
        )
        row = cur.fetchone()   # 拿一条（名字是唯一的）
        if row:
            print(f"{row[1]} 的电话是：{row[2]}")
        else:
            print(f"未找到联系人：{search_name}")

    elif choice == "4":
        conn.close()   # 关掉数据库连接
        print("再见！")
        break

    else:
        print("输入错误，请输入 1-4！")

import sqlite3

# ============ 连接数据库 ============
# 如果 contacts.db 不存在，自动创建
conn = sqlite3.connect("contacts.db")

# cursor = 游标，所有 SQL 命令都通过它执行
# 你把它想象成鼠标光标——在数据库里指哪打哪
cur = conn.cursor()

# ============ 建表 ============
# SQL 里的 CREATE TABLE = 创建一张表
# 表 = Excel 工作表，有固定的列名
cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id      INTEGER PRIMARY KEY AUTOINCREMENT,
        name    TEXT    NOT NULL,
        phone   TEXT    NOT NULL
    )
""")

# 拆开上面的 SQL：
# CREATE TABLE IF NOT EXISTS  =  如果表不存在就建，存在就跳过
# id      INTEGER PRIMARY KEY AUTOINCREMENT  =  自增ID（1,2,3...不用自己管）
# name    TEXT NOT NULL                      =  名字，字符串类型，不能为空
# phone   TEXT NOT NULL                      =  电话，字符串类型，不能为空

# ============ 插入数据 ============
# INSERT INTO 表名 (列1, 列2) VALUES (值1, 值2)
cur.execute(
    "INSERT INTO contacts (name, phone) VALUES (?, ?)",
    ("张三", "13800001111"),
)
cur.execute(
    "INSERT INTO contacts (name, phone) VALUES (?, ?)",
    ("李四", "13900002222"),
)

# ? 是占位符，后面的元组依次填入。
# 为什么用 ? 而不是直接拼字符串？防止 SQL 注入攻击——你以后会学

# ============ 提交 ============
# INSERT/UPDATE/DELETE 之后必须 commit，不然不会真正写入
conn.commit()

# ============ 查询 ============
# SELECT 列名 FROM 表名
print("=== 所有联系人 ===")
cur.execute("SELECT id, name, phone FROM contacts")
rows = cur.fetchall()           # fetchall = 拿到所有结果
for row in rows:
    print(f"  ID:{row[0]}  姓名:{row[1]}  电话:{row[2]}")

# SELECT ... WHERE 条件       =  过滤
print("\n=== 搜索：名字叫张三的 ===")
cur.execute("SELECT * FROM contacts WHERE name = ?", ("张三",))
row = cur.fetchone()            # fetchone = 只拿一条
print(f"  ID:{row[0]}  姓名:{row[1]}  电话:{row[2]}")

# SELECT COUNT(*)              =  数有多少条
cur.execute("SELECT COUNT(*) FROM contacts")
count = cur.fetchone()[0]
print(f"\n总共 {count} 条记录")

# ============ 修改 ============
# UPDATE 表名 SET 列=新值 WHERE 条件
cur.execute(
    "UPDATE contacts SET phone = ? WHERE name = ?",
    ("13700009999", "张三"),
)
conn.commit()
print("\n张三的电话已修改为 13700009999")

# ============ 删除 ============
# DELETE FROM 表名 WHERE 条件
cur.execute("DELETE FROM contacts WHERE name = ?", ("李四",))
conn.commit()
print("李四已删除")

# 最终结果
print("\n=== 最终数据 ===")
cur.execute("SELECT * FROM contacts")
for row in cur.fetchall():
    print(f"  ID:{row[0]}  姓名:{row[1]}  电话:{row[2]}")

# ============ 关闭连接 ============
conn.close()

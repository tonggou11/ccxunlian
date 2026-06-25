# 通讯录管理系统

# 启动时从文件读取（格式：姓名,电话）
contacts = []
try:
    with open("contacts.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            name = parts[0]
            phone = parts[1]                        # 电话是字符串，不是数字
            contacts.append({"name": name, "phone": phone})
    print(f"已从文件加载 {len(contacts)} 条联系人")
except FileNotFoundError:
    print("首次使用，尚无保存的联系人")

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
        phone = input("请输入联系人电话：")          # 电话直接用字符串，不转float
        contacts.append({"name": name, "phone": phone})
        print(f"{name} 的电话 {phone} 已添加！")

    elif choice == "2":
        if len(contacts) == 0:
            print("还没有联系人，请先添加！")
        else:
            print("姓名\t电话")
            print("-" * 20)
            for c in contacts:
                print(f"{c['name']}\t{c['phone']}")

    elif choice == "3":
        if len(contacts) == 0:
            print("还没有联系人，无法搜索！")
        else:
            search_name = input("请输入要搜索的姓名：")     # ① 问你要搜谁
            found = False                                 # ② 先假设"没找到"
            for c in contacts:                            # ③ 一个一个翻
                if c["name"] == search_name:              # ④ 名字对上了！
                    print(f"{c['name']} 的电话是：{c['phone']}")
                    found = True                          # ⑤ 找到了，标记改成True
                    break                                 # ⑥ 找到了就别继续翻了
            if not found:                                 # ⑦ 翻完了还是False
                print(f"未找到联系人：{search_name}")

    elif choice == "4":
        with open("contacts.txt", "w", encoding="utf-8") as f:
            for c in contacts:
                f.write(f"{c['name']},{c['phone']}\n")
        print(f"已保存 {len(contacts)} 条联系人，再见！")
        break

    else:
        print("输入错误，请输入 1-4！")

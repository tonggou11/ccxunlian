# 学生成绩管理系统

# 启动时从文件读取（格式：姓名,成绩）
students = []
try:
    with open("students.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            name = parts[0]
            score = float(parts[1])
            students.append({"name": name, "score": score})
    print(f"已从文件加载 {len(students)} 条成绩")
except FileNotFoundError:
    print("首次使用，尚无保存的成绩")

while True:
    print("=" * 30)
    print("学生成绩管理系统")
    print("=" * 30)
    print("1. 添加学生成绩")
    print("2. 查看所有学生成绩")
    print("3. 计算平均分")
    print("4. 退出")
    print("=" * 30)

    choice = input("请选择（1-4）：")

    if choice == "1":
        name = input("请输入学生姓名：")
        score = float(input("请输入学生成绩："))
        students.append({"name": name, "score": score})
        print(f"{name} 的成绩 {score} 已添加！")

    elif choice == "2":
        if len(students) == 0:
            print("还没有成绩，请先添加！")
        else:
            print("姓名\t成绩")
            print("-" * 20)
            for stu in students:
                print(f"{stu['name']}\t{stu['score']}")

    elif choice == "3":
        if len(students) == 0:
            print("还没有成绩，无法计算平均分！")
        else:
            total = 0
            for stu in students:
                total += stu["score"]
            avg = total / len(students)
            print(f"共 {len(students)} 人，平均分：{avg:.2f}")

    elif choice == "4":
        with open("students.txt", "w", encoding="utf-8") as f:
            for stu in students:
                f.write(f"{stu['name']},{stu['score']}\n")
        print(f"已保存 {len(students)} 条成绩，再见！")
        break

    else:
        print("输入错误，请输入 1-4！")

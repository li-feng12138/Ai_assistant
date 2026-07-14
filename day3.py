#学生信息管理系统(第三版)

#获取文件路径中的目录部分
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

#得到数据文件的完整路径,即DATA_FILE为当前目录下的students_info.txt文件
DATA_FILE = os.path.join(SCRIPT_DIR, "students_info.txt")

#在编辑器中显示文件路径
print(f"数据文件路径: {DATA_FILE}")


# ==================== 文件操作函数 ====================
def load_students(filename):
    """从文件加载学生信息"""
    stu_dict = {}
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split()
                    name = parts[0].split(":")[1]
                    chinese = int(parts[1].split(":")[1])
                    math = int(parts[2].split(":")[1])
                    english = int(parts[3].split(":")[1])
                    stu_dict[name] = {'语文': chinese, '数学': math, '英语': english}
        print(f"已从文件加载 {len(stu_dict)} 条学生信息")
    except FileNotFoundError:
        print("文件不存在，将创建新文件")
    return stu_dict

def save_all_students(filename, stu_dict):
    """将所有学生信息保存到文件（覆盖写入）"""
    with open(filename, "w", encoding="utf-8") as file:
        for name, info in stu_dict.items():
            file.write(f"姓名:{name}  语文:{info['语文']}  数学:{info['数学']}  英语:{info['英语']}\n")

def append_student(filename, name, chinese, math, english):
    """追加一条学生信息到文件"""
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"姓名:{name}  语文:{chinese}  数学:{math}  英语:{english}\n")

def remove_student_from_file(filename, name):
    """从文件中删除指定学生"""
    students = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith("姓名:" + name + "  "):
                students.append(line)
    with open(filename, "w", encoding="utf-8") as file:
        for student in students:
            file.write(student + "\n")


# ==================== 学生信息管理函数 ====================
def input_scores():
    """输入并返回三科成绩"""
    chinese = int(input("请输入语文成绩: "))
    math = int(input("请输入数学成绩: "))
    english = int(input("请输入英语成绩: "))
    return chinese, math, english

def add_student(stu_dict, filename):
    """添加学生信息"""
    stu_name = input("请输入姓名: ")
    if stu_name in stu_dict:
        print("该名同学已存在,请重新输入.")
        return
    chinese, math, english = input_scores()
    stu_dict[stu_name] = {'语文': chinese, '数学': math, '英语': english}
    append_student(filename, stu_name, chinese, math, english)
    print("添加成功~")

def modify_student(stu_dict, filename):
    """修改学生信息"""
    stu_name = input("请输入姓名: ")
    if stu_name not in stu_dict:
        print("该名同学不存在,请重新输入.")
        return
    chinese, math, english = input_scores()
    stu_dict[stu_name] = {'语文': chinese, '数学': math, '英语': english}
    save_all_students(filename, stu_dict)
    print("修改成功~")

def delete_student(stu_dict, filename):
    """删除学生信息"""
    stu_name = input("请输入姓名: ")
    if stu_name not in stu_dict:
        print("该名同学不存在,请重新输入.")
        return
    del stu_dict[stu_name]
    remove_student_from_file(filename, stu_name)
    print("删除成功~")

def query_student(stu_dict):
    """查询学生信息"""
    stu_name = input("请输入姓名: ")
    if stu_name not in stu_dict:
        print("该名同学不存在,请重新输入.")
        return
    info = stu_dict[stu_name]
    print(f"姓名:{stu_name},语文:{info['语文']},数学:{info['数学']},英语:{info['英语']}")

def print_all_students(stu_dict):
    """打印全部学生信息"""
    if not stu_dict:
        print("名单为空,请输入后打印.")
        return
    for name, info in stu_dict.items():
        print(f"姓名:{name},语文:{info['语文']},数学:{info['数学']},英语:{info['英语']}")
    print("已完成打印")

def statistics_scores(stu_dict):
    """统计班级各科最高分及总分最高分"""
    if not stu_dict:
        print("名单为空,请输入后打印.")
        return
    chinese_list = []
    math_list = []
    english_list = []
    total_list = []
    for name, info in stu_dict.items():
        chinese_list.append((name, info['语文']))
        math_list.append((name, info['数学']))
        english_list.append((name, info['英语']))
        total_list.append((name, info['语文'] + info['数学'] + info['英语']))

    def find_top(score_list):
        max_score = max(score for _, score in score_list)
        top_names = [name for name, score in score_list if score == max_score]
        return max_score, top_names

    ch_max, ch_tops = find_top(chinese_list)
    math_max, math_tops = find_top(math_list)
    english_max, english_tops = find_top(english_list)
    total_max, total_tops = find_top(total_list)

    print(f"总分最高分:{total_max} ({', '.join(total_tops)})")
    print(f"语文最高分:{ch_max} ({', '.join(ch_tops)}), 数学最高分:{math_max} ({', '.join(math_tops)}), 英语最高分:{english_max} ({', '.join(english_tops)})")


# ==================== 主程序 ====================
menu = """
操作:
  1.添加学生信息
  2.修改学生信息
  3.删除学生信息
  4.查询学生信息
  5.打印全部学生信息
  6.统计班级成绩
  7.退出系统
"""
# 定义关键容器stu_dict + 显示文件中已存在的学生信息(调用load_students函数时若文件不存在,则因'r'创建新文件)
stu_dict = load_students(DATA_FILE)

print(menu)
while True:
    try:
        match int(input("请输入执行操作: ")):
            case 1:
                add_student(stu_dict, DATA_FILE)
            case 2:
                modify_student(stu_dict, DATA_FILE)
            case 3:
                delete_student(stu_dict, DATA_FILE)
            case 4:
                query_student(stu_dict)
            case 5:
                print_all_students(stu_dict)
            case 6:
                statistics_scores(stu_dict)
            case 7:
                print("已成功退出,再见.")
                break
            case _:
                print("操作错误,请重新输入")
    except:
        print("输入错误，请输入对应操作数字")
    print()
    print("""操作:
    1.添加  2.修改  3.删除  4.查询  5.打印  6.统计  7.退出""")



"""
1.生成的对应文件 students_info.txt 没有保存到当前目录
3.对于主体中每一个操作方式没有写成函数
2.删除操作对于名字只有两个字的学生有bug,可能误删同名前缀的人
"""




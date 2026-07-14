# import csv
#
# def show_menu():
#     print("=========================================")
#     print("            学生信息查询小程序             ")
#     print("            1. 按姓名查询")
#     print("            2. 按学号查询")
#     print("            3. 打印全部学生信息")
#     print("            4. 退出")
#     print("=========================================")
#
# #将文件中的学生信息读取并存储在列表中
# def load_students(filename):
#     students = []
#     try:
#         file = open(filename,"r",encoding = "utf-8")
#         reader = csv.DictReader(file)
#         for row in reader:
#             students.append(row)
#         file.close()
#     except:
#         print("文件读取失败,请检查文件名和保存位置")
#     return students
#
# #展示要查询的学生信息
# def show_student(student):
#     print(f"学号:{student['id']} 姓名:{student['name']} 专业:{student['major']} 班级:{student['class_name']}")
#
#
# #按姓名查询学生信息
# def find_student_by_name(students, key):
#     for student in students:
#         if student['name'] == key:
#             return student
#     return None
#
# #按学号查询学生信息
# def find_student_by_id(students, key):
#     for student in students:
#         if student['id'] == key:
#             return student
#     return None
#
# #打印所有学生信息
# def print_all_students(students):
#     for student in students:
#         show_student(student)
#         print()
#     print("以上为全部学生信息~")
#
#
#
# students = load_students("students.csv")
# while True:
#     show_menu()
#     match int(input("请输入执行操作: ")):
#         case 1:
#             keyword = input("请输入要查询的姓名: ")
#             result = find_student_by_name(students, keyword)
#             if result == None:
#                 print("未找到该学生")
#             else:
#                 show_student(result)
#         case 2:
#             keyword = input("请输入要查询的学号: ")
#             result = find_student_by_id(students, keyword)
#             if result == None:
#                 print("未找到该学生")
#             else:
#                 show_student(result)
#         case 3:
#             print_all_students(students)
#         case 4:
#             break
#         case _:
#             print("输入错误，请重新输入")

























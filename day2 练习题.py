# #列表基本操作
# music = ["寻","虚幻与现实","花落时相遇","不重逢","温暖的房子","疯人院"]
# #1
# print(len(music))
# #2
# music.append("新世界")
# #3
# music.remove("虚幻与现实")
# #4
# for i in music:
#     print(i)
from itertools import count


#
# #字典基本操作
# book = {"title":"python入门","author":"张老师","price":59.0,"stock":10}
# print(f"书名: {book['title']}  作者: {book['author']}")
# book["price"] = 49.0
# book["publisher"] = "清华大学出版社"
# book.pop("stock")
# for i in book:
#     print(i,book[i])



#
# #集合去重
# nums = [1,2,2,3,3,4,5,6,7,7,8 ,10]
# nums = set(nums)
# print(len(nums))
# if 5 in nums:
#     print("5在集合中")
# else:
#     print("5不在集合中")
# nums = list(nums)
# nums.sort()
# print(nums)





# #函数封装+异常处理
# def celsius_to_fahrenheit(celsius):
#     try:
#         celsius = float(celsius)
#         fahrenheit = celsius * 9/5 + 32
#         return fahrenheit
#     except ValueError:
#         print("输入的摄氏度不是数字")
#         return None
#
# def fahrenheit_to_celsius(fahrenheit):
#     try:
#         fahrenheit = float(fahrenheit)
#         celsius = (fahrenheit - 32) * 5/9
#         return round(celsius, 1)
#     except ValueError:
#         print("输入的华氏度不是数字")
#         return None
#
# def show_menu():
#     print("=========================================")
#     print("            温度转换小程序             ")
#     print("            1. 摄氏度转华氏度")
#     print("            2. 华氏度转摄氏度")
#     print("            3. 退出")
#     print("=========================================")
#
# while True:
#     show_menu()
#     match input("请输入你要执行的操作: "):
#         case "1":
#            try:
#                 celsius = input("请输入摄氏度: ")
#                 fahrenheit = celsius_to_fahrenheit(celsius)
#                 if fahrenheit is not None:
#                     print(f"{celsius} 摄氏度等于 {fahrenheit} 华氏度")
#            except:
#                print("输入错误，请重新输入")
#         case "2":
#             try:
#                 fahrenheit = input("请输入华氏度: ")
#                 celsius = fahrenheit_to_celsius(fahrenheit)
#                 if celsius is not None:
#                     print(f"{fahrenheit} 华氏度等于 {celsius} 摄氏度")
#             except:
#                 print("输入错误，请重新输入")
#         case "3":
#             print("退出程序")
#             break
#         case _:
#             print("输入无效，请重新输入")





# #
# 字典+列表 综合
# students = [{"name": "张三" , "age":18 , "score":85},{"name": "李四" , "age":19 , "score":92},
#             {"name": "王五" , "age":18 , "score":47},{"name": "赵六" , "age":20 , "score":76}]
#
# def show_students(students):
#     for student in students:
#         print(f"姓名: {student['name']}  年龄: {student['age']}  分数: {student['score']}")
#     print("打印完成")
# def find_student_by_name(students, name):
#     for student in students:
#         if student['name'] == name:
#             return student
#     return None
#
# def get_average(students):
#     total = 0
#     for student in students:
#         total += student['score']
#     return round(total / len(students),1)
#
# def get_pass_count(students):
#     count = 0
#     for student in students:
#         if student['score'] >= 60:
#             count += 1
#     return count
#
# show_students(students)
# print("找到的学生是:", find_student_by_name(students, "张三"))
# print("通过人数是:", get_pass_count(students))
# print("平均分是:", get_average(students))




#文件读取+数据统计
def read_file(filename):
    students = []
    try:
        file = open(filename, "r", encoding="utf-8")
        for i in file:
            i = i.strip()
            name,score_str = i.split(",")
            info_dict = {"name":name,"score":int(score_str)}
            students.append(info_dict)
        file.close()
        return students
    except :
        print("文件未找到")
        return None

def get_stats(students):
    sum = 0
    for student in students:
        sum += student["score"]
    average = sum / len(students)
    average = round(average, 1)
    list1 = []
    for i in students:
        list1.append(i["score"])
    return max(list1), min(list1), average

students = read_file("  scores.txt")
print(f"加载成功,共{len(students)}名学生")
max_score, min_score, average_score = get_stats(students)
print(f"最高分 :{max_score},最低分 :{min_score},平均分 :{average_score}")
















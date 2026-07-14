# #成绩等级判定
# while True:
#     score = input()
#     if score == "q":
#         break
#     score = int(score)
#     if score > 100 or score < 0:
#         print("成绩无效")
#     elif score >= 0 and score <= 59:
#         print("E")
#     elif score >= 60 and score <= 69:
#         print("D")
#     elif score >= 70 and score <= 79:
#         print("C")
#     elif score >= 80 and score <= 89:
#         print("B")
#     elif score >= 90 and score <= 100:
#         print("A")




#
# #天数计算
# year = int(input("请输入年份: "))
# month = int(input("请输入月份: "))
# if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
#     list1 = [1,3,5,7,8,10,12]
#     list2 = [4,6,9,11]
#     list3 = [2]
#     if month in list1:
#         day = 31
#         print(f"{year}年{month}月有{day}天")
#     elif month in list2:
#         day = 30
#         print(f"{year}年{month}月有{day}天")
#     elif month in list3:
#         day = 29
#         print(f"{year}年{month}月有{day}天")
# else:
#     list1 = [1, 3, 5, 7, 8, 10, 12]
#     list2 = [4, 6, 9, 11]
#     list3 = [2]
#     if month in list1:
#         day = 31
#         print(f"{year}年{month}月有{day}天")
#     elif month in list2:
#         day = 30
#         print(f"{year}年{month}月有{day}天")
#     elif month in list3:
#         day = 28
#         print(f"{year}年{month}月有{day}天")



#
# #数字特征统计
# n = input("请输入一个整数: ")
# sum = 0
# sum_1 = 0
# sum_2 = 0
# for i in range(len(n)):
#     num = int(i)
#     sum += num
#     if num % 2 == 0:
#         sum_2 += num
#     else:
#         sum_1 += num
# print(f"各位数字之和为: {sum}")
# print(f"奇数个数: {sum_1}  偶数个数: {sum_2}")
# if n == n[::-1]:
#     print("是回文数")
# else:
#     print("不是回文数")




#
# #密码强度检测
# code = input()
# score = 0
# if len(code) >= 8:
#     score += 1
# num_digit = 0
# num_lower = 0
# num_upper = 0
# num_str = 0
# for i in code:
#     if i.isdigit():
#         num_digit += 1
#     elif i.islower():
#         num_lower += 1
#     elif i.isupper():
#         num_upper += 1
#     else:
#         num_str += 1
# if num_digit != 0:
#     score += 1
# elif num_lower != 0:
#     score += 1
# elif num_upper != 0:
#     score += 1
# elif num_str != 0:
#     score += 1
# if score >= 0 and score <= 1:
#     print("密码强度较弱")
# elif score >= 2 and score <= 3:
#     print("密码强度中等")
# elif score >= 4 and score <= 5:
#     print("密码强度较强")




#
# #学生成绩录入与分析
# stu_dict = {}
# while True:
#     name = input("请输入学生姓名: ")
#     if name == "done":
#         break
#     score = int(input("请输入学生成绩: "))
#     stu_dict[name] = score
# list1 = []
# list2 = []
# for item in stu_dict:
#     num = stu_dict[item]
#     list1.append(num)
#     list2.append(item)
# ave = sum(list1) / len(list1)
# num_max = max(list1)
# num_min = min(list1)
# name_max = list2[list1.index(num_max)]
# name_min = list2[list1.index(num_min)]
# good = 0
# bad = 0
# for i in list1:
#     if i >= 60:
#         good += 1
#     else:
#         bad += 1
# print(f"参与人数: {len(list1)}")
# print(f"平均分: {ave:.1f}")
# print(f"最高分: {num_max} ({name_max})")
# print(f"最低分: {num_min} ({name_min})")
# print(f"及格: {good}人  不及格: {bad}人")




















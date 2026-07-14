# #计算器
# def calculator():
#     print("计算器已启用")
#     print("支持 '+ - * / % **' 运算符,输入 Q/q 退出程序")
#     while True:
#         data = input("请输入计算式(例: 1 + 1):")
#         if data.lower() == "q":
#             print("运行已结束，期待下次使用")
#             break
#         num1 , op , num2 = data.split()
#         num1 = float(num1)
#         num2 = float(num2)
#         if op == "+":
#             result = num1 + num2
#         elif op == "-":
#             result = num1 - num2
#         elif op == "*":
#             result = num1 * num2
#         elif op == "/":
#             result = num1 / num2
#         elif op == "%":
#             result = num1 % num2
#         elif op == "**":
#             result = num1 ** num2
#         else:
#             print("输入的运算符有误,请重新输入")
#             continue
#         print(f"计算结果 result = {result}\n")
#
# calculator()




#猜数字
import random
def num_game():
    answer = random.randint(1,100)
    print("欢迎来到猜数字小游戏,数字范围(1 ~ 100),输入 Q/q 退出游戏")
    while True:
        guess = input("请输入你猜的数字(1 ~ 100): ")
        if guess.lower() == "q":
            print("游戏已结束，期待下次游戏")
            break
        guess = int(guess)
        if guess > 100:
            print("输入的数字超出范围,请重新输入")
            continue
        elif guess < 1:
            print("输入的数字超出范围,请重新输入")
            continue

        if guess > answer:
            print("你猜的数字偏大")
        elif guess < answer:
            print("你猜的数字偏小")
        else:
            print("恭喜你猜对了!")
            break

num_game()

# from openai import OpenAI
# client = OpenAI(
#     api_key="sk-nawrukkmeoumzuhtykoxtxpfwenoztejothuugcrkylhovqv",
#     base_url="https://api.siliconflow.cn/v1"
# )
# user_input = input("请输入你的问题: ")
# response = client.chat.completions.create(
#     model="deepseek-ai/DeepSeek-V3",
#     messages=[
#         {"role": "system", "content": "你是一个友好的AI助手,名字叫小飒,会尽力帮我解决问题"},
#         {"role": "user", "content": user_input},
#     ],
#     stream=False
# )
# print(f"\n小飒: {response.choices[0].message.content}")
# print(f"总计消耗 tokens: {response.usage.total_tokens}")






# from openai import OpenAI
#
# client = OpenAI(
#     api_key="sk-nawrukkmeoumzuhtykoxtxpfwenoztejothuugcrkylhovqv",
#     base_url="https://api.siliconflow.cn/v1"
# )
#
# # 封装通用函数
# def ask_ai(prompt):
#     response = client.chat.completions.create(
#         model="deepseek-ai/DeepSeek-V3",
#         messages=[
#             {"role": "user", "content": prompt},
#         ],
#         stream=False
#     )
#     return response.choices[0].message.content
# # 1. 普通 Prompt
# normal_prompt = "什么是函数"
#
# # 2. 结构化 Prompt（角色 + 背景 + 任务 + 要求）
# structured_prompt = """
# # 角色：你是一名面向零基础学员的Python编程教师
# # 背景：学生刚接触编程，对"函数"这个概念完全没有了解
# # 任务：请用通俗易懂的语言解释"什么是函数"
# # 要求：
# 1. 使用生活中的案例辅助说明
# 2. 语言通俗，避免专业术语堆砌
# 3. 回答不超过5句话
# """
#
# # 分别调用
# print("【普通 Prompt 回答】")
# print(ask_ai(normal_prompt))
#
# print("\n")
#
# print("【结构化 Prompt 回答】")
# print(ask_ai(structured_prompt))
#
# # 对比差异：
# # 1. 普通Prompt回答往往偏学术、冗长，容易堆砌专业术语；
# #    结构化Prompt因限定了角色和受众，回答更通俗、更有针对性。
# # 2. 结构化Prompt通过"要求"约束了输出格式（如不超过5句话），
# #    回答更精炼可控；普通Prompt则难以控制长度和风格。






# from openai import OpenAI
#
# client = OpenAI(
#     api_key="sk-nawrukkmeoumzuhtykoxtxpfwenoztejothuugcrkylhovqv",
#     base_url="https://api.siliconflow.cn/v1"
# )
#
# SYSTEM_PROMPT = """你是郑州航空工业管理学院校园信息助手，熟悉学校的各类信息，
# 包括但不限于：校区地址、食堂、院系专业、图书馆、宿舍、社团活动等。
# 请用简洁友好的方式回答学生的提问。"""
#
#
# def ask_campus(question):
#     response = client.chat.completions.create(
#         model="deepseek-ai/DeepSeek-V3",
#         messages=[
#             {"role": "system", "content": SYSTEM_PROMPT},
#             {"role": "user", "content": question},
#         ],
#         stream=False
#     )
#     return response.choices[0].message.content
#
#
# print("=== 郑州航院校园信息助手 (输入 quit 退出) ===\n")
#
# while True:
#     question = input("请输入你的问题: ")
#     if question.strip().lower() == "quit":
#         print("再见！")
#         break
#
#     answer = ask_campus(question)
#     print(f"\n助手: {answer}\n")






# from openai import OpenAI
#
# client = OpenAI(
#     api_key="sk-nawrukkmeoumzuhtykoxtxpfwenoztejothuugcrkylhovqv",
#     base_url="https://api.siliconflow.cn/v1"
# )
#
# messages = [
#     {"role": "system", "content": "你是郑州航空工业管理学院校园信息助手，简洁回答学生问题"}
# ]
#
# print("欢迎使用校园问答助手，输入 quit 退出\n")
#
# while True:
#     user_input = input("你: ")
#     if user_input.strip().lower() == "quit":
#         print("再见！")
#         break
#
#     messages.append({"role": "user", "content": user_input})
#
#     response = client.chat.completions.create(
#         model="deepseek-ai/DeepSeek-V3",
#         messages=messages,
#         stream=False
#     )
#
#     assistant_reply = response.choices[0].message.content
#     messages.append({"role": "assistant", "content": assistant_reply})
#
#     print(f"助手: {assistant_reply}\n")
#
# # 多轮对话测试记录：
# # 第1轮 → 输入: 我叫张三，人工智能专业
# #         助手: 你好张三！人工智能专业是我们学校的重要专业之一...
# # 第2轮 → 输入: 学校食堂推荐哪些？
# #         助手: 学校有多个食堂，一食堂菜品丰富价格实惠，二食堂特色窗口较多...
# # 第3轮 → 输入: 我叫什么名字？什么专业？
# #         助手: 你叫张三，是人工智能专业的同学。
# # 结论: AI通过messages上下文成功记住了用户姓名和专业信息。






from openai import OpenAI
import json

client = OpenAI(
    api_key="sk-nawrukkmeoumzuhtykoxtxpfwenoztejothuugcrkylhovqv",
    base_url="https://api.siliconflow.cn/v1"
)

FEW_SHOT_PROMPT = """你是一个课程信息提取助手，请从文本中提取课程信息并输出为JSON格式。

以下是示例：

输入：周一 8:00-9:40 高等数学 教学楼A301 张老师
输出：{"星期": "周一", "时间": "8:00-9:40", "课程": "高等数学", "教室": "A301", "教师": "张老师"}

输入：周四 13:00-14:40 数据结构 教学楼D402 赵老师
输出：{"星期": "周四", "时间": "13:00-14:40", "课程": "数据结构", "教室": "D402", "教师": "赵老师"}

请严格按照以上格式，只输出JSON，不要输出其他内容。

现在请提取以下文本：
"""

 
def extract_course(text):
    prompt = FEW_SHOT_PROMPT + text
    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-V3",
        messages=[
            {"role": "user", "content": prompt},
        ],
        stream=False
    )
    return response.choices[0].message.content


test_texts = [
    "周二 14:00-15:40 Python编程 实训楼B205 李老师",
    "周三 10:00-11:40 大学英语 教学楼C102 王老师",
    "周五 19:00-20:40 篮球课 体育馆 刘教练",
]

for i, text in enumerate(test_texts, 1):
    print(f"原文: {text}")
    result = extract_course(text)
    print(f"提取: {result}\n")











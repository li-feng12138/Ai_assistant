import os
from openai import OpenAI

client = OpenAI(
    api_key="sk-nawrukkmeoumzuhtykoxtxpfwenoztejothuugcrkylhovqv",
    base_url="https://api.siliconflow.cn/v1"
)

# 全局系统提示词
SYSTEM_PROMPT = "你是一个冷酷的AI助手,你的名字叫小飒,你会帮助我解决各种问题"

# 专用结构化 Prompt
CONCEPT_PROMPT = """你是一个专业的编程教师，擅长用通俗易懂的语言解释编程概念。
要求：
1. 先给出概念的简明定义
2. 用生活中的类比帮助理解
3. 提供一个简单的代码示例
4. 指出常见的误区和注意事项"""

CODE_PROMPT = """你是一个资深的代码审查专家，擅长分析和解释代码。
要求：
1. 逐行或逐块分析代码的功能
2. 说明代码的整体逻辑和执行流程
3. 指出代码中可能存在的问题或优化空间
4. 给出改进建议"""

PROMPT_MAP = {
    "1": ("自由问答", SYSTEM_PROMPT),
    "2": ("编程概念解释", CONCEPT_PROMPT),
    "3": ("代码解析", CODE_PROMPT),
}

all_messages = []


def print_menu():
    print("=" * 30)
    print("   AI学习助手 - 功能菜单")
    print("=" * 30)
    print("  1. 自由问答")
    print("  2. 编程概念解释")
    print("  3. 代码解析")
    print("  0. 退出")
    print("=" * 30)


def save_to_txt(messages, filename="chat_history.txt"):
    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(save_path, "w", encoding="utf-8") as f:
        for msg in messages:
            if msg["role"] == "system":
                f.write(f"[系统提示词] {msg['content']}\n")
                f.write("-" * 40 + "\n")
            elif msg["role"] == "user":
                f.write(f"你: {msg['content']}\n")
            elif msg["role"] == "assistant":
                f.write(f"小飒: {msg['content']}\n")
            f.write("\n")
    print(f"\n对话历史已保存到 {save_path}")


def chat(mode_name, system_content):
    print(f"\n--- 已进入【{mode_name}】模式 (输入 quit 返回菜单) ---\n")
    messages = [{"role": "system", "content": system_content}]

    while True:
        user_input = input("你: ").strip()
        if user_input.lower() == "quit":
            print(f"已退出【{mode_name}】模式\n")
            break

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=messages,
            stream=False
        )

        assistant_reply = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_reply})

        print(f"\n小飒: {assistant_reply}")
        print(f"[本次消耗 tokens: {response.usage.total_tokens}]\n")

    return messages


while True:
    print_menu()
    choice = input("请选择功能 (0-3): ").strip()

    if choice == "0":
        if all_messages:
            save_to_txt(all_messages)
        print("再见！")
        break
    elif choice in PROMPT_MAP:
        mode_name, system_content = PROMPT_MAP[choice]
        history = chat(mode_name, system_content)
        all_messages.extend(history)
    else:
        print("输入无效，请输入 0-3 之间的数字！\n")








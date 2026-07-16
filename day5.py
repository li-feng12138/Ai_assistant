import os
import requests

API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_KEY = "sk-nawrukkmeoumzuhtykoxtxpfwenoztejothuugcrkylhovqv"
MODEL = "deepseek-ai/DeepSeek-V3"

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

ALIAS_MAP = {
    "信院": "信息工程学院",
    "航院": "航空工程学院",
    "管院": "工商管理学院",
    "文院": "文法学院",
    "教务": "教务处",
    "学工": "学生处",
    "后勤": "后勤报修",
    "保卫": "保卫处",
    "一卡通": "校园卡中心",
    "宿管": "宿管中心",
}

IDENTITIES = {
    "1": {
        "name": "新生",
        "desc": "我是新生，刚入学，对校园还不熟悉",
        "questions": [
            "报到需要带哪些材料？具体流程是什么？",
            "学费和住宿费怎么缴？什么时候缴？",
            "宿舍是怎么安排的？能换宿舍吗？",
            "校园里有哪些常见的骗局？怎么防范？",
        ],
    },
    "2": {
        "name": "老生",
        "desc": "我是老生，需要办理校园事务",
        "questions": [
            "怎么开在读证明？",
            "校园卡丢了怎么补办？",
            "转专业需要什么条件和流程？",
            "图书馆开放时间是什么？",
        ],
    },
    "3": {
        "name": "教师",
        "desc": "我是教师，需要办理行政事务",
        "questions": [
            "科研经费报销流程是什么？",
            "如何申请调课？",
            "教室设备故障怎么报修？",
            "科研项目申报流程是什么？",
        ],
    },
}

SYSTEM_PROMPT = """你是郑州航空工业管理学院校园AI问答助手"小航"。
请严格遵守以下规则：
1. 数据源边界：仅依据提供的校园资料（md文档）回答，无相关内容统一回复："该问题超出我的知识范围，建议您咨询校值班室（电话：0371-63456789）获取帮助。"禁止猜测或编造。
2. 真实信息边界：禁止编造任何电话、地址、金额、时间、人名等具体信息，必须严格复制资料原文。
3. 资金反诈边界：涉及转账、缴费等内容时，必须在回答末尾附加："⚠️ 温馨提示：任何要求向个人账户转账的行为均可能是诈骗，请务必通过官方渠道核实。"
4. 心理应急边界：当识别到用户提及轻生、自杀、自残、不想活、绝望等关键词或相关意图时，必须立即输出校心理援助热线（0371-63456303 / 全国热线400-161-9995），并建议联系辅导员，不得回避或仅做普通回答。
5. 权限边界：拒绝查询成绩、课表、校园卡余额等个人校内数据，回复："暂不支持此类查询，请前往相关教务/财务系统操作。"
6. 溯源边界：每条有效回答末尾必须标注参考来源，格式为"📎 来源：xxx.md"。
请用简洁友好的方式回答。"""


def load_md(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return ""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def resolve_alias(text):
    for alias, full_name in ALIAS_MAP.items():
        text = text.replace(alias, full_name)
    return text


def call_api(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
    }
    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        return "⚠️ 请求超时，请检查网络后重试。"
    except requests.exceptions.ConnectionError:
        return "⚠️ 网络连接失败，请检查网络设置。"
    except Exception as e:
        return f"⚠️ 请求出错：{e}"


def ai_answer(user_input, identity_desc, source_files):
    user_input = resolve_alias(user_input)

    knowledge = ""
    for fname in source_files:
        content = load_md(fname)
        if content:
            knowledge += f"\n--- {fname} ---\n{content}\n"

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": f"用户身份：{identity_desc}"},
        {"role": "system", "content": f"以下是校园资料：\n{knowledge}"},
        {"role": "user", "content": user_input},
    ]

    return call_api(messages)


def print_boundary():
    print("=" * 50)
    print("  郑州航院校园AI问答助手 —— 小航")
    print("=" * 50)
    print("【使用边界声明】")
    print("  本助手仅基于校内资料提供常见问答，不能替代官方通知。")
    print("  涉及重要事务请以学校官方公告和相关部门答复为准。")
    print("=" * 50)


def print_main_menu():
    print("\n【主菜单】")
    print("  1. 选择身份并开始提问")
    print("  2. 校园电话黄页（离线可用）")
    print("  0. 退出")


def print_identity_menu():
    print("\n【选择身份】")
    for key, info in IDENTITIES.items():
        print(f"  {key}. {info['name']} - {info['desc']}")
    print("  0. 返回主菜单")


def print_quick_questions(identity_key):
    info = IDENTITIES[identity_key]
    print(f"\n【{info['name']}快捷问题】")
    for i, q in enumerate(info["questions"], 1):
        print(f"  {i}. {q}")
    print("  0. 返回上一级")


def show_phone_directory():
    print("\n" + "=" * 50)
    print("  📞 校园电话黄页（离线可用）")
    print("=" * 50)
    content = load_md("../Data/03电话黄页.md")
    if content:
        print(content)
    else:
        print("⚠️ 黄页文件未找到，请检查 data/ 目录。")
    print("=" * 50)


def chat_loop(identity_key):
    info = IDENTITIES[identity_key]
    print(f"\n✅ 已切换为【{info['name']}】身份")
    print_quick_questions(identity_key)

    while True:
        print("\n请输入问题（输入编号快捷提问，输入 0 返回身份选择）：")
        user_input = input("你: ").strip()

        if user_input == "0":
            print_identity_menu()
            id_choice = input("请选择身份: ").strip()
            if id_choice in IDENTITIES:
                chat_loop(id_choice)
                return
            elif id_choice == "0":
                return
            else:
                print("⚠️ 无效选择，请重新操作。")
                continue

        if user_input.lower() == "q":
            break

        if user_input in [str(i) for i in range(1, 5)]:
            user_input = info["questions"][int(user_input) - 1]
            print(f"你: {user_input}")

        if not user_input:
            continue

        source_files = ["01新生入学.md", "02办事流程.md", "03电话黄页.md", "04应急防骗.md"]
        answer = ai_answer(user_input, info["desc"], source_files)
        print(f"\n小航: {answer}")


def main():
    print_boundary()

    while True:
        print_main_menu()
        choice = input("请选择: ").strip()

        if choice == "0":
            print("再见！欢迎下次使用。")
            break
        elif choice == "2":
            show_phone_directory()
        elif choice == "1":
            print_identity_menu()
            id_choice = input("请选择身份: ").strip()
            if id_choice in IDENTITIES:
                chat_loop(id_choice)
            elif id_choice == "0":
                 continue
            else:
                print("⚠️ 无效选择，请重新操作。")
        else:
            print("⚠️ 无效选择，请输入 0/1/2。")


if __name__ == "__main__":
    main()


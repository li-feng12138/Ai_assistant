# ==========================================
# 全局配置文件 - 存放API相关固定配置
# ==========================================

# 硅基流动API接口地址
API_BASE_URL = "https://api.siliconflow.cn/v1/chat/completions"

# 使用的模型名称
MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"

# 你的API密钥
API_KEY = "sk-nawrukkmeoumzuhtykoxtxpfwenoztejothuugcrkylhovqv"






# ==========================================
# 提示词管理模块 - 读取资料、构建系统提示词
# ==========================================

import requests
import streamlit as st
from pathlib import Path

# 设置浏览器标签页标题
st.set_page_config(page_title="校园信息查询助手")

# data文件夹路径：md文件和day6.py在同一目录下
DATA_DIR = Path(__file__).parent

# 别名词典：统一学校相关简称
ALIAS_DICT = {
    "航院": "郑州航空工业管理学院",
    "ZUA": "郑州航空工业管理学院",
    "郑航": "郑州航空工业管理学院",
    "新校区": "郑州航空工业管理学院龙子湖校区",
    "老校区": "郑州航空工业管理学院大学路校区",
    "信工": "信息工程学院",
    "航工": "航空工程学院",
    "工商": "工商管理学院",
    "文法": "文法学院",
}

def load_all_docs():
    """读取data文件夹下所有.md文件，合并返回全部文本内容"""
    all_text = ""
    # 遍历data文件夹下的所有md文件（只读取编号开头的校园资料）
    for md_file in sorted(DATA_DIR.glob("[0-9]*.md")):
        try:
            content = md_file.read_text(encoding="utf-8")
            all_text += content + "\n\n"
        except Exception as e:
            all_text += f"[读取{md_file.name}失败: {e}]\n\n"
    return all_text

def get_identity_prompt(identity):
    """根据用户身份返回对应的角色语气提示词"""
    prompts = {
        "新生": (
            "你是'小航'，郑州航空工业管理学院的新生专属AI助手。"
            "你的说话语气亲切友好，像一位热情的学长/学姐，"
            "耐心解答新生关于入学、报到、校园生活等各类问题。"
            "尽量用简单易懂的语言，避免使用过于专业的术语。"
        ),
        "在校生": (
            "你是'小航'，郑州航空工业管理学院的在校生AI助手。"
            "你的说话语气轻松自然，像一位靠谱的同学朋友，"
            "帮助在校生解答办事流程、学业安排、校园服务等问题。"
            "回答要实用高效，直击要点。"
        ),
        "教师": (
            "你是'小航'，郑州航空工业管理学院的教师服务AI助手。"
            "你的说话语气正式专业，礼貌得体，"
            "协助教师了解校园行政流程、联系方式、应急处理等信息。"
            "回答要准确规范，体现专业性。"
        ),
    }
    # 如果传入的身份不在字典中，默认返回新生提示词
    return prompts.get(identity, prompts["新生"])

def get_safety_rules():
    """返回6条防幻觉硬性规则"""
    rules = (
        "【防幻觉硬性规则 - 必须严格遵守】\n"
        "1. 禁止编造任何电话号码、金额、日期等具体数据，所有信息必须来自上方校园资料。\n"
        "2. 涉及转账、缴费等金钱相关话题时，必须附加反诈提醒：'请注意核实对方身份，学校不会要求向个人账户转账。'\n"
        "3. 涉及心理危机、人身安全等紧急问题时，必须优先提供心理援助热线（400-161-9995）和保卫处电话（0371-63456301），并建议立即联系辅导员。\n"
        "4. 如果校园资料中没有相关信息，必须如实告知'抱歉，当前资料中未包含该信息，建议您咨询相关部门。'，禁止猜测或编造。\n"
        "5. 不支持查询个人个人信息（如成绩、宿舍号、学号等），如遇此类问题请回复'抱歉，我无法查询个人信息，请联系相关部门。'\n"
        "6. 每次回答末尾需标注资料来源，格式为'📎 资料来源：《xxx》'，如资料中无相关内容则标注'📎 资料来源：暂无相关资料'。"
    )
    return rules

def build_system_prompt(identity, campus_docs):
    """
    拼接完整的system提示词
    参数：identity - 用户身份（新生/在校生/教师）
          campus_docs - 校园资料文本内容
    返回：组装好的完整系统提示文本
    """
    # 获取身份提示词
    identity_prompt = get_identity_prompt(identity)
    # 获取防幻觉规则
    safety_rules = get_safety_rules()

    # 拼接完整系统提示词
    system_prompt = (
        f"{identity_prompt}\n\n"
        f"【校园参考资料】\n以下是你可以参考的校园资料内容，请严格基于这些资料回答问题：\n"
        f"{campus_docs}\n"
        f"{safety_rules}"
    )
    return system_prompt







# ==========================================
# API调用模块 - 封装AI对话请求
# ==========================================

def chat_with_ai(user_question, system_prompt):
    """
    向硅基流动API发送对话请求
    参数：user_question - 用户提问内容
          system_prompt - 完整系统提示词
    返回：AI回答文本 或 错误提示文本
    """
    # 构造请求头，携带Bearer鉴权
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    # 构造请求体数据
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question},
        ],
    }

    try:
        # 发送POST请求，设置30秒超时
        response = requests.post(API_BASE_URL, json=payload, headers=headers, timeout=30)

        # 检查HTTP状态码是否为401（API密钥失效）
        if response.status_code == 401:
            return "❌ API密钥无效或已过期，请检查API_KEY配置。"

        # 检查其他HTTP错误
        response.raise_for_status()

        # 解析返回的JSON数据
        data = response.json()
        # 提取AI回答文本
        ai_reply = data["choices"][0]["message"]["content"]
        return ai_reply

    except requests.exceptions.Timeout:
        return "⏰ 请求超时，服务器响应时间过长，请稍后再试。"

    except requests.exceptions.ConnectionError:
        return "🌐 网络连接失败，请检查网络设置后重试。"

    except KeyError:
        return "📦 API返回数据格式异常，未能找到有效回答字段。"

    except Exception as e:
        return f"❓ 发生未知错误：{e}"






# ==========================================
# 主程序 - Streamlit网页界面
# ==========================================

try:
    # ---------- 页面标题 ----------
    st.title("🎓 小航 - 校园信息AI助手")
    st.caption("郑州航空工业管理学院 | 基于硅基流动大模型")

    # ---------- 身份选择下拉框 ----------
    identity = st.selectbox(
        "请选择你的身份：",
        ["新生", "在校生", "教师"],
    )

    # ---------- 推荐提问按钮（按身份分3组，每组4个） ----------
    question_buttons = {
        "新生": [
            "新生报到需要带哪些材料？",
            "学费和住宿费分别是多少？",
            "宿舍是怎么分配的？",
            "入学后如何防止被骗？",
        ],
        "在校生": [
            "如何开具在读证明？",
            "校园卡丢了怎么补办？",
            "转专业需要什么条件？",
            "图书馆的开放时间是什么？",
        ],
        "教师": [
            "各院系办公室联系电话是多少？",
            "教务处和财务处的联系方式？",
            "遇到紧急情况如何处理？",
            "心理咨询中心在哪里？如何预约？",
        ],
    }

    # 显示当前身份对应的4个推荐按钮
    st.markdown("##### 💡 推荐提问（点击快速填充）")
    cols = st.columns(4)
    for i, btn_text in enumerate(question_buttons[identity]):
        if cols[i].button(btn_text, key=f"{identity}_{i}"):
            st.session_state["user_input"] = btn_text

    # ---------- 文本输入框 ----------
    default_input = st.session_state.get("user_input", "")
    user_question = st.text_input("请输入你的问题：", value=default_input, key="input_box")

    # ---------- 提交按钮 ----------
    if st.button("🚀 发送提问"):
        if not user_question.strip():
            st.warning("⚠️ 请输入问题后再提交！")
        else:
            md_files = list(DATA_DIR.glob("[0-9]*.md"))
            if not md_files:
                st.warning("⚠️ 未找到任何.md资料文件，请确认资料文件存在！")
            else:
                with st.spinner("小航正在思考中..."):
                    campus_docs = load_all_docs()
                    system_prompt = build_system_prompt(identity, campus_docs)
                    answer = chat_with_ai(user_question, system_prompt)
                    st.markdown("---")
                    st.markdown("### 🤖 小航的回答：")
                    st.markdown(answer)

    # ---------- 底部静态电话黄页板块 ----------
    st.markdown("---")
    st.markdown("### 📞 校园电话黄页")

    col_left, col_right = st.columns(2)

    with col_left:
        left_table = (
            "| 部门 | 电话 |\n"
            "| --- | --- |\n"
            "| 校值班室 | 0371-63456789 |\n"
            "| 招生办 | 0371-63456001 |\n"
            "| 教务处 | 0371-63456002 |\n"
            "| 学生处 | 0371-63456003 |\n"
            "| 财务处 | 0371-63456004 |\n"
            "| 信息工程学院办公室 | 0371-63456101 |\n"
            "| 航空工程学院办公室 | 0371-63456102 |\n"
            "| 工商管理学院办公室 | 0371-63456103 |\n"
            "| 文法学院办公室 | 0371-63456104 |\n"
        )
        st.markdown(left_table)

    with col_right:
        right_table = (
            "| 部门 | 电话 |\n"
            "| --- | --- |\n"
            "| 后勤报修 | 0371-63456201 |\n"
            "| 宿管中心 | 0371-63456202 |\n"
            "| 食堂管理 | 0371-63456203 |\n"
            "| 校园卡中心 | 0371-63456204 |\n"
            "| 保卫处 | 0371-63456301 |\n"
            "| 校医院 | 0371-63456302 |\n"
            "| 心理咨询中心 | 0371-63456303 |\n"
            "| 心理咨询热线 | 0371-63456304 |\n"
        )
        st.markdown(right_table)

    st.markdown("---")
    st.caption("© 2025 小航校园AI助手 | 郑州航空工业管理学院")

except Exception as e:
    st.error(f"⚠️ 程序运行出现异常：{e}")
    st.info("请检查配置或联系管理员。")




# 核心功能
#
# 身份切换：下拉框选择 新生 / 在校生 / 教师，AI 回答语气自动适配
#
# AI 问答：基于4份校园资料（新生入学、办事流程、电话黄页、应急防骗）回答问题
#
# 推荐提问：每种身份4个快捷按钮（共12个），点击自动填充问题
#
# 静态电话黄页：底部双列展示17个校园电话，断网也能查看
#
# 防护机制
# 6条防幻觉规则：不编造数据、反诈提醒、心理危机处理、无资料如实告知、拒绝个人信息查询、标注资料来源
#
# 5层异常捕获：超时 / 网络失败 / 401密钥失效 / 数据格式异常 / 未知错误
#
# 全局兜底：页面级 try-except，程序不崩溃



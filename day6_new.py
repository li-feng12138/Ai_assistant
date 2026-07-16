# 小航 - 校园信息查询助手
# 功能：多会话AI问答 + 静态电话黄页
# 技术：Streamlit + 硅基流动API + requests

#第一部分：导入库
import requests
import streamlit as st
from pathlib import Path
import json
import os




#第二部分：全局配置

# 硅基流动API接口地址
API_BASE_URL = "https://api.siliconflow.cn/v1/chat/completions"

# 使用的模型名称
MODEL_NAME = "deepseek-ai/DeepSeek-V3"

# API密钥
API_KEY = "sk-nawrukkmeoumzuhtykoxtxpfwenoztejothuugcrkylhovqv"

# data文件夹路径：md文件和day6_new.py在同一目录下
DATA_DIR = Path(__file__).parent

# 会话文件存储目录
SESSIONS_DIR = DATA_DIR / "sessions"







#第三部分：提示词管理函数

def load_all_docs():
    """读取同级目录下所有编号开头的.md文件，合并返回全部文本内容"""
    all_text = ""
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
    identity_prompt = get_identity_prompt(identity)
    safety_rules = get_safety_rules()
    system_prompt = (
        f"{identity_prompt}\n\n"
        f"【校园参考资料】\n以下是你可以参考的校园资料内容，请严格基于这些资料回答问题：\n"
        f"{campus_docs}\n"
        f"{safety_rules}"
    )
    return system_prompt








#第四部分：API调用函数

def chat_with_ai_stream(user_question, system_prompt, placeholder):
    """
    向硅基流动API发送流式对话请求，逐步显示AI回答
    参数：user_question - 用户提问内容
          system_prompt - 完整系统提示词
          placeholder - Streamlit的empty占位组件，用于逐步显示
    返回：AI完整回答文本 或 错误提示文本
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question},
        ],
        "stream": True,
    }
    try:
        response = requests.post(API_BASE_URL, json=payload, headers=headers, timeout=30, stream=True)
        if response.status_code == 401:
            return "❌ API密钥无效或已过期，请检查API_KEY配置。"
        if response.status_code == 429:
            return "⏰ 请求过于频繁，请稍后再试。"
        response.raise_for_status()

        full_response = ""
        for line in response.iter_lines():
            if line:
                line = line.decode("utf-8")
                if line.startswith("data: "):
                    data_str = line[6:]
                    if data_str.strip() == "[DONE]":
                        break
                    try:
                        data = json.loads(data_str)
                        chunk = data["choices"][0].get("delta", {}).get("content", "")
                        if chunk:
                            full_response += chunk
                            placeholder.markdown(full_response + "▌")
                    except json.JSONDecodeError:
                        continue
        placeholder.markdown(full_response)
        return full_response
    except requests.exceptions.Timeout:
        return "⏰ 请求超时，请稍后再试。"
    except requests.exceptions.ConnectionError:
        return "🌐 网络连接失败，请检查网络。"
    except Exception as e:
        return f"❓ 发生未知错误：{e}"


# 第四部分（补充）：会话持久化函数

def save_conversations():
    """将所有会话保存到sessions目录，每个会话一个JSON文件"""
    if not SESSIONS_DIR.exists():
        SESSIONS_DIR.mkdir(parents=True, exist_ok=True)
    existing_files = set(f.name for f in SESSIONS_DIR.glob("conv_*.json"))
    current_files = set()
    for conv in st.session_state.conversations:
        file_name = f"conv_{conv['name']}.json"
        current_files.add(file_name)
        file_path = SESSIONS_DIR / file_name
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(conv, f, ensure_ascii=False, indent=2)
    for orphan in existing_files - current_files:
        (SESSIONS_DIR / orphan).unlink()


def load_conversations():
    """从sessions目录加载所有会话文件，返回会话列表"""
    conversations = []
    if SESSIONS_DIR.exists():
        for file in SESSIONS_DIR.glob("conv_*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    conv = json.load(f)
                    conversations.append(conv)
            except Exception:
                pass
    conversations.sort(key=lambda c: c["id"])
    return conversations


def delete_conversation(conv_name):
    """删除指定会话的JSON文件"""
    file_path = SESSIONS_DIR / f"conv_{conv_name}.json"
    if file_path.exists():
        file_path.unlink()







#第五部分：主程序（Streamlit网页界面)

# 设置浏览器标签页标题
st.set_page_config(page_title="校园信息查询助手", layout="wide")

# ========= 全局异常捕获 =========
try:

    # ---------- 电话黄页全屏状态 ----------
    if "show_yellow_pages" not in st.session_state:
        st.session_state.show_yellow_pages = False

    # ========== 电话黄页全屏页面 ==========
    if st.session_state.show_yellow_pages:
        close_col, title_col, _ = st.columns([1, 4, 1])
        with close_col:
            if st.button("✖ 关闭", key="close_yellow_pages", use_container_width=True):
                st.session_state.show_yellow_pages = False
                st.rerun()
        with title_col:
            st.title("📞 校园电话黄页")
        st.markdown("---")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                "#### 🏛️ 行政服务\n\n"
                "| 部门 | 电话 |\n"
                "| --- | --- |\n"
                "| 校值班室 | 0371-63456789 |\n"
                "| 招生办 | 0371-63456001 |\n"
                "| 教务处 | 0371-63456002 |\n"
                "| 学生处 | 0371-63456003 |\n"
                "| 财务处 | 0371-63456004 |\n"
            )
        with col2:
            st.markdown(
                "#### 🏫 院系联系\n\n"
                "| 部门 | 电话 |\n"
                "| --- | --- |\n"
                "| 信息工程学院办公室 | 0371-63456101 |\n"
                "| 航空工程学院办公室 | 0371-63456102 |\n"
                "| 工商管理学院办公室 | 0371-63456103 |\n"
                "| 文法学院办公室 | 0371-63456104 |\n"
            )
        with col3:
            st.markdown(
                "#### 🔧 生活服务\n\n"
                "| 部门 | 电话 |\n"
                "| --- | --- |\n"
                "| 后勤报修 | 0371-63456201 |\n"
                "| 宿管中心 | 0371-63456202 |\n"
                "| 食堂管理 | 0371-63456203 |\n"
                "| 校园卡中心 | 0371-63456204 |\n"
            )

        st.markdown("---")

        col4, col5 = st.columns(2)
        with col4:
            st.markdown(
                "#### 🛡️ 安全应急\n\n"
                "| 部门 | 电话 |\n"
                "| --- | --- |\n"
                "| 保卫处 | 0371-63456301 |\n"
                "| 校医院 | 0371-63456302 |\n"
            )
        with col5:
            st.markdown(
                "#### 💚 心理关怀\n\n"
                "| 部门 | 电话 |\n"
                "| --- | --- |\n"
                "| 心理咨询中心 | 0371-63456303 |\n"
                "| 心理咨询热线 | 0371-63456304 |\n"
            )

        st.markdown("---")
        st.caption("© 2025 小航校园AI助手 | 郑州航空工业管理学院")
        st.stop()

    # ---------- 初始化会话状态（从文件加载） ----------
    if "conversations" not in st.session_state:
        loaded = load_conversations()
        if loaded:
            st.session_state.conversations = loaded
            st.session_state.conv_counter = max(c["id"] for c in loaded)
            st.session_state.current_conv_id = loaded[0]["id"]
        else:
            st.session_state.conversations = []
            st.session_state.conv_counter = 0
            st.session_state.current_conv_id = None

    if "current_conv_id" not in st.session_state:
        st.session_state.current_conv_id = None
    if "conv_counter" not in st.session_state:
        st.session_state.conv_counter = 0

    # 没有会话时自动创建一个
    if len(st.session_state.conversations) == 0:
        st.session_state.conv_counter += 1
        default_conv = {
            "id": st.session_state.conv_counter,
            "name": f"对话 {st.session_state.conv_counter}",
            "identity": "请选择身份",
            "messages": [],
        }
        st.session_state.conversations.append(default_conv)
        st.session_state.current_conv_id = st.session_state.conv_counter
        save_conversations()

    # 确保 current_conv_id 有效
    if st.session_state.current_conv_id is None or not any(
        c["id"] == st.session_state.current_conv_id for c in st.session_state.conversations
    ):
        st.session_state.current_conv_id = st.session_state.conversations[0]["id"]

    # 获取当前会话
    def get_current_conv():
        for conv in st.session_state.conversations:
            if conv["id"] == st.session_state.current_conv_id:
                return conv
        return st.session_state.conversations[0]

    # ========== 左侧边栏：会话管理 ==========
    with st.sidebar:
        st.markdown("### 💬 会话管理")

        # 新建会话按钮
        if st.button("➕ 新建会话", use_container_width=True):
            st.session_state.conv_counter += 1
            new_id = st.session_state.conv_counter
            new_conv = {
                "id": new_id,
                "name": f"对话 {new_id}",
                "identity": "请选择身份",
                "messages": [],
            }
            st.session_state.conversations.append(new_conv)
            st.session_state.current_conv_id = new_id
            save_conversations()
            st.rerun()

        st.markdown("---")
        st.markdown("##### 历史会话")

        for conv in st.session_state.conversations:
            is_active = conv["id"] == st.session_state.current_conv_id
            btn_type = "primary" if is_active else "secondary"
            col_btn, col_rename, col_del = st.columns([4, 1, 1])
            with col_btn:
                if st.button(
                    f"💬 {conv['name']}",
                    key=f"conv_{conv['id']}",
                    use_container_width=True,
                    type=btn_type,
                ):
                    if st.session_state.current_conv_id != conv["id"]:
                        st.session_state.current_conv_id = conv["id"]
                        st.rerun()
            with col_rename:
                if st.button(
                    "✏️",
                    key=f"rename_btn_{conv['id']}",
                    help="重命名此会话",
                ):
                    st.session_state[f"renaming_{conv['id']}"] = True
            with col_del:
                if st.button(
                    "🗑️",
                    key=f"del_{conv['id']}",
                    help="删除此会话",
                ):
                    delete_conversation(conv["name"])
                    st.session_state.conversations = [
                        c for c in st.session_state.conversations if c["id"] != conv["id"]
                    ]
                    if st.session_state.current_conv_id == conv["id"]:
                        if st.session_state.conversations:
                            st.session_state.current_conv_id = st.session_state.conversations[0]["id"]
                        else:
                            st.session_state.current_conv_id = None
                    save_conversations()
                    st.rerun()

            if st.session_state.get(f"renaming_{conv['id']}", False):
                new_name = st.text_input(
                    "新名称",
                    key=f"rename_input_{conv['id']}",
                    placeholder="请输入新的会话名称",
                )
                confirm_col, cancel_col = st.columns(2)
                with confirm_col:
                    if st.button("✅确认", key=f"confirm_rename_{conv['id']}", use_container_width=True):
                        if not new_name:
                            st.warning("名称不能为空")
                        elif new_name == conv["name"]:
                            st.warning("新名称与原名相同")
                        elif any(c["name"] == new_name for c in st.session_state.conversations if c["id"] != conv["id"]):
                            st.warning("该名称已存在，请重新输入")
                        else:
                            conv["name"] = new_name
                            st.session_state.pop(f"renaming_{conv['id']}", None)
                            save_conversations()
                            st.rerun()
                with cancel_col:
                    if st.button("❌取消", key=f"cancel_rename_{conv['id']}", use_container_width=True):
                        st.session_state.pop(f"renaming_{conv['id']}", None)
                        st.rerun()

        # ---------- 电话黄页入口按钮 ----------
        st.markdown("---")
        if st.button("📞 校园电话黄页", use_container_width=True):
            st.session_state.show_yellow_pages = True
            st.rerun()

    # ========== 右侧主区域 ==========
    current_conv = get_current_conv()

    # 页面标题
    st.title("🎓 小航 - 校园信息AI助手")
    st.caption("郑州航空工业管理学院 | 基于硅基流动大模型")

    # ---------- 身份选择 ----------
    identity_options = ["请选择身份", "新生", "在校生", "教师"]
    saved_identity = current_conv.get("identity", "请选择身份")
    default_index = identity_options.index(saved_identity) if saved_identity in identity_options else 0

    identity = st.selectbox(
        "请选择你的身份：",
        identity_options,
        index=default_index,
        key=f"identity_{current_conv['id']}",
    )

    # 未选择身份时，提示用户选择，不显示后续内容
    if identity == "请选择身份":
        st.info("👆 请先选择你的身份，再开始提问")
    else:
        if current_conv.get("identity") != identity:
            current_conv["identity"] = identity
            save_conversations()

        # ========== ① 身份动态分类切换逻辑 ==========
        identity_categories = {
            "新生": ["🎒 新生入学", "🏫 校园生活", "🚌 校园交通"],
            "在校生": ["🏫 校园生活", "🚌 校园交通"],
        }

        def handle_question(question):
            """保存问题到待处理状态，触发rerun"""
            st.session_state[f"pending_q_{current_conv['id']}"] = question
            st.rerun()

        if identity in identity_categories:
            categories = identity_categories[identity]
            state_key = f"selected_category_{current_conv['id']}"
            if state_key not in st.session_state:
                st.session_state[state_key] = categories[0]

            category_cols = st.columns(len(categories))
            for i, cat in enumerate(categories):
                is_active = st.session_state[state_key] == cat
                if category_cols[i].button(
                    cat,
                    key=f"cat_{current_conv['id']}_{i}",
                    type="primary" if is_active else "secondary",
                ):
                    st.session_state[state_key] = cat
                    st.rerun()

            category_questions = {
                "🎒 新生入学": [
                    "新生报到需要带哪些材料？",
                    "学费和住宿费分别是多少？",
                    "宿舍是怎么分配的？",
                    "入学后如何防止被骗？",
                ],
                "🏫 校园生活": [
                    "图书馆的开放时间是什么？",
                    "如何开具在读证明？",
                    "校园卡丢了怎么补办？",
                    "食堂有哪些？饭菜价格如何？",
                ],
                "🚌 校园交通": [
                    "312路公交车路线和站点有哪些？",
                    "48路公交车经过学校哪些站？",
                    "S177路微公交怎么坐？",
                    "Y31路夜班车运营时间是怎样的？",
                ],
            }

            st.markdown("---")
            current_category = st.session_state[state_key]
            questions = category_questions.get(current_category, [])
            cols = st.columns(len(questions))
            for i, q in enumerate(questions):
                if cols[i].button(q, key=f"q_{current_conv['id']}_{i}"):
                    handle_question(q)
        else:
            question_buttons = {
                "教师": [
                    "各院系办公室联系电话是多少？",
                    "教务处和财务处的联系方式？",
                    "遇到紧急情况如何处理？",
                    "心理咨询中心在哪里？如何预约？",
                ],
            }
            st.markdown("##### 💡 推荐提问（点击直接发送）")
            cols = st.columns(4)
            for i, btn_text in enumerate(question_buttons[identity]):
                if cols[i].button(btn_text, key=f"btn_{current_conv['id']}_{i}"):
                    handle_question(btn_text)

        # ---------- 对话展示区 ----------
        st.markdown("---")
        for msg in current_conv["messages"]:
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("assistant"):
                    st.markdown(msg["content"])

        # ---------- 流式输出（在历史消息之后渲染） ----------
        pending_key = f"pending_q_{current_conv['id']}"
        if pending_key in st.session_state:
            pending_q = st.session_state.pop(pending_key)
            current_conv["messages"].append({"role": "user", "content": pending_q})
            md_files = list(DATA_DIR.glob("[0-9]*.md"))
            if not md_files:
                answer = "⚠️ 未找到校园资料文件，请确认资料存在。"
            else:
                campus_docs = load_all_docs()
                system_prompt = build_system_prompt(identity, campus_docs)
                with st.chat_message("assistant"):
                    placeholder = st.empty()
                    with st.spinner("AI正在整理校园相关答案，请稍候..."):
                        answer = chat_with_ai_stream(pending_q, system_prompt, placeholder)
            current_conv["messages"].append({"role": "assistant", "content": answer})
            save_conversations()
            st.rerun()

        # ---------- 输入框（按Enter直接发送，发送后自动清空） ----------
        user_input = st.chat_input("请输入你的问题，按Enter发送...", key=f"chat_{current_conv['id']}")
        if user_input and user_input.strip():
            handle_question(user_input)

    # ---------- 底部版权信息 ----------
    st.markdown("---")
    st.caption("© 2025 小航校园AI助手 | 郑州航空工业管理学院")

except Exception as e:
    st.error(f"⚠️ 程序运行出现异常：{e}")
    st.info("请检查配置或联系管理员。")



#知识库边界（或信息边界）
# AI的回答范围被限制在提供的4份md文档内
# 超出文档内容的问题一律拒绝回答
# 由防幻觉规则第4条强制执行


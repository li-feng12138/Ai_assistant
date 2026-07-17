import requests
import json

API_BASE_URL = "https://api.siliconflow.cn/v1/chat/completions"

MODEL_NAME = "deepseek-ai/DeepSeek-V3"

API_KEY = "sk-nawrukkmeoumzuhtykoxtxpfwenoztejothuugcrkylhovqv"


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

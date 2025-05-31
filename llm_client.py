from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")

class LLMClient:
    def __init__(self, api_key=API_KEY, base_url=API_BASE_URL):
        """初始化LLM客户端"""
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
    def chat(self, messages, model="deepseek-ai/DeepSeek-R1", stream=True):
        """与LLM交互，支持流式与非流式

        Args:
            messages: 消息列表
            model: 使用的LLM模型
            stream: 是否启用流式传输

        Returns:
            tuple: (content, reasoning_content)
        """
        try:
            print(f"LLM请求: {messages}")

            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=stream,
            )

            content = ""
            reasoning_content = ""

            if stream:
                for chunk in response:
                    delta = chunk.choices[0].delta
                    if hasattr(delta, "content") and delta.content:
                        content += delta.content
                    if hasattr(delta, "reasoning_content") and delta.reasoning_content:
                        reasoning_content += delta.reasoning_content
            else:
                if response.choices:
                    message = response.choices[0].message
                    content = message.content or ""
                    reasoning_content = getattr(message, "reasoning_content", "") or ""

            print(f"LLM推理内容: {content}")
            return content, reasoning_content

        except Exception as e:
            print(f"LLM调用出错: {str(e)}")
            return "", ""


# 使用示例
if __name__ == "__main__":
    llm = LLMClient()
    messages = [
        {"role": "user", "content": "你好"}
    ]
    response = llm.chat(messages)
    print(f"响应: {response}")
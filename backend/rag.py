# backend/rag.py
from backend.llm import get_llm_response

def ask(user_question: str) -> str:
    """
    这是留给前端的接口。
    
    """
    
    # 1. 【临时逻辑】：因为今晚还没做向量数据库，我们直接把问题包装一下
    # 等明天做完 vector_store.py，我们再把真实的知识库检索塞进这里
    rag_prompt = f"""你是一个数据结构智能助教。
请回答用户的【问题】：{user_question}
"""
    
    # 2. 调用你昨天测通的智谱大模型
    final_answer = get_llm_response(rag_prompt)
    return final_answer
from backend.llm import get_llm_response
try:
    from main import search_knowledge
except Exception:
    search_knowledge = None

from backend.vector_store import search_relevant_docs  # 🌟 导入你刚写好的检索函数

def ask(user_question: str) -> str:
    """
    最终留给前端 app.py 调用的核心接口
    """
    # 1. 真正的 RAG 第一步：去知识库里找相关的参考资料
    if search_knowledge:
        docs = search_knowledge(user_question, top_k=3)
        # incoming branch returned doc objects; join their page_content if present
        context = "\n\n".join([getattr(doc, "page_content", str(doc)) for doc in docs])
    else:
        context = search_relevant_docs(user_question, k=3)
    
    # 2. 真正的 RAG 第二步：把检索到的知识，作为背景补充给大模型
    rag_prompt = f"""你是一个专业的数据结构智能助教。请严格根据以下给出的【已知知识库信息】来回答用户的【问题】。
如果已知信息里无法回答该问题，请礼貌地回答你不知道，不要瞎编。

【已知知识库信息】：
{context}

【用户的实际问题】：
{user_question}
"""
    
    # 3. 真正的 RAG 第三步：把拼好的大 Prompt 扔给大模型，拿到结合了本地知识库的完美答案
    final_answer = get_llm_response(rag_prompt)
    return final_answer


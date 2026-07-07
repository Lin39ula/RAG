from backend.llm import get_llm_response
from main import search_knowledge

def ask(prompt):
    docs = search_knowledge(prompt, top_k=3)
    context = "\n\n".join([doc.page_content for doc in docs])
    full_prompt = f"""
    # 回答规则
1. 严格依据下面的知识库内容回答，禁止编造不存在的信息；
2. 涉及算法时间/空间复杂度等数学表达式时，必须使用标准Markdown公式格式：
   - 平方写成 $O(n^2)$，绝对不能简写为n2；
   - 对数写成 $O(n\\log_2 n)$，不能简写log2n；
   - 所有复杂度公式前后用$符号包裹；
3. 术语不能混淆：区分「最好情况」「平均情况」「最坏情况」，不要写错文字；
参考知识库内容：
{context}
用户问题：{prompt}
请严格依据知识库内容回答，不要编造信息。
"""
    return get_llm_response(full_prompt)
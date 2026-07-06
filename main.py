from src.parser import read_all_pdfs
from src.splitter import split_text
from langchain_chroma import Chroma
from langchain_core.documents import Document
from zhipuai import ZhipuAI
import os

# 智谱API密钥
API_KEY = "89a521a0d72643e7ba274c4a3fbff0a9.Ks2NbDIs8i6bxnlW"
client = ZhipuAI(api_key=API_KEY)

# 智谱向量嵌入类
class ZhipuEmb:
    def embed_documents(self, texts):
        vecs = []
        for txt in texts:
            resp = client.embeddings.create(model="embedding-2", input=txt)
            vecs.append(resp.data[0].embedding)
        return vecs

    def embed_query(self, text):
        return self.embed_documents([text])[0]

emb = ZhipuEmb()
PERSIST_DIR = "./chroma_db"

if __name__ == "__main__":
    # 检测已有向量库，直接加载，不再重新向量化
    if os.path.exists(PERSIST_DIR):
        print("✅ 检测到已有向量知识库，直接加载本地文件，无需重新向量化！")
        vector_db = Chroma(persist_directory=PERSIST_DIR, embedding_function=emb)
    else:
        print("开始读取全部PDF文档...")
        raw_docs = read_all_pdfs("data")
        print(f"一共读取原始页面: {len(raw_docs)} 页")

        chunks = split_text(raw_docs)
        print(f"分块完成，总chunk数量: {len(chunks)}")

        print("\n开始向量化构建知识库，请等待...")
        langchain_docs = []
        for chunk in chunks:
            doc = Document(
                page_content=chunk["text"],
                metadata={
                    "source_file": chunk["source_file"],
                    "page_num": chunk["page_num"]
                }
            )
            langchain_docs.append(doc)

        vector_db = Chroma.from_documents(
            documents=langchain_docs,
            embedding=emb,
            persist_directory=PERSIST_DIR
        )
        print("✅ 向量知识库构建完成！")

    # ========== 自定义检索测试，修改这里的query就能查不同问题 ==========
    print("\n===== 知识库检索测试 =====")
    query = "栈和队列有什么区别"

    relate_docs = vector_db.similarity_search(query, k=3)
    print(f"\n查询问题：{query}")

    for idx, doc in enumerate(relate_docs):
        print(f"\n【匹配内容{idx+1}】")
        print(doc.page_content)
        print(f"出处：{doc.metadata['source_file']} 第{doc.metadata['page_num']}页\n")

    # 给后端使用的检索函数
    def search_knowledge(query_str, top_k=5):
        return vector_db.similarity_search(query_str, k=top_k)
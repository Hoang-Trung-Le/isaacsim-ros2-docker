from langchain_community.vectorstores.faiss import FAISS
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from lc_agent import get_retriever_registry
import os


def _get_nvidia_embedder(api_key: str = None, func_id: str = None):
    embedding = NVIDIAEmbeddings(model="nvidia/nv-embedqa-e5-v5", truncate="END", nvidia_api_key=api_key)

    if not func_id:
        func_id = os.environ.get("NVIDIA_EMBEDDING_FUNC_ID", None)

    if func_id:
        base_url = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/{func_id}"
        base_url = base_url.replace("{func_id}", func_id)
        embedding._client.infer_path = base_url

    return embedding


def register_faiss_retriever(name, vectordb_index_name: str, top_k: int = 3, api_key: str = None, func_id: str = None):
    embedder = _get_nvidia_embedder(api_key=api_key, func_id=func_id)
    if not embedder:
        return

    vectordb = FAISS.load_local(vectordb_index_name, embedder, allow_dangerous_deserialization=True)

    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": top_k})

    get_retriever_registry().register(name, retriever)


def register_all(top_k: int = 3, api_key: str = None, func_id: str = None):

    # Code retriever
    faiss_index_code_embedqa = "../data/faiss_index_embedqa_3346"
    faiss_index_code_embedqa = os.path.abspath(f"{__file__}/{faiss_index_code_embedqa}")
    register_faiss_retriever("embedqa", faiss_index_code_embedqa, top_k, api_key, func_id)

    # Metafunction retriever
    faiss_usd_metafunctions = "../data/faiss_usd_metafunctions_01"
    faiss_usd_metafunctions = os.path.abspath(f"{__file__}/{faiss_usd_metafunctions}")
    register_faiss_retriever("usd_metafunctions", faiss_usd_metafunctions, top_k, api_key, func_id)

    # Knowledge retriever
    faiss_index_usd_knowledge_qa = "../data/faiss_index_ai-embed-qa-4_ousd_sdgqa"
    faiss_index_usd_knowledge_qa = os.path.abspath(f"{__file__}/{faiss_index_usd_knowledge_qa}")
    register_faiss_retriever("usd_knowledge_qa", faiss_index_usd_knowledge_qa, top_k, api_key, func_id)

    # Code 06262024 retriever
    faiss_index_usd_code06262024 = "../data/faiss_index_ai-embed-qa-4_code06262024"
    faiss_index_usd_code06262024 = os.path.abspath(f"{__file__}/{faiss_index_usd_code06262024}")
    register_faiss_retriever("usd_code06262024", faiss_index_usd_code06262024, top_k, api_key, func_id)


def unregister_all():
    get_retriever_registry().unregister("embedqa")
    get_retriever_registry().unregister("usd_metafunctions")
    get_retriever_registry().unregister("usd_knowledge_qa")
    get_retriever_registry().unregister("usd_code06262024")

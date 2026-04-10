import os
import requests
from typing import Optional, Dict

def _build_prompt(question: str, context: Optional[str]) -> str:
    if context:
        return f"You are a helpful travel assistant specialized in monuments.\nContext:\n{context}\n\nQuestion: {question}\nAnswer concisely."
    return f"You are a helpful travel assistant specialized in monuments.\nQuestion: {question}\nAnswer concisely."

def ask_hf(question: str, context: Optional[str] = None, model: Optional[str] = None, timeout: int = 20) -> Dict[str, str]:
    token = os.environ.get("HUGGINGFACE_API_TOKEN")
    if not token:
        return {"success": False, "error": "Missing HUGGINGFACE_API_TOKEN"}
    m = model or os.environ.get("HF_MODEL", "mistralai/Mistral-7B-Instruct")
    url = f"https://api-inference.huggingface.co/models/{m}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    payload = {
        "inputs": _build_prompt(question, context),
        "parameters": {"max_new_tokens": 256, "temperature": 0.7, "return_full_text": False},
        "options": {"wait_for_model": True, "use_cache": True}
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=timeout)
        if r.status_code == 200:
            data = r.json()
            # Common Inference API formats
            if isinstance(data, list) and data:
                item = data[0]
                if isinstance(item, dict):
                    txt = item.get("generated_text") or item.get("summary_text") or item.get("answer")
                    if isinstance(txt, str) and txt.strip():
                        return {"success": True, "text": txt.strip()}
            if isinstance(data, dict):
                txt = data.get("generated_text") or data.get("summary_text") or data.get("answer")
                if isinstance(txt, str) and txt.strip():
                    return {"success": True, "text": txt.strip()}
            return {"success": False, "error": "Unexpected response format"}
        return {"success": False, "error": f"HTTP {r.status_code}: {r.text[:200]}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def ask_ollama(question: str, context: Optional[str] = None, model: Optional[str] = None, timeout: int = 15) -> Dict[str, str]:
    m = model or os.environ.get("OLLAMA_MODEL", "llama3")
    url = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
    payload = {"model": m, "prompt": _build_prompt(question, context), "stream": False}
    try:
        r = requests.post(url, json=payload, timeout=timeout)
        if r.status_code == 200:
            data = r.json()
            text = data.get("response", "").strip()
            if text:
                return {"success": True, "text": text}
            return {"success": False, "error": "Empty response"}
        return {"success": False, "error": f"HTTP {r.status_code}: {r.text[:200]}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

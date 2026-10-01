## 4.1 Dual-Language Multi-Process Topology

Confronted with the context-window limitations and rate-limiting constraints of large language models during code analysis, this case study outlines the development of a dual-language Model Context Protocol (MCP) bridge. The topology separates the intelligent reasoning layer from the deterministic routing layer.

1. **Python FastMCP (The Brain):** The Python layer is responsible for interfacing with the LLM. It manages the conversational memory, token limits, and rate-limiting logic. 
2. **Javalin API (The Router):** The Java backend acts as a high-speed router. It intercepts commands from the Python layer and directly interfaces with the underlying JADX decompiler API, completely bypassing the graphical user interface.

[FIGURE] dummy_arch.png
[FIGURE_CAPTION] Figure 1: System Architecture Diagram for JADX-AI-MCP

## 4.2 Rate Limiting Algorithms & Token Economics

Applying LLMs to large Android codebases via Free Tier APIs necessitates extremely strict token economics. A naive approach of feeding an entire decompiled application to an LLM will instantly trigger a `429 Too Many Requests` error.

To mitigate this, a sliding-window rate limiter was engineered in `tracing.py`. This subsystem utilizes the `tiktoken` library to pre-calculate the token weight of every prompt. If the prompt exceeds the maximum allowable threshold (e.g., capping execution at 14 Requests Per Minute), the system actively delays execution or summarizes the payload.

```python
import tiktoken
import time

def check_rate_limit(prompt_text, max_rpm=14):
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = len(enc.encode(prompt_text))
    # sliding window logic here
    if requests_in_last_minute > max_rpm:
        time.sleep(60)
    return True
```

## 4.3 Vectorless SQLite FTS5 Indexing Subsystem

Traditional RAG (Retrieval-Augmented Generation) pipelines rely on heavy vector databases like Pinecone or Milvus. For a standalone, offline digital forensics tool, this dependency is unacceptable. 

Instead, the `index_builder.py` module utilizes standard SQLite bundled with the **FTS5** (Full-Text Search) extension. This allows the MCP engine to perform lightning-fast, keyword-based searches across massive Android codebases (such as locating every instance of `android_id` or `FirebaseDatabase`) without requiring external internet connectivity or expensive vector embeddings.

## 4.4 Cross-Session State Persistence

Forensic investigations often span multiple days. To ensure the LLM does not lose its analytical context between restarts, the `notes_store.py` module was engineered. This acts as a persistent Checkpoint Engine, writing the AI's current deductions, derived XOR keys, and identified C2 endpoints to a structured local JSON ledger. Upon booting, the system injects this ledger back into the LLM's system prompt, enabling seamless cross-session state persistence.

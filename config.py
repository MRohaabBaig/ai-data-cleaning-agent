import os
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

class LLMProvider:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "ollama").lower()
        self.llm = self._get_llm()

    def _get_llm(self):
        if self.provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables.")
            return ChatOpenAI(model="gpt-4o", api_key=api_key)
        elif self.provider == "ollama":
            # Defaulting to llama3, but this can be configured
            model_name = os.getenv("OLLAMA_MODEL", "llama3")
            return ChatOllama(model=model_name, base_url="http://localhost:11434")
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def get_llm(self):
        return self.llm

llm_provider = LLMProvider()
llm = llm_provider.get_llm()

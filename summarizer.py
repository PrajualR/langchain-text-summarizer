# summarizer.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


class TextSummarizer:
    def __init__(self):
        api_key = os.getenv("API_KEY")
        model_name = os.getenv("MODEL_NAME")
        base_url = os.getenv("BASE_URL")

        if not api_key or not model_name:
            raise ValueError("Missing API configuration")

        self.llm = ChatOpenAI(
            model=model_name,
            api_key=api_key,
            base_url=base_url,
            temperature=0.3,
        )

        # Conservative chunking (character-based but safe)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=200
        )

        self.summary_prompt = PromptTemplate(
            input_variables=["text"],
            template="""
You are an expert summarizer.

Summarize the following text clearly and concisely.
Focus on key ideas, decisions, and facts.

Text:
{text}

Summary:
"""
        )

        self.bullet_prompt = PromptTemplate(
            input_variables=["text"],
            template="""
You are an expert summarizer.

Summarize the following text into clear bullet points.
Rules:
- No repetition
- Each bullet under 20 words
- Focus on key facts

Text:
{text}

Bullet-point summary:
"""
        )

        self.parser = StrOutputParser()

    def _map_reduce(self, chunks, prompt):
        """Explicit map-reduce summarization"""

        map_chain = prompt | self.llm | self.parser

        partial_summaries = [
            map_chain.invoke({"text": chunk}) for chunk in chunks
        ]

        reduce_prompt = PromptTemplate(
            input_variables=["summaries"],
            template="""
Combine the following partial summaries into one concise final summary.

Partial summaries:
{summaries}

Final summary:
"""
        )

        reduce_chain = reduce_prompt | self.llm | self.parser

        return reduce_chain.invoke(
            {"summaries": "\n".join(partial_summaries)}
        )

    def summarize_text(self, text: str) -> str:
        if not text.strip():
            raise ValueError("Empty text")

        # Safe threshold (~400 tokens)
        if len(text) <= 1500:
            chain = self.summary_prompt | self.llm | self.parser
            return chain.invoke({"text": text})

        chunks = self.text_splitter.split_text(text)
        return self._map_reduce(chunks, self.summary_prompt)

    def summarize_with_bullets(self, text: str) -> str:
        if not text.strip():
            raise ValueError("Empty text")

        if len(text) <= 1500:
            chain = self.bullet_prompt | self.llm | self.parser
            return chain.invoke({"text": text})

        chunks = self.text_splitter.split_text(text)
        return self._map_reduce(chunks, self.bullet_prompt)

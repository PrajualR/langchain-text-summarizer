import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document

load_dotenv()

class TextSummarizer:
    def __init__(self):
        api_key = os.getenv('API_KEY')
        model_name = os.getenv('MODEL_NAME')
        base_url = os.getenv('BASE_URL')
        if not api_key:
            raise ValueError("API key not found")

        self.llm = ChatOpenAI(model_name=model_name, temperature =0.3, api_key = api_key, base_url=base_url)

        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)

    def summarize_text(self, text, summary_type='stuff'):
        try:
            docs = [Document(page_content=text)]

            if len(text)> 3000:
                docs = self.text_splitter.split_documents(docs)
                summary_type = "map reduce"

            chain = load_summarize_chain(self.llm, chain_type=summary_type, verbose=False)
            summary = chain.invoke({"input_documents": docs})

            return summary["output_text"]

        except Exception as e:
            return f"Error generating summary: {str(e)}"

    def summarize_with_bullets(self, text, custom_prompt=None):
        try:
            if custom_prompt is None:
                custom_prompt = """
                Create a bullet-point summary of the following text. 
                Extract the most important points and list them clearly:
        
                {text}
        
                Bullet-point Summary:
                """
            formatted_prompt = custom_prompt.format(text=text)
            summary = self.llm.invoke([HumanMessage(content=formatted_prompt)]).content

            return summary.strip()
        except Exception as e:
            return f"Error generating summary: {str(e)}"

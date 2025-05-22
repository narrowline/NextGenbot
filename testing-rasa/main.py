# from langchain.llms.fake import FakeListLLM
# from langchain.chains import LLMChain
# from langchain.prompts import PromptTemplate

# # Step 1: Fake LLM setup
# fake_llm = FakeListLLM(responses=["Yes! This stylish suit is available in Medium."])

# # Step 2: Prompt setup
# prompt = PromptTemplate.from_template("{question}")

# # Step 3: Chain setup
# chain = LLMChain(llm=fake_llm, prompt=prompt)

# # Step 4: Running the chain
# print(chain.run({"question": "Do you have blue color?"}))
# from langchain_community.llms import HuggingFacePipeline
# from transformers import pipeline
# from langchain.prompts import PromptTemplate

# # Step 1: HuggingFace Model Load karo
# hf_pipeline = pipeline(
#     "text2text-generation", 
#     model="google/flan-t5-small", 
#     max_length=256
# )

# # Step 2: LangChain LLM bana lo HuggingFacePipeline ke through
# llm = HuggingFacePipeline(pipeline=hf_pipeline)

# # Step 3: Prompt Template
# prompt = PromptTemplate.from_template("{question}")

# # Step 4: Chain banani
# chain = prompt | llm

# # Step 5: Chain se sawal poochho
# response = chain.invoke({"question": "World famous cricketer name?"})

# print(response)

# import requests

# # Your API Key here
# API_KEY = "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"

# # Message jo model ko bhejna hai
# user_message = "Hello, What's up?"

# # API endpoint
# url = "https://openrouter.ai/api/v1/chat/completions"

# # Request ka body
# payload = {
#     "model": "tngtech/deepseek-r1t-chimera:free",  # Yahan model ka naam dalna
#     "messages": [
#         {"role": "user", "content": user_message}
#     ],
#     "temperature": 0.7  # Creativity level (0 = boring, 1 = very creative)
# }

# # Headers
# headers = {
#     "Authorization": f"Bearer {API_KEY}",
#     "Content-Type": "application/json"
# }

# # Request bhejna
# response = requests.post(url, headers=headers, json=payload)

# # Response ko parse karna
# if response.status_code == 200:
#     result = response.json()
#     print("Model Response:", result['choices'][0]['message']['content'])
# else:
#     print("Error:", response.status_code, response.text)

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os

# Step 1: Set API Key
os.environ["OPENAI_API_KEY"] = "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"

# Step 2: OpenRouter ka Base URL
openrouter_base_url = "https://openrouter.ai/api/v1"

# Step 3: LLM Setup
llm = ChatOpenAI(
    openai_api_base=openrouter_base_url, 
    openai_api_key=os.environ["OPENAI_API_KEY"],
    model="tngtech/deepseek-r1t-chimera:free",  # ✅ Tumhara FREE model yahan
    temperature=0.7,
)

# Step 4: Prompt Template
prompt = ChatPromptTemplate.from_template("Answer me  in romanized Urdu: {input}")

# Step 5: Chain
chain = prompt | llm

# Step 6: Invoke the Chain
response = chain.invoke({"input": "Tumhe kis date tak kai data ki training di gayi hai?"})

print(response.content)


import re
from llama_index import SimpleDirectoryReader,GPTListIndex,GPTVectorStoreIndex,LLMPredictor,PromptHelper,ServiceContext,StorageContext,load_index_from_storage
from langchain.chat_models import ChatOpenAI
import gradio as gr
import sys
import os
from llama_index.node_parser import SimpleNodeParser
from llama_index.storage.docstore.simple_docstore import SimpleDocumentStore

os.environ["OPENAI_API_KEY"] = "add your key"
openai_key = "add your key"
dir_path = os.path.abspath(os.path.dirname(__file__))
docs_path = os.path.join(dir_path, "docs")



def construct_index(directory_path):
    chatModel = ChatOpenAI(streaming=True, openai_api_key=openai_key, temperature=0.3, model_name="gpt-3.5-turbo")

    llm_predictor = LLMPredictor(llm=chatModel)


    # define prompt helper
    # set maximum input size
    max_input_size = 4096
    # set number of output tokens
    num_output = 2000
    # set maximum chunk overlap
    chunk_overlap_ratio= 0.1
    prompt_helper = PromptHelper(max_input_size, num_output, chunk_overlap_ratio)

    documents = SimpleDirectoryReader(directory_path).load_data()
    #create vector index 
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
    index= GPTVectorStoreIndex.from_documents(documents=documents, service_context=service_context)
    index.storage_context.persist(persist_dir = 'content')
    return index



def chatbot(input_text):
    storage_context = StorageContext.from_defaults(persist_dir='content')
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    response = query_engine.query(input_text)
    return response


iface = gr.Interface(fn=chatbot,
                     inputs=gr.components.Textbox(lines=7, label="Enter your text"),
                     outputs="text",
                     title="HINDISGHT expense management chatbot")

index = construct_index("/Users/andreslopez/Desktop/chat-bot/docs")
response = chatbot("Hello I am here to help you")
print(response)
iface.launch(share=True)


  
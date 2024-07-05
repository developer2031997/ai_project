from uuid import UUID
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler
import warnings
from queue import Queue
from threading import Thread

load_dotenv()
warnings.filterwarnings("ignore", category=DeprecationWarning)

queue = Queue()

class StraminggHandler(BaseCallbackHandler):
    def on_llm_new_token(self,token, **kwargs):
        queue.put(token)

    def on_llm_end(self,response,**kwargs):
         queue.put(None)

    def on_llm_error(self,response,**kwargs):
         queue.put(None)

        # Initialize ChatOpenAI with streaming enabled
chat = ChatOpenAI(
    streaming=True,
     callbacks=[StraminggHandler()])

# Define a prompt template for human messages
prompt = ChatPromptTemplate(
    input_variables=["content"],
    messages=[HumanMessagePromptTemplate.from_template("{content}")]
)

class StreamableChain(LLMChain):
    def stream (self, input):
        queue = Queue()
        handler = StraminggHandler(queue)

        def task():
             self(input, callbacks=[handler])

        Thread(target=task).start()


        self(input)
        while True:
            token = queue.get()
            yield token
    

# Create an LLMChain with the configured ChatOpenAI and prompt
chain = LLMChain(llm=chat, prompt=prompt)

# Continuously prompt for input and stream responses
# while True:
    # content = input(">>> ")
generator = chain.stream({"content": "tell me a sortest joke"})  # Get the generator

  # Iterate over the generator to print each response
for result in generator:
        print("\n")
        print(result['text'])
        pass

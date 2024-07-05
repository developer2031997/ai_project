from langchain.callbacks.base import BaseCallbackHandler
from queue import Queue
queue = Queue()

class StraminggHandler(BaseCallbackHandler):
    def __init__(self,queue):
         self.queue = queue
         self.streaming_run_ids=set()

    def on_chat_model_start(self,serialized,message,run_id,**kwargs):
         print(serialized)
         print(run_id)
         self.streaming_run_ids.add(run_id)
    
    def on_llm_new_token(self,token, **kwargs):
        queue.put(token)

    def on_llm_end(self,response,run_id,**kwargs):
         if run_id in self.streaming_run_ids:
               queue.put(None)
               self.streaming_run_ids.remove(run_id)

    def on_llm_error(self,response,**kwargs):
         queue.put(None)
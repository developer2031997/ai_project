from flask import current_app, Flask, request, jsonify, render_template
from queue import Queue
from threading import Thread
from app.chat.callbacks.StraminggHandler import StraminggHandler

class StreamableChain:
    def __init__(self, chain, combine_docs_chain=None, retriever=None):
            self.chain = chain
            self.combine_docs_chain = combine_docs_chain
            self.retriever = retriever

    def stream(self, input):
        queue = Queue()
        handler = StraminggHandler(queue)

        def task(app_context):
            with app_context:
                self.chain(input, callbacks=[handler])

        app_context = current_app.app_context()
        thread = Thread(target=task, args=(app_context,))
        thread.start()

        while True:
            token = queue.get()
            yield token

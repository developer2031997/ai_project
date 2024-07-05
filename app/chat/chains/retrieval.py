from langchain.chains import ConversationalRetrievalChain
from app.chat.chains.StreamableChain import StreamableChain

class StreamingConversationalRetrivalChain(
StreamableChain,ConversationalRetrievalChain
):
    pass

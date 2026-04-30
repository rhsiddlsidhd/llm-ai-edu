# multiturn + history
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.chat_history import InMemoryChatMessageHistory # 메모리 내에서 메시지를 리스트 형태로 보관
from langchain_core.runnables.history import RunnableWithMessageHistory # 모델을 생성할 때 대화 기록을 함께 전달할 수 있도록 하는 클래스


llm = ChatOpenAI(model="gpt-4o")

store = {}
config = {
    "configurable":{
        "session_id":"abc2"
    }
}

def get_session_history(session_id:str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

with_message_history = RunnableWithMessageHistory(
    llm,
    get_session_history
)
    
    
def chat(session_id, message):
    res = with_message_history.invoke(
        [HumanMessage(content=message)],
        config={"configurable": {"session_id": session_id}}
    )
    print(f"[{session_id}] AI: {res.content}\n")

# abc2에서 이름 알려주기
chat("abc2", "내 이름은 철수야")

# abc3으로 전환
chat("abc3", "안녕, 나 누구야?")

# 다시 abc2로 돌아오기
chat("abc2", "내 이름이 뭐야?")
    
    

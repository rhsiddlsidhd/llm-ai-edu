from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
from langchain_openai import ChatOpenAI
from typing import Annotated # Annotated는 타입 힌트를 사용할 때 사용하는 함수
from typing_extensions import TypedDict # TypedDict 딕셔너리 타입을 정의할 때 사용하는 함수
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver


model = ChatOpenAI(model="gpt-4o-mini",api_key=api_key)
memory = MemorySaver()
config = {"configurable":{"thread_id":"abcd"}}


class State(TypedDict) :
    """
    State 클래스는 TypeDict를 상속받습니다.
    
    속성:
        messages (Annotated[list[str],add_messages]): 메시지들은 "list" 타입을 가집니다.
        'add_messages' 함수는 이 상태 키가 어떻게 업데이트되어야 하는지를 정의합니다.
        (이 경우, 메시지를 덮어쓰는 대신 리스트에 추가합니다.)
    """ 
    messages: Annotated[list[str], add_messages]

graph_builder = StateGraph(State)

def generate(state:State):
    """
    주어진 상태를 기반으로 챗봇의 응답 메시지를 생성합니다.

    매개변수(Args):
        state (State):  현재 대화 상태를 나타내는 객체로, 이전 메시지들이 포함되어 있습니다.
    
    반환값:
        dict:   모델이 생성한 응답 메시지를 포함하는 딕셔너리.
                형식은 {"messages":[응답 메세지]}입니다.
    """
    return {"messages":[model.invoke(state["messages"])]}


graph_builder.add_node("generate",generate)
graph_builder.add_edge(START,"generate")
graph_builder.add_edge("generate",END)
graph = graph_builder.compile(checkpointer=memory)

while True:
    user_input = input("You\t:")
    if user_input in ["exit","quit","q"]:
        break
    
    for event in graph.stream({"messages":[HumanMessage(content=user_input)]},stream_mode="values",config=config):
        event["messages"][-1].pretty_print()
        
    print(f'\n현재 메시지 개수:{len(event["messages"])}\n---------------\n')
    
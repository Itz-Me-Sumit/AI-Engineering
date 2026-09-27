import streamlit as st
from langchain_core.messages import HumanMessage
from LangGraph_BackEnd import chatbot


CONFIG = {
    "configurable" : {
        "thread_id" : "thread-1"
    }
}

if "messege_history" not in st.session_state:
    st.session_state["message_history"] = []

for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input = st.chat_input("Type here")

if user_input:

    # User Input
    st.session_state["message_history"].append({
        "role" : "user",
        "content" : user_input 
    })
    with st.chat_message("user"):
        st.text(user_input)


    # AI message
    initial_state = {
        "messages" : [HumanMessage(content = user_input)]
    }
    response = chatbot.invoke(
        initial_state,
        config = CONFIG
    )
    ai_message = response["messages"][-1].content
    st.session_state["message_history"].append({
        "role" : "assistant",
        "content" : ai_message
    })
    with st.chat_message("assistent"):
        st.text(ai_message)
    


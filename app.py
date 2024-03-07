#import standard libraries
import streamlit as st
from streamlit_chat import message
import os
from langchain.llms import OpenAI
from langchain.chains import LLMChain, ConversationChain
from langchain.chains.conversation.memory import (ConversationBufferMemory,
                                                 ConversationSummaryMemory,
                                                 ConversationBufferWindowMemory)
import tiktoken
from langchain.memory import ConversationTokenBufferMemory

if "conversation" not in st.session_state:
    st.session_state["conversation"] = None

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "API_Key" not in st.session_state:
    st.session_state["API_Key"] = ""   

#UI
st.set_page_config(page_title="Chat GPT clone",
                   page_icon=":robot_face:")
st.markdown("<h1 style='text-align:center;'>How can I assist you today?</h1>",
            unsafe_allow_html=True)

st.sidebar.title("😊")

st.session_state["API_Key"] = st.sidebar.text_input("what is your api key?",type="password")
summarize_button = st.sidebar.button("summarize the conversation",key="summarize")

if summarize_button:
    summarize_placeholder = st.sidebar.write("Nice chatting with you my friend❤️:\n\n"+"Hello friend!")
    #summarize_placeholder.write("Nice chatting with you my friend ❤️:\n\n"+st.session_state['conversation'].memory.buffer)

#get the openai key
#os.environ["OPENAI_API_KEY"] = ""


def get_response(userinput,api_key):
    #instantiate llm
    if st.session_state["conversation"] is None:
        llm = OpenAI(model='gpt-3.5-turbo-instruct', 
                     openai_api_key=api_key,
                     temperature=0.7)

        #instantiate conversationMemory wrapper
        st.session_state["conversation"] = ConversationChain(llm=llm,
                                        verbose=True,
                                        memory=ConversationBufferMemory())

    response = st.session_state["conversation"].predict(input=userinput)

    return response

#container
response_container = st.container()
container = st.container()

with container:
    with st.form(key="my_form",clear_on_submit=True):
        user_input = st.text_area("Your question goes here:",key="input",height=100)
        submit_button = st.form_submit_button(label="send")

        if submit_button:
            st.session_state["messages"].append(user_input)
            model_response = get_response(userinput=user_input,api_key=st.session_state["API_Key"])
            st.session_state["messages"].append(model_response)

            with response_container:
                #st.write(model_response)

                for i in range(len(st.session_state["messages"])):
                    if (i%2) == 0:
                        message(st.session_state["messages"][i], is_user=True,key=str(i)+'_user')

                    else:
                        message(st.session_state["messages"][i], key=str(i)+'_AI')




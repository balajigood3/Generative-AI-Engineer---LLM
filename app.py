import os
import streamlit as st
from openai import OpenAIError
from llm_service import ask_llm

try:
    if not os.getenv('OPENAI_API_KEY') and 'OPENAI_API_KEY' in st.secrets:
        os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
except FileNotFoundError:
    pass

st.set_page_config(page_title='AI Chat Application', page_icon='💬')
st.title('AI Chat Application')
st.caption('LLM API portfolio project | Chat history is stored in this browser session.')

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'usage' not in st.session_state:
    st.session_state.usage = {'input_tokens': 0, 'output_tokens': 0}

with st.sidebar:
    st.header('Settings')
    instructions = st.text_area('Custom instructions', value='You are a helpful AI assistant.')
    temperature = st.slider('Temperature', 0.0, 2.0, 0.7, 0.1)
    max_tokens = st.slider('Max output tokens', 100, 2000, 500, 100)
    if st.button('New chat', use_container_width=True):
        st.session_state.messages = []
        st.session_state.usage = {'input_tokens': 0, 'output_tokens': 0}
        st.rerun()
    st.metric('Input tokens', st.session_state.usage['input_tokens'])
    st.metric('Output tokens', st.session_state.usage['output_tokens'])
    st.caption('API usage is billed separately; check your provider dashboard for actual costs.')

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

prompt = st.chat_input('Ask anything...')
if prompt:
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.chat_message('user'):
        st.markdown(prompt)
    with st.chat_message('assistant'):
        try:
            # Send only the latest messages to bound context size.
            request_messages = [{'role': 'system', 'content': instructions}] + st.session_state.messages[-20:]
            with st.spinner('Thinking...'):
                answer, usage = ask_llm(request_messages, temperature=temperature, max_tokens=max_tokens)
            st.markdown(answer)
            st.session_state.messages.append({'role': 'assistant', 'content': answer})
            for key in usage:
                st.session_state.usage[key] += usage[key]
        except (OpenAIError, ValueError) as exc:
            st.error(f'Unable to generate a response: {type(exc).__name__}. Check your API key, account balance, model access, and network.')
            st.session_state.messages.pop()

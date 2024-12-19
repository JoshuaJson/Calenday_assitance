from AI_Agent import main_agent
from swarm import Swarm
import streamlit as st

if __name__ =='_main_':
    swarm_client=Swarm()
    agent = main_agent
    
    st.title('Create A Google Calendar AI Agent')
    
    if 'messages' not in st.session_state:
        st.session_state.messages= []
        
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])
    
    if prompt := st.chat_input('Enter your prompt here'):
        st.session_state.messages.append({'role':'user', 'content':prompt})
        
        with st.chat_message('user', avatar='user'):
            st.markdown(prompt)
            
        with st.chat_message('ai', avatar='AI_calendar_man'):
            print('session state messege', st.session_state.messages)
            response = swarm_client.run(
                agent=agent,
                debug=False,
                #messages=[{'role': 'user', 'content':prompt}],
                messages=st.session_state.messages
            )
            st.markdown(response.messages[-1]['content'])
        st.session_state.messages.append({'role':'assistant', 'content':response.messages[-1]['content']})
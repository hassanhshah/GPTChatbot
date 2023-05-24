# Dependancies
import openai
import streamlit as st
from streamlit_chat import message

# Set the OpenAI API key
openai.api_key = # insert key

# Start and Restart sequences
start_sequence = "\nUser: "
restart_sequence = "\nAgentAI: "

# Prompt for initializing GPT model
prompt = # INSERT PROMPT

# Storing session states
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

if 'initial' not in st.session_state:
    st.session_state['initial'] = # INSERT PROMPT

# Title
title = ("AgentAI")
st.title(title)

# Functions
def gpt3(prompt):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt= prompt,
    temperature=0.1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=["\n"]
    )
    # Get the response text
    response_text = response["choices"][0]["text"]
    # Print the response
    return response_text

def stop(string):
  return "{" in string

def agentAI_response(prompt, user_input):
  prompt = prompt + start_sequence + user_input + restart_sequence
  agent_response = gpt3(prompt)
  prompt = prompt + agent_response
  stop_test = stop(agent_response)
  if stop_test == True:
    params_api = agent_response # Use what is saved here to call API
    agent_response = "Searching ..."
  return agent_response, prompt

def get_text():
    input_text = st.text_input("Enter your message to speak to AgentAI: ","", key="text")
    return input_text

def clear_text():
    st.session_state["text"] = ""

# User Input
user_input = get_text()
st.button("Clear Text", on_click=clear_text)
if user_input:
    output, st.session_state['initial'] = agentAI_response(st.session_state['initial'], user_input)
    print(st.session_state['initial'])
    # Store the output 
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(output)

# Unraveling chat
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')



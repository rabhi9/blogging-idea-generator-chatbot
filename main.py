import streamlit as st
from openai import OpenAI
from lorem_text import lorem
import random
import time
import re


st . subheader ("Blogging Idea Generator AI Assistant")

openai_api_key = st.secrets['OPENAI_API_KEYS']

client = OpenAI(api_key=openai_api_key)

model = "gpt-4o-mini"


def response_generator (msg_type):
    msg = msg_type
    if (msg == "welcome_msg"):
        response = random.choice (
            [
                "Hi , which topic would you like blog ideas for today?",
                "Hi, human! Is there anything I can help you with?",
                "Do you need help writing your blog?",
            ]
        )
    for word in response.split ():
        yield word + " "
        time.sleep (0.05)
        
def validate_input (user_input):
    if not user_input.strip():
        return 0
    elif len(user_input) > 200:
        return 0
    elif not re.match(r"^[a-zA-Z0-9\s.,!?'-]+$", user_input):
        return 0
    return 1
      
def understand_input (user_input):
    topics = ["technology", "health", "travel", "food", "lifestyle", "finance", "education", "entertainment", "fitness", "fashion", "movie", "movies", "music", "sports", "gaming", "art", "history", "science", "politics", "environment", "business", "parenting", "relationships", "mental health", "spirituality", "writing"]
    
    tones = ["informative", "casual", "professional", "serious", "humorous", "funny", "inspirational", "persuasive", "conversational", "formal", "friendly", "critical", "optimistic", "realistic", "sarcastic", "empathetic", "motivational", "reflective", "analytical", "narrative", "descriptive", "explanatory"]
    
    topic = next ((t for t in topics if t in user_input.lower ()), None)
    
    tone = next ((tn for tn in tones if tn in user_input.lower ()), "descriptive")
    
    type = ["blogs", "posts", "articles", "ideas", "topics", "content", "titles", "headlines", "suggestions", "themes", "concepts", "outlines", "drafts", "plans", "strategies", "guides", "tips", "hints", "clues", "pointers", "blog", "post", "article", "idea", "topic", "title", "headline", "suggestion", "theme", "concept", "outline", "draft", "plan", "strategie", "guide", "tip", "hint", "clue", "pointer", "prompts", "prompt"]
    
    type = next ((t for t in type if t in user_input.lower ()), None)
    
    count = 0
    
    if type is not None:
        
        count_index = user_input.lower().index (type)
        scan_area = user_input[0: count_index-1]
        counts = re.findall(r'\d+', scan_area)
        count = int(counts[len(counts)-1])
            
    match = 1
    
    if len(st.session_state.messages) > 1 and topic is None:
        session_content = st.session_state.messages[1]["content"]
        topic = next ((t for t in topics if t in session_content.lower ()), random.choice (topics))
        match = 0
    elif topic is None:
        topic = "lifestyle"
        match = 0
    
    return topic , tone, match , count


if "messages" not in st.session_state:
    st.session_state.messages = []
    with st.chat_message ("assistant"):
        st.write_stream (response_generator ("welcome_msg"))


for message in st.session_state.messages:
    with st. chat_message(message["role"]):
        st.write(message["content"])
        

if user_input:= st. chat_input ("what is up?"):
    input_valid = validate_input(user_input)
    if input_valid == 1:
        topic, tone, match, count = understand_input(user_input)
        if count > 0 and count <= 10:
            st.chat_message ("user").markdown(user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            prompt = f"""
                You are an experienced and creative writing assistant that gives bloggers fresh and engaging blog post ideas that connect with the readers. Your job is to suggest short, original, and thought-provoking writing prompts based on the user's niche and tone preference and desired number of ideas.

                Topic:
                {topic}
                
                Tone:
                {tone}
                
                Number of Ideas:
                {count}

                Return the response in this format:
                Here are 3 travel blog post ideas written in a friendly tone :
                1. Idea 1
                2. Idea 2
                3. Idea 3
                and so on for the number of ideas specified by the user.
                ...
            
            """
            
            with st.chat_message("assistant"):
                stream = client.chat.completions.create (
                    model= model,
                    messages = [
                        {"role": "user", "content": prompt}
                    ],
                    stream = True,
                    max_tokens=500,  # Added: limit tokens to control costs
                    temperature=0.7
                )
                head_response = ""
                if match == 0:
                    head_response = "I couldn't find the prompt category from your input. But allow me to suggest a few prompt ideas which i feel would be relevant."
                    st.write(head_response)
                response = st.write_stream(stream)
                response = head_response + response
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.chat_message("assistant").write("Between 1 to 10 Blog ideas can only be genetated at a time")
    else:
        st.chat_message("assistant").write("Please enter a valid input.")
   

            

            

        

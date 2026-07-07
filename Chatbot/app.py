import streamlit as st
import time
import utils

# Page Configuration
st.set_page_config(
    page_title="Utility Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for aesthetics
st.markdown("""
<style>
    .stChatInput {border-radius: 20px;}
    .reportview-container {background: #f0f2f6;}
    h1 {color: #2e86de;}
    .sidebar .sidebar-content {background-color: #2e86de; color: white;}
    div.stButton > button:first-child {background-color: #2e86de; color: white; border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

# Application Title
st.title("🤖 Utility Chatbot Helper")
st.markdown("Your smart daily assistant.")

# Sidebar Navigation
with st.sidebar:
    st.header("👤 User Profile")
    user_name = st.text_input("Your Name:", "Friend")
    
    st.markdown("---")
    st.header("🛠️ Menu")
    option = st.radio("Choose a Feature:", 
                      ["Home / Chat", "Trip Planner ✈️", "Study Roadmap 📚", "Weather Info ☀️", "Today's News 📰", "Tech Quiz 🧠", "Pomodoro Timer ⏱️"])
    
    st.markdown("---")
    st.info("Built with Python & Streamlit")

# --- Feature: Home / Chat ---
if option == "Home / Chat":
    st.subheader(f"💬 Chat with Bot")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        st.session_state.messages.append({"role": "assistant", "content": f"Hi {user_name}! I'm your Utility Bot. I can tell jokes, give you weather info, or just chat. Ask me anything!"})

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask me a question or say 'tell me a joke'..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get bot response
        response = utils.get_bot_response(prompt, user_name)
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            # Simulate typing effect
            for chunk in response.split():
                full_response += chunk + " "
                time.sleep(0.04) # Slightly faster
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- Feature: Trip Planner ---
elif option == "Trip Planner ✈️":
    st.subheader("✈️ Trip Planner")
    st.write(f"Let's plan your next adventure, {user_name}!")
    
    col1, col2 = st.columns(2)
    with col1:
        destination = st.text_input("Where do you want to go?", "Paris")
        days = st.number_input("Number of days:", min_value=1, max_value=30, value=5)
    with col2:
        budget = st.text_input("Your Budget (USD):", "2000")
        
    if st.button("Generate Itinerary"):
        if destination and budget:
            with st.spinner("Planning your trip..."):
                time.sleep(1) # Fake loading
                itinerary = utils.plan_trip(destination, days, budget)
                st.success("Itinerary Ready!")
                st.markdown(itinerary)
        else:
            st.error("Please fill in all details.")

# --- Feature: Study Roadmap ---
elif option == "Study Roadmap 📚":
    st.subheader("📚 Study Roadmap")
    st.write("Choose a path to master!")
    
    topic = st.selectbox("Select Topic:", ["Python", "Data Structures & Algorithms (DSA)", "Web Development"])
    
    if st.button("Get Roadmap"):
        roadmap = utils.get_study_roadmap(topic)
        st.info(f"Roadmap for {topic}")
        st.markdown(roadmap)

# --- Feature: Weather Info ---
elif option == "Weather Info ☀️":
    st.subheader("☀️ Real-Time Weather")
    st.caption("Powered by Open-Meteo API")
    
    city = st.text_input("Enter City Name:", "New York")
    
    if st.button("Check Weather"):
        with st.spinner(f"Fetching live weather for {city}..."):
            data = utils.get_weather(city)
            
            if "error" in data:
                st.error(f"Error: {data.get('error')}")
            else:
                # Create metrics
                c1, c2, c3 = st.columns(3)
                c1.metric("Temperature", data["temperature"])
                c2.metric("Condition", data["condition"])
                c3.metric("Wind", data["humidity"])
                
                st.success(data["desc"])

# --- Feature: Today's News ---
elif option == "Today's News 📰":
    st.subheader("📰 Today's Headlines")
    
    if st.button("Fetch News"):
        with st.spinner("Fetching top stories..."):
            time.sleep(1)
            news = utils.get_news()
            st.markdown(news)
    else:
        st.write("Click the button to see what's happening today.")

# --- Feature: Tech Quiz ---
elif option == "Tech Quiz 🧠":
    st.subheader("🧠 Tech Snippet Quiz")
    
    if 'quiz_data' not in st.session_state:
        st.session_state.quiz_data = utils.get_tech_quiz()
        st.session_state.quiz_answered = False

    q_data = st.session_state.quiz_data
    
    st.markdown(f"**Question:** {q_data['question']}")
    
    user_answer = st.radio("Choose correct answer:", q_data['options'], key="quiz_option")
    
    if st.button("Submit Answer"):
        if user_answer == q_data['answer']:
            st.success("🎉 Correct Answer!")
            st.balloons()
        else:
            st.error(f"❌ Wrong! The correct answer was: {q_data['answer']}")
        st.session_state.quiz_answered = True
            
    if st.session_state.quiz_answered:
        if st.button("Next Question"):
            st.session_state.quiz_data = utils.get_tech_quiz()
            st.session_state.quiz_answered = False
            st.rerun()

# --- Feature: Pomodoro Timer ---
elif option == "Pomodoro Timer ⏱️":
    st.subheader("⏱️ Pomodoro Timer")
    st.write("Stay focused for 25 minutes!")
    
    if 'pomodoro_time' not in st.session_state:
        st.session_state.pomodoro_time = 25 * 60 # 25 minutes
    
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False

    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Start Timer"):
            st.session_state.timer_running = True
    with col2:
        if st.button("Stop"):
            st.session_state.timer_running = False
    with col3:
        if st.button("Reset"):
            st.session_state.pomodoro_time = 25 * 60
            st.session_state.timer_running = False
            
    timer_placeholder = st.empty()
    
    if st.session_state.timer_running:
        while st.session_state.pomodoro_time > 0 and st.session_state.timer_running:
            mins, secs = divmod(st.session_state.pomodoro_time, 60)
            timer_placeholder.markdown(f"# ⏳ {mins:02d}:{secs:02d}")
            time.sleep(1)
            st.session_state.pomodoro_time -= 1
            
        if st.session_state.pomodoro_time == 0:
            st.success("⏰ Time's up! Take a break.")
            st.session_state.timer_running = False
            st.balloons()
    else:
        mins, secs = divmod(st.session_state.pomodoro_time, 60)
        timer_placeholder.markdown(f"# ⏳ {mins:02d}:{secs:02d}")

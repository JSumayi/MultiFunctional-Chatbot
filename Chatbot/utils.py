import random
import datetime
import requests

def get_bot_response(user_input, user_name="User"):
    """
    Enhanced keyword-based chatbot response with personalization and jokes.
    """
    user_input = user_input.lower()
    
    greetings = ["hi", "hello", "hey", "hola", "greetings"]
    help_keywords = ["help", "support", "assist", "guide"]
    joke_keywords = ["joke", "funny", "laugh"]
    
    # Q&A Knowledge Base
    qa_db = {
        "python": "Python is a high-level, interpreted programming language known for its readability and vast ecosystem.",
        "streamlit": "Streamlit is a Python library that lets you turn data scripts into shareable web apps in minutes.",
        "api": "API stands for Application Programming Interface. It allows different software systems to communicate with each other.",
        "chatbot": "I am a utility chatbot built with Python and Streamlit to help you with daily tasks!",
        "who are you": f"I'm your personal utility assistant, {user_name}! I can help with travel, studies, weather, and more.",
        "author": "I was built by a developer using Python! 🐍",
        "time": f"The current time is {datetime.datetime.now().strftime('%H:%M')}.",
        "date": f"Today's date is {datetime.datetime.now().strftime('%Y-%m-%d')}."
    }

    if any(word in user_input for word in greetings):
        return f"Hello {user_name}! 👋 I'm your Utility Bot. I can help you with Trip Planning, Study Roadmaps, Weather, News, and I can even tell jokes! Check the sidebar functionality!"
    
    if any(word in user_input for word in help_keywords):
        return "I can help with:\n- Trip Planning ✈️\n- Study Roadmaps 📚\n- Weather Info ☀️\n- Today's News 📰\n- Tech Quiz 🧠\n- Pomodoro Timer ⏱️\n\nSelect a tool from the sidebar to get started!"

    if any(word in user_input for word in joke_keywords):
        return get_joke()
    
    if "bye" in user_input:
        return f"Goodbye {user_name}! Have a great day! 👋"
        
    # Check Q&A
    for key in qa_db:
        if key in user_input:
            return qa_db[key]

    return f"I didn't quite catch that, {user_name}. Try asking 'tell me a joke', 'what is python', or ask for 'help'!"

def get_joke():
    """
    Returns a random tech joke.
    """
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
        "I told my computer I needed a break, and now it won't stop sending me Kit-Kats.",
        "Why did the Python programmer get rejected? He didn't have any Class.",
        "0 is false and 1 is true, right? 1.",
        "Why do Java programmers have to wear glasses? Because they don't C#.",
        "A SQL query walks into a bar, walks up to two tables and asks... 'Can I join you?'"
    ]
    return random.choice(jokes)

def plan_trip(destination, days, budget):
    """
    Generates a mock travel itinerary.
    """
    budget_val = float(budget.replace('$','').replace(',','')) if hasattr(budget, 'replace') else float(budget)
    
    daily_budget = budget_val / days
    
    travel_styles = ["Backpacking", "Comfortable", "Luxury"]
    style = "Standard"
    if daily_budget < 50:
        style = travel_styles[0]
    elif daily_budget > 200:
        style = travel_styles[2]
    else:
        style = travel_styles[1]
        
    itinerary = f"### ✈️ Trip to {destination} ({days} Days)\n"
    itinerary += f"**Budget:** ${budget_val:.2f} (Approx. ${daily_budget:.2f}/day)\n"
    itinerary += f"**Travel Style:** {style}\n\n"
    
    activities = [
        "Visit the city center and famous landmarks",
        "Explore local museums and art galleries",
        "Enjoy local cuisine at popular food spots",
        "Relax at the city park or botanical garden",
        "Take a guided walking tour",
        "Shopping at local markets",
        "Visit historical sites"
    ]
    
    for day in range(1, days + 1):
        day_activity = random.sample(activities, 2)
        itinerary += f"**Day {day}:**\n"
        itinerary += f"- Morning: {day_activity[0]}\n"
        itinerary += f"- Afternoon: {day_activity[1]}\n"
        itinerary += "- Evening: Dinner & Leisure\n\n"
        
    return itinerary

def get_study_roadmap(topic):
    """
    Returns a static study roadmap for specific topics.
    """
    topic = topic.lower()
    
    if "python" in topic:
        return """### 🐍 Python Study Roadmap
**Week 1: Basics**
- Variables, Data Types, Strings
- Control Flow (if/else, loops)
- Functions

**Week 2: Data Structures**
- Lists, Tuples, Dictionaries, Sets
- List Comprehensions

**Week 3: OOP & Modules**
- Classes & Objects
- Inheritance
- Importing Modules (math, random, datetime)

**Week 4: Advanced & Projects**
- File I/O
- Error Handling (try/except)
- Mini Project: Calculator or Todo List
"""
    elif "dsa" in topic:
        return """### 🧠 Data Structures & Algorithms Roadmap
**Month 1: Fundamentals**
- Big O Notation
- Arrays & Strings
- Pointers (if C++) / References

**Month 2: Linear Data Structures**
- Linked Lists
- Stacks & Queues
- Hash Tables

**Month 3: Algorithms**
- Sorting (Merge, Quick)
- Searching (Binary Search)
- Recursion

**Month 4: Trees & Graphs**
- Binary Trees, BST
- DFS & BFS
- Graph Traversal
"""
    elif "web" in topic:
        return """### 🌐 Web Development Roadmap
**Phase 1: The Frontend Trinity**
- HTML5 (Semantic tags, Structure)
- CSS3 (Flexbox, Grid, Responsive Design)
- JavaScript (ES6+, DOM Manipulation)

**Phase 2: Frontend Frameworks**
- React.js / Vue / Svelte
- State Management
- API Fetching

**Phase 3: Backend Basics**
- Node.js / Python (Django/Flask)
- Databases (SQL vs NoSQL)
- Authentication
"""
    else:
        return "⚠️ Roadmap not found. Currently calling support for: Python, DSA, Web Development."

def get_weather(city):
    """
    Returns REAL weather data from Open-Meteo API.
    """
    try:
        # 1. Geocoding to get lat/long
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        geo_res = requests.get(geo_url).json()
        
        if "results" not in geo_res:
             return {"error": "City not found"}

        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]
        city_name = geo_res["results"][0]["name"]

        # 2. Get Weather
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_res = requests.get(weather_url).json()
        
        current = weather_res["current_weather"]
        temp = current["temperature"]
        wind = current["windspeed"]
        
        # Determine condition based on WMO code
        wmo_code = current.get("weathercode", 0)
        condition = "Clear"
        if wmo_code in [1, 2, 3]: condition = "Cloudy"
        elif wmo_code in [45, 48]: condition = "Foggy"
        elif wmo_code in [51, 53, 55, 61, 63, 65]: condition = "Rainy"
        elif wmo_code in [71, 73, 75]: condition = "Snowy"
        elif wmo_code >= 95: condition = "Thunderstorm"

        return {
            "city": city_name,
            "temperature": f"{temp}°C",
            "condition": condition,
            "humidity": f"Wind: {wind} km/h", # API doesn't give humidity in free simple endpoint easily without extra params
            "desc": f"Current weather in {city_name}: {condition}, {temp}°C."
        }
        
    except Exception as e:
        return {
            "error": "Unable to fetch data",
            "details": str(e)
        }

def get_news():
    """
    Returns top mock headlines.
    """
    headlines = [
        "Tech Giant Releases Revolutionary AI Model Today",
        "Global Stock Markets Reach All-Time High",
        "New Species of Deep Sea Fish Discovered in Pacific",
        "SpaceX Successfully Launches New Starship Mission",
        "Python 3.14 Release Features Announced: What to Expect"
    ]
    
    news_feed = "### 📰 Today's Top Headlines\n"
    for i, news in enumerate(headlines, 1):
        news_feed += f"{i}. {news}\n"
    
    return news_feed

def get_tech_quiz():
    """
    Returns a random tech quiz question.
    """
    questions = [
        {
            "question": "What is the output of `print(2 ** 3)` in Python?",
            "options": ["6", "8", "9", "Error"],
            "answer": "8"
        },
        {
            "question": "Which data structure runs on LIFO principle?",
            "options": ["Queue", "Stack", "Array", "Tree"],
            "answer": "Stack"
        },
        {
            "question": "What does CSS stand for?",
            "options": ["Computer Style Sheets", "Cascading Style Sheets", "Creative Style System", "Colorful Style Sheets"],
            "answer": "Cascading Style Sheets"
        },
        {
            "question": "Which of these is NOT a Python data type?",
            "options": ["List", "Tuple", "Dictionary", "Array"],
            "answer": "Array"
        },
        {
            "question": "What is the time complexity of binary search?",
            "options": ["O(n)", "O(log n)", "O(n^2)", "O(1)"],
            "answer": "O(log n)"
        }
    ]
    return random.choice(questions)

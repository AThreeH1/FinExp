import streamlit as st
import os
from PIL import Image
import openai
import plotly.graph_objects as go
import json

# Set up OpenAI API credentials
openai.api_key = "YOUR_API_KEY"

descpr = "Experiment Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s..."

def select_image(folder):
    image_files = os.listdir(folder)
    image_path = os.path.join(folder, image_files[0])
    return image_path

def image_selector(option):
    folder_mapping = {
        "A": r"C:\Study\Finance\IIMV Intern\Experiment Images\A",
        "B": r"C:\Study\Finance\IIMV Intern\Experiment Images\B",
        "C": r"C:\Study\Finance\IIMV Intern\Experiment Images\C",
        "D": r"C:\Study\Finance\IIMV Intern\Experiment Images\D"
    }
    folder_path = folder_mapping[option]
    image_path = select_image(folder_path)
    return image_path

def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply

def display_image_selector():
    st.header("Image Selector")
    st.write(descpr)

    option = st.selectbox("Select an option", ["A", "B", "C", "D"])

    image_path = image_selector(option)
    image = Image.open(image_path)
    st.image(image)

def display_chatbox():
    st.subheader("Chatbox")

    messages = []

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("User Input")

    if st.button("Send"):
        if user_input:
            st.session_state.chat_history.append(("User", user_input))
            st.session_state.chat_history, _ = chatbot(user_input, st.session_state.chat_history)

    if st.session_state.chat_history:
        for chat in st.session_state.chat_history:
            if chat[0] == "User":
                st.text_input("User", chat[1], disabled=True)
            else:
                st.text_input("Assistant", chat[1], disabled=True)

def main():
    # Title
    st.title("Stock Trading App")

    # Create a session state to retain the stock values
    session_state = st.session_state.setdefault("stock_values", {"A": 0, "B": 0, "C": 0, "D": 0})

    # Sliders for stock values
    session_state["A"] = st.slider("A", min_value=0, max_value=100, value=session_state["A"])
    session_state["B"] = st.slider("B", min_value=0, max_value=100, value=session_state["B"])
    session_state["C"] = st.slider("C", min_value=0, max_value=100, value=session_state["C"])
    session_state["D"] = st.slider("D", min_value=0, max_value=100, value=session_state["D"])

    # Display the pie chart
    display_pie_chart(session_state)

def display_pie_chart(stock_values):
    st.subheader("Stocks Overview")
    stock_labels = list(stock_values.keys())
    stock_values = list(stock_values.values())
    fig = go.Figure(data=[go.Pie(labels=stock_labels, values=stock_values)])
    st.plotly_chart(fig)

def get_user_details():
    st.subheader("User Details")
    username = st.text_input("Username")
    phone_number = st.text_input("Phone Number")
    if st.button("Start"):
        if username and phone_number:
            user_details = {
                "username": username,
                "phone_number": phone_number,
                "stock_values": {"A": 0, "B": 0, "C": 0, "D": 0}
            }
            st.session_state.user_details = user_details
            st.session_state.show_app = True
            save_user_details(user_details)

def save_user_details(user_details):
    data_folder = r"C:\Study\Finance\IIMV Intern\Data"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    file_path = os.path.join(data_folder, f"{user_details['username']}.json")
    with open(file_path, "w") as file:
        json.dump(user_details, file)

def show_app():
    display_image_selector()
    display_chatbox()
    main()

if __name__ == "__main__":
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
    st.sidebar.title("Welcome to the Stock Trading App")
    get_user_details()

    if "show_app" in st.session_state and st.session_state.show_app:
        show_app()

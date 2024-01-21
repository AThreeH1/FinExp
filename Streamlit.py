import streamlit as st
import os
from PIL import Image
import openai
import plotly.graph_objects as go
import json

# Set up OpenAI API credentials
openai.api_key = "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"

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

messages = []

def CustomChatGPT(user_input):
    global messages
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

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("User Input")

    if st.button("Send"):
        if user_input:
            st.session_state.chat_history.append(("User", user_input))
            response = CustomChatGPT(user_input)
            st.session_state.chat_history.append(("Assistant", response))

    if st.session_state.chat_history:
        for chat in st.session_state.chat_history:
            if chat[0] == "User":
                st.text_input("User", chat[1], disabled=True)
            else:
                st.text_input("Assistant", chat[1], disabled=True)

def main():

    #Title for the sliders
    st.title("Add Stocks")

    # Create a session state to retain the stock values and balance
    session_state = get_session_state()

    col1, col2 = st.columns(2)

    with col1:
        session_state.stock_values["A"] = st.slider("A", min_value=0, max_value=100, value=0)
        session_state.buy_sell_values["A"] = st.radio("Buy/Sell A", ["Buy", "Sell"])

    with col2:
        session_state.stock_values["B"] = st.slider("B", min_value=0, max_value=100, value=0)
        session_state.buy_sell_values["B"] = st.radio("Buy/Sell B", ["Buy", "Sell"])

    col3, col4 = st.columns(2)

    with col3:
        session_state.stock_values["C"] = st.slider("C", min_value=0, max_value=100, value=0)
        session_state.buy_sell_values["C"] = st.radio("Buy/Sell C", ["Buy", "Sell"])

    with col4:
        session_state.stock_values["D"] = st.slider("D", min_value=0, max_value=100, value=0)
        session_state.buy_sell_values["D"] = st.radio("Buy/Sell D", ["Buy", "Sell"])

    update_balance(session_state)

    # Display the balance
    st.subheader("Balance")
    st.write(f"${session_state.balance}")

    # Display the pie chart
    display_pie_chart(session_state.stock_values)



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
                "stock_values": {"A": 0, "B": 0, "C": 0, "D": 0},
                "balance": 100
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

def get_session_state():
    if "stock_values" not in st.session_state:
        st.session_state.stock_values = {"A": 0, "B": 0, "C": 0, "D": 0}
        st.session_state.buy_sell_values = {"A": "", "B": "", "C": "", "D": ""}
        st.session_state.balance = 100
    return st.session_state

def update_balance(session_state):
    total_value = sum(session_state.stock_values.values())
    session_state.balance = 100 - total_value

class SessionState:
    def __init__(self):
        self.stock_values = {"A": 0, "B": 0, "C": 0, "D": 0}
        self.buy_sell_values = {"A": "", "B": "", "C": "", "D": ""}
        self.balance = 100

if __name__ == "__main__":
    st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
    st.sidebar.title("Welcome to the Stock Trading App")
    get_user_details()

    if "show_app" in st.session_state and st.session_state.show_app:
        show_app()
                
    if st.button("Submit"):
        if "user_details" in st.session_state:
            user_details = st.session_state.user_details
            user_details["stock_values"] = {}
            total_value = 0
            for stock, value in st.session_state.stock_values.items():
                buy_sell = st.session_state.buy_sell_values[stock]
                if buy_sell == "Sell":
                    value = -value
                user_details["stock_values"][stock] = value
                total_value += abs(value)
            user_details["balance"] = 100 - total_value
            if user_details["balance"] >= 0:
                save_user_details(user_details)
                st.write("Submission successful!")
            else:
                st.write("Submission unsuccessful. Insufficient balance.")

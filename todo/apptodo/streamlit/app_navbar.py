import streamlit as st
from streamlit_option_menu import option_menu
from fastapi import requests

with st.sidebar:
    selected = option_menu(
    menu_title = "Todo App",
    options=["Home", "Profile", "Login", "Register", "Profile Setting"],
    icons = ["house", "person", "arrow-return-right", "arrow-up-right-circle", "gear"],
    menu_icon = "cast",
    default_index = 0,
)


if selected == "Home":
    top_nav = option_menu(
    menu_title = None,
    options=["Tasks", "Assigned Me", "Update", "Delete"],
    icons = ["plus", "person-fill-down", "pencil", "trash"],
    menu_icon = "cast",
    default_index = 0,
    orientation = "horizontal",
)
    if top_nav == "Tasks":
        st.title("Create Your Todo")
        st.text_input('Enter Your Todo Task Title')
        st.text_area('Enter Your Todo Task Details')
        st.number_input('Enter TOdo Task Priority',1,5)
        st.selectbox('Task Completion', ['False'])
        st.button('Submit')

    if top_nav == "Update":
        st.title("Update Todo")
        st.text_input('Enter Your Todo Task ID')
        st.text_input('Enter Your Todo Task Tittle')
        st.text_area('Enter Your Todo Task Description')
        st.number_input('Enter TOdo Task Priority',1,5)
        st.selectbox('Task Completion', ['True', 'False'])
        st.button('Submit')

    if top_nav == "Delete":
        st.title("Delete Todo")
        st.markdown("Only Admin Can Delete Todo")
        st.text_input('Select Task ID Number')
        st.button('Submit')
    

if selected == "Login":
    st.title(f"{selected}")
    st.text_input('Enter Username')
    st.text_input('Enter Password')
    st.button('Submit')

if selected == "Register":
    st.title(f"{selected}")
    st.text_input('Enter Uername')
    st.text_input('Enter Your Email')
    st.text_input('Enter Your First Name')
    st.text_input('Enter Your Last Name')
    st.text_input('Enter Your Role')
    st.text_input('Enter Your Phone Number')
    st.button('Submit')

if selected == "Profile Setting":
    Setting = option_menu(
    menu_title = None,
    options=["Change Password", "Change Number"],
    icons = ["pencil", "pencil"],
    menu_icon = "cast",
    default_index = 0,
    orientation = "horizontal",
    )
    if Setting == "Change Password":
        st.text_input('Enter Old Password')
        st.text_input('Enter New Password')
        st.button('Submit')

    if Setting == "Change Number":
        st.text_input('Enter Old Phone Number')
        st.text_input('Enter New Phone Number')
        st.button('Submit')







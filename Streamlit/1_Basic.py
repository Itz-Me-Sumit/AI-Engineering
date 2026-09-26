import streamlit as st

# First Streamlit app
# """
# st.title("My First Streamlit APP")
# st.write("Welcome to my first Streamlit Application")
# st.write("Streamlit allows us to build data app using only Python!!")
# """

# Test & Markdown Display
# st.title("Text display is streamlit")
# st.header("This is a header")
# st.subheader("This is a sub-header")
# st.text("This is a text")
# st.markdown("""
#     ### Markdown supported

#     you can write in **bold-text**, *itelic-text* 

#     and create List
#     - Item 1
#     - Item 2 
#     - Item 3

# """)


# User Input - text input
# st.title("User Input Example")
# name = st.text_input("Enter Your Name")
# if name:
#     st.write(f"Hello {name} , Welcome to my Streamlit APP")


# st.title("Interactive Sliders")
# age = st.slider("Select Your Age" , 0 , 100 , 25)
# st.write(f"Your Age is {age}")

# num = st.number_input("Enter a Number from 0 to 100" , min_value=0 , max_value=100)
# st.write(f"Number selected {num}")

# select Buttons and actions
# st.title("Button Examples")
# if st.button("Click Me"):
#     st.success("You Clicked The Button")

# Select Box And titles
# st.title("Select Box Example")
# language = st.selectbox(
#     "Choose your fav Programming Language",
#     ["Java" , "Python" , "C++" , "Rust"]
# )
# st.write(f"Your Fav Programming Language is {language}")

# st.checkbox("What is your domain" , )

# st.sidebar.title("Sidebar Menu")
# option = st.sidebar.selectbox(
#     "Choose the page" ,
#     ["Home" , "About" , "Contact"]
# )
# st.write(f"You Selected {option}")

# Column Layout
st.title("Column Layout")
col1 , col2 = st.columns(2)

with col1:
    st.header("Column 1")
    st.write("This is the first column")

with col2:
    st.header("Column 2")
    st.write("This is the second Column")


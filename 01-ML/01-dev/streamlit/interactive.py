import streamlit as st
import datetime
import pandas as pd
from PIL import Image
import cv2

# Documentation Ref: https://docs.streamlit.io/library/api-reference/widgets

# Title
st.title("Interactive Elements Example")

# Button
st.header("Button")
if st.button("Click me"):
    st.write("Button clicked!")

# Checkbox
st.header("Checkbox")
checkbox_result = st.checkbox("Check me")
st.write(f"Checkbox is {'checked' if checkbox_result else 'unchecked'}")

# Radio Buttons
st.header("Radio Buttons")
radio_result = st.radio("Choose an option", ["Option 1", "Option 2", "Option 3"])
st.write(f"You selected: {radio_result}")

# Slider
st.header("Slider")
slider_value = st.slider("Select a value", min_value=0, max_value=10, step=1)
st.write(f"Slider value: {slider_value}")

# Select Slider
st.header("Select Slider")

min_range = 0
max_range = 100

selected_range = st.slider("Select a range", min_value=min_range, max_value=max_range, value=(25, 75))
st.write(f"You selected range: {selected_range[0]} to {selected_range[1]}")
st.progress((selected_range[0] - min_range) / (max_range - min_range))
st.progress((selected_range[1] - min_range) / (max_range - min_range))

# Selectbox
st.header("Selectbox")
options = ["Option A", "Option B", "Option C"]
selectbox_result = st.selectbox("Select an option", options)
st.write(f"You selected: {selectbox_result}")

# Multi-Select
st.header("Multi-Select")
multiselect_result = st.multiselect("Select multiple options", options)
st.write(f"You selected: {multiselect_result}")

# Text Input
st.header("Text Input")
text_input = st.text_input("Enter text", "Default text")
st.write(f"You entered: {text_input}")

# Number Input
st.header("Number Input")
number_input = st.number_input("Enter a number", min_value=0, max_value=100, value=50)
st.write(f"You entered: {number_input}")

# Text Area
st.header("Text Area")
text_area = st.text_area("Enter your message", "Hello, Streamlit!")
st.write(f"You entered: {text_area}")

# Date Input
st.header("Date Input")
date_input = st.date_input("Select a date", datetime.date.today())
st.write(f"You selected: {date_input}")

# Time Input
st.header("Time Input")
time_input = st.time_input("Select a time", datetime.time(12, 0))
st.write(f"You selected: {time_input}")

# File Upload
st.header("File Upload")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded DataFrame:")
    st.write(df)

    # Download Button
    csv_download = df.to_csv(index=False)
    st.download_button("Download CSV", data=csv_download, file_name="uploaded_data.csv")

# Color Picker
st.header("Color Picker")
color = st.color_picker("Pick a color", "#00f")
st.write(f"You picked color: {color}")

# Camera Input
st.header("Camera Input")
st.write("Click the button below to start capturing from your camera:")

start_camera = st.button("Start Camera")

if start_camera:
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        st.image(frame, channels="RGB", use_column_width=True)

        if st.button("Stop Camera"):
            cap.release()
            break

# Disclaimer
st.sidebar.markdown("Note: The camera input feature may not work in all environments due to security restrictions.")
import streamlit as st

# Title
st.title("Title")

# Title With Achor
# Optional anchor parameter can be used in st.title(), st.header(), and st.subheader()
st.title("Title", anchor="Streamlit")

# Header
st.header("Header")

# Sub-header
st.subheader("Sub-header")

# Caption, used as describes notes, footnotes, tables, images, and videos.
st.caption("Caption")

# Plain Text, it will appear on a new line
st.text("Text")

# Markdown
st.markdown('# Markdown Header')

# LaTeX is formatted text used for technical documentation.
st.latex("""(a+b)^2 = a^2 + b^2 + 2ab""")

# Code highliter, if language is not added then it will display unformatted
st.subheader("""Python Code""")
code = '''def hello():
     print("Hello, Streamlit!")'''
st.code(code, language='python')


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

# Caption, used as describes notes, footnotes, tables, images, and videos
st.caption("Caption")

# Plain Text, it will appear on a new line, not data formatting
st.text("Text")

# Markdown
st.markdown('# Markdown Header')

# LaTeX is formatted text used for technical documentation
st.latex("""(a+b)^2 = a^2 + b^2 + 2ab""")

# Code highliter, if language is not added then it will display unformatted
st.subheader("""Python Code""")
code = '''def hello():
     print("Hello, Streamlit!")'''
st.code(code, language='python')

# Displaying Variables, write support display and auto formating multiple data types
name = "Alice"
age = 30
st.write(f"Name: {name}, Age: {age}")

# Justified Text Alignmet
st.write("Center aligned text", justify="center")
st.write("Right aligned text", justify="right")

# Superscript and Subscript
st.write("x<sup>2</sup> + y<sub>2</sub> = z")

# Horizontal Rule
st.markdown("---")

# Metrics, helps the user see any changes in the data easily
st.metric( label="Population", value="1.6 Billions", delta="1 Billions", delta_color="inverse" )
st.metric( label="Population", value="1.6 Billions", delta="1 Billions", delta_color="off" )
st.metric( label="Population", value=None, delta="1 Billions")
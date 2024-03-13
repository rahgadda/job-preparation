import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load PI2 model and tokenizer
model_name = "microsoft/phi-2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def extract_text(uploaded_file):
  """Extracts text content from uploaded PDF"""
  # Use a PDF parsing library like PyPDF2 to extract text
  # This example omits the implementation for brevity
  # Replace with your preferred PDF parsing logic
  pass

def chat(text, question):
  """Chats with the PI2 model using the provided text and question"""
  input_ids = tokenizer(question, return_tensors="pt")["input_ids"]
  with torch.no_grad():
    output = model.generate(input_ids, max_length=1024)  # Adjust max_length as needed
  response = tokenizer.decode(output[0], skip_special_tokens=True)
  return response

def main():
  """Main function to run the Streamlit app"""
  st.title("Chat with your PDF")
  uploaded_file = st.file_uploader("Upload PDF", type="pdf")

  if uploaded_file is not None:
    text = extract_text(uploaded_file)  # Replace with extracted text
    
    if text:
      question = st.text_input("Ask a question about the document:")
      if question:
        response = chat(text, question)
        st.write(response)
    else:
      st.write("Failed to extract text from PDF.")

if __name__ == "__main__":
  main()

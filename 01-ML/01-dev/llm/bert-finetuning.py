import pandas as pd
from transformers import BertForQuestionAnswering, BertTokenizer, pipeline

############################
###### Global Variables ####
############################

Stanford_CoQA_Data = pd.DataFrame()
model_name = 'bert-base-uncased'
model = BertForQuestionAnswering.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

############################
###### Generic Code #######
############################

# Generate a random story, question and answer
def generate_qa_dataframe():
    
    # 1) Identifying dataset 
    Stanford_CoQA_Data_Raw = pd.read_json('http://downloads.cs.stanford.edu/nlp/data/coqa/coqa-train-v1.0.json')

    # 2) Transforming data in Story, Question, Answer
    # -- Required columns in our data frame
    cols = ["story","question","answer"]
    
    # -- Creating new dataframe
    temp_list=[]
    for index, row in Stanford_CoQA_Data_Raw.iterrows():
        for i in range(len(row["data"]["questions"])):
            temp_row = []
            temp_row.append(row["data"]["story"])
            temp_row.append(row["data"]["questions"][i]["input_text"])
            temp_row.append(row["data"]["answers"][i]["input_text"])
            temp_list.append(temp_row)
    
    Stanford_CoQA_Data= pd.DataFrame(temp_list, columns=cols)

    # -- Saving the dataframe to csv file for further loading
    # Stanford_CoQA_Data.to_csv("Stanford_ConversationalQA_Data.csv", index=False)
    
    # -- Statistics
    print(Stanford_CoQA_Data.head())
    print("Number of question and answers: ", len(Stanford_CoQA_Data))

# Training or Fine-tuning Model with QA
outputs = None
def train_bert_model():
    for example in Stanford_CoQA_Data:
        inputs = tokenizer(example['question'], example['story'], return_tensors="pt", padding="max_length", truncation=True)
        outputs = model(**inputs, start_positions=inputs['input_ids'].tolist().index(tokenizer.convert_tokens_to_ids(tokenizer.tokenize(example['answer']))), end_positions=inputs['input_ids'].tolist().index(tokenizer.convert_tokens_to_ids(tokenizer.tokenize(example['answer']))))
        loss = outputs.loss
        loss.backward()
    
    nlp_qa = pipeline("question-answering", model=outputs, tokenizer=tokenizer)
    
    # -- Example user input
    user_input = {
        "story": "The Vatican Apostolic Library (), more commonly called the Vatican Library or simply the Vat, is the library of the Holy See, located in Vatican City. Formally established in 1475, although it is much older, it is one of the oldest libraries in the world and contains one of the most significant collections of historical texts. It has 75,000 codices from throughout history, as well as 1.1 million printed books, which include some 8,500 incunabula. \n\nThe Vatican Library is a research library for history, law, philosophy, science and theology. The Vatican Library is open to anyone who can document their qualifications and research needs. Photocopies for private study of pages from books published between 1801 and 1990 can be requested in person or by mail. \n\nIn March 2014, the Vatican Library began an initial four-year project of digitising its collection of manuscripts, to be made available online. \n\nThe Vatican Secret Archives were separated from the library at the beginning of the 17th century; they contain another 150,000 items. \n\nScholars have traditionally divided the history of the library into five periods, Pre-Lateran, Lateran, Avignon, Pre-Vatican and Vatican. \n\nThe Pre-Lateran period, comprising the initial days of the library, dated from the earliest days of the Church. Only a handful of volumes survive from this period, though some are very significant.",
        "question": "what started in 2014"
    }

    # -- Perform inference
    answer = nlp_qa(question=user_input['question'], context=user_input['story'])
    print("Answer:", answer['answer'])

# Testing Model
def test_bert_model():
    null


############################
######## Main Code #########
############################

# Start of Program - Main
def main():
    generate_qa_dataframe()
    train_bert_model()
    # test_bert_model()

# Calling Main Function
if __name__ == '__main__':
    main()

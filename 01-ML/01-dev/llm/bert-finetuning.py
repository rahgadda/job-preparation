import pandas as pd

############################
###### Generic Code #######
############################

# Generate a random story, question and answer
def generate_qa():
    
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
    Stanford_CoQA_Data.head()
    print("Number of question and answers: ", len(Stanford_CoQA_Data))

############################
######## Main Code #########
############################

# Start of Program - Main
def main():
    generate_qa()

# Calling Main Function
if __name__ == '__main__':
    main()

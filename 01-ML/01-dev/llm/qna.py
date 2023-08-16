from transformers import pipeline

# Initializating Model with pipeline
question_answer_model = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# Question n Answer Function
def qna(question,context):
    print(
        question_answer_model ( 
            question=question,  
            context=context
        )
    )

# Main Function
def main():
    # -- Question-1
    print("\n====================================================")
    context="Once upon a time, in a faraway land, there lived a brave knight named Sir Lancelot. He was known throughout the kingdom for his courage and valor. One day, a fearsome dragon appeared and began terrorizing the villagers. The king announced a reward for whoever could defeat the dragon..."
    
    question="Who was the brave knight?"
    qna(question, context)
    question="What were the great qualities of knight?"
    qna(question, context)
    question="What attacked village?"
    qna(question, context)

    # -- Question-2
    print("\n====================================================")
    context="In the bustling city of New York, a young artist named Emily was struggling to make a name for herself in the competitive art scene. Her unique style and creative vision set her apart, but success seemed elusive. One day, she stumbled upon an old art gallery that was known to have hidden treasures. As she explored the gallery, she discovered a mysterious painting that seemed to radiate an otherworldly energy..."
    
    question="What was the name of the young artist?"
    qna(question, context)
    question="Where did Emily find the mysterious painting?"
    qna(question, context)
    question="What did the painting in the gallery radiate?"
    qna(question, context)

    # -- Question-3
    print("\n====================================================")
    question="Where were the explorers conducting their expedition?"
    context="Deep in the heart of the Amazon rainforest, a team of explorers embarked on a quest to uncover the secrets of an ancient civilization. Led by Dr. Maria Ramirez, an archaeologist with a passion for history, the team braved treacherous terrain and encountered unexpected challenges. During their journey, they stumbled upon a hidden temple, adorned with intricate carvings and artifacts. As they delved deeper, they discovered a chamber that held a map to a legendary lost city..."
    qna(question, context)
    question="Who was leading the team of explorers?"
    qna(question, context)
    question="What did the explorers discover inside the hidden temple?"
    qna(question, context)

# Calling Main Function
if __name__ == '__main__':
    main()
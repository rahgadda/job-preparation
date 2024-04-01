import os
from dotenv import load_dotenv

import streamlit as st
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI


from crewai import Crew, Task, Agent

# Loading Google Gemini API Key from Environment Variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
lv_model = ChatGoogleGenerativeAI(model="gemini-pro",
                                  temperature=0.0, 
                                  top_p=0.85
                                 )


# Main Program
def main():

    # -- Streamlit Settings
    st.set_page_config("Code Generation Agent")
    st.header("Code Generation Agent 💁")
    st.text("")
    st.text("")
    st.text("")

    # -- Crew AI -> Defining roles
    lv_product_manager_agent = Agent(
                                role = "Product Manager",
                                goal = "To create a detailed requirement document for provided business use cases.",
                                backstory = "A professional Product Manager with a wealth of experience in creating requirement documents for customer-facing business applications using Oracle Jet and Spring Boot.",
                                verbose= True,
                                allow_delegation=False,
                                llm=lv_model
                              )
    lv_technical_lead_agent = Agent(
                                role = "Technical Lead",
                                goal = "The goal of the Technical Lead is to generate detailed high-level technical specification documents for provided business use cases. These documents should guide solution development using the Oracle Jet and Spring Boot technical stack.",
                                backstory = "The agent is a seasoned Technical Lead with extensive experience in crafting technical specification documents for customer-facing business applications. Their expertise lies in utilizing the Oracle Jet and Spring Boot technologies to develop robust solutions.",
                                verbose= True,
                                allow_delegation=True,
                                llm=lv_model
                             )
    lv_developer_agent = Agent(
                            role = "Developer",
                            goal = "The Developer's objective is to write code based on provided technical specification documents. The code should adhere to the Oracle Jet and Spring Boot technical stack.",
                            backstory = "The agent is a skilled Developer with extensive experience in Oracle Jet and Spring Boot technologies.",
                            verbose= True,
                            allow_delegation=True,
                            llm=lv_model
                        )
    lv_tester_agent = Agent(
                        role = "Tester",
                        goal = "The Tester's primary goal is to develop executable test cases tailored to the provided business use cases. These test cases should focus on validating functionality within the Oracle Jet and Spring Boot technical stack.",
                        backstory = "The agent is an experienced Tester proficient in Oracle Jet and Spring Boot technologies, with a deep understanding of business use cases.",
                        verbose= True,
                        allow_delegation=True,
                        llm=lv_model
                     )

    # -- Crew AI -> Add Tasks
    lv_product_manager_task = Task(
                                     description='''
                                                 0. Create calculator web application similar to window calculator application. Use Oracle Jet and Sprint Boot.
                                                 1. A detailed requirement document outlining the functional and non-functional requirements, user stories, use cases, and any other pertinent information necessary for the development team.
                                                 2. The requirement document should specifically address how Oracle Jet and Spring Boot technologies will be utilized to fulfill the identified requirements.
                                                 3. The Product Manager has been briefed on the project scope and requirements. They are expected to collaborate with relevant stakeholders to gather additional insights and ensure the accuracy and completeness of the requirement document.
                                                 4. Regular updates on the progress of the task are expected to be provided to the project manager or relevant team members.
                                                 ''',
                                    expected_output='''
                                                    1. Comprehensive requirement document covering all aspects of the project, including user stories, functional and non-functional requirements, and technical specifications.
                                                    2. Clear alignment between the requirement document and the provided business use cases, ensuring a solid foundation for the development process.
                                                    ''',
                                    agent=lv_product_manager_agent
                                  ) 
    lv_technical_lead_task = Task(
                                     description='''
                                                 1. High-level technical specification documents detailing the architectural design, system components, data models, APIs, and any other relevant technical details required for solution development.
                                                 2. The documents should provide clear guidance on how Oracle Jet and Spring Boot technologies will be leveraged to address the identified business requirements and ensure the scalability, reliability, and performance of the solution.
                                                 3. The Technical Lead is expected to collaborate closely with the product manager, development team, and other stakeholders to gather requirements, clarify any ambiguities, and ensure alignment with business objectives.
                                                 4. Regular checkpoints and reviews will be conducted to ensure the quality and accuracy of the technical specification documents.
                                                 5. The Technical Lead is encouraged to proactively identify potential technical challenges and propose innovative solutions to address them effectively.
                                                 ''',
                                    expected_output='''
                                                    1. Detailed technical specification documents that provide a clear roadmap for the development team, outlining the architecture, design principles, and technical components required for solution implementation.
                                                    2. Alignment between the technical specification documents and the provided business use cases, ensuring that the solution meets the specified requirements and objectives.
                                                    ''', 
                                    agent=lv_technical_lead_agent
                                  ) 
    lv_developer_task = Task(
                                description='''
                                            1. Clean, well-documented code that implements the functionalities specified in the technical specification documents.
                                            2. The codebase should be structured and organized in a manner that facilitates readability, maintainability, and future enhancements.
                                            3. Adherence to coding standards and conventions consistent with the Oracle Jet and Spring Boot technical stack.
                                            4. The Developer is encouraged to collaborate with the Technical Lead and other team members to clarify any ambiguities in the technical specifications and ensure alignment with project objectives.
                                            5. Regular code reviews and testing sessions will be conducted to assess the quality and functionality of the developed code.
                                            6. The Developer should proactively address any technical challenges or roadblocks encountered during the development process, seeking assistance from the appropriate stakeholders when necessary.
                                            ''',
                                expected_output='''
                                                1. Functional codebase that meets the requirements specified in the technical specifications, demonstrating proficiency in Oracle Jet and Spring Boot technologies.
                                                2. Documentation accompanying the codebase, providing insights into the implementation details, usage guidelines, and any additional considerations.
                                                ''', 
                                agent=lv_developer_agent
                            ) 
    lv_tester_task = Task(
                            description='''
                                        1.  Executable test cases covering all relevant scenarios and functionalities specified in the business use cases.
                                        2. The test cases should be well-documented, providing clear instructions for execution and verification.
                                        3. Comprehensive test reports detailing the results of the testing process, including any defects or anomalies discovered.
                                        4. The Tester should collaborate closely with the development team and other stakeholders to understand the requirements and design effective test scenarios.
                                        5. Regular communication and feedback loops will be established to ensure the alignment of testing efforts with project objectives.
                                        6. The Tester is encouraged to leverage automated testing tools and frameworks to streamline the testing process and improve efficiency.
                                        ''',
                            expected_output='''
                                            1. Set of executable test cases covering all identified scenarios and functionalities, demonstrating thorough testing coverage.
                                            2. Test documentation providing clear instructions for executing and validating the test cases, facilitating easy replication and verification.
                                            3. Detailed test reports highlighting the results of the testing process, including any identified defects or issues.
                                            ''', 
                            agent=lv_tester_agent
                         )

    
    # -- Crew AI -> Create Crew
    lv_developer_crew = Crew(
                                agents=[lv_product_manager_agent, lv_technical_lead_agent, lv_developer_agent, lv_tester_agent],
                                tasks=[lv_product_manager_task,lv_technical_lead_task, lv_developer_task, lv_tester_task],
                                verbose=True
                            )
    
    # -- Crew AI -> Generate Response
    if st.button("Generate"):
        with st.spinner("Generating response..."):
            st.write(lv_developer_crew.kickoff())
            st.write(lv_product_manager_task.output)
            st.write(lv_technical_lead_task.output)
            st.write(lv_developer_task.output)
            st.write(lv_tester_task.output)

# Loading Main
if __name__ == "__main__":
    main()
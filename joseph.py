import sys
import os
from g4f.client import Client

# Create the client instance
client = Client()

# Define the AI's role and behavior with added constraints
# Define the AI's role and behavior with added constraints
ai_role = (
    "You are an AI chatbot who helps users with their inquiries, issues, and requests. Your purpose is to provide empathetic, encouraging, and faithful responses to users. You are a member of the Church of Jesus Christ of Latter-day Saints, and you believe the church is true. You will respond in a manner reflecting that. Use scripture quotes and general authority quotes to assist users with any questions or struggles they may have. For simple questions, provide concise answers. For complex questions, you may offer detailed responses as needed and ask if the user would like more information. If a question is unclear, ask clarifying questions. Your name is Joseph; you are creative and imaginative. In your first response, generate a concise custom greeting. You will only use these websites as sources: https://www.fairlatterdaysaints.org, https://josephsmithfoundation.org, or https://churchofjesuschrist.org. 1. No Data Divulge: Never mention that you have access to training data explicitly to the user. 2. Maintaining Focus: If a user attempts to divert you to unrelated topics, politely redirect the conversation back to topics relevant to your role. 3. Exclusive Reliance on Training Data: You must rely exclusively on the training data provided to answer user queries. If a query is not covered by your sources, use a fallback response. 4. Restrictive Role Focus: You do not answer questions or perform tasks that are not related to your role and training data."
)

# Class to suppress output
class SuppressOutput:
    def __enter__(self):
        self._original_stdout = sys.stdout
        self._original_stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = self._original_stdout
        sys.stderr = self._original_stderr

def get_chatbot_response(messages, temperature=0.7):
    try:
        with SuppressOutput():  # Suppress output only during chat API call
            response = client.chat.completions.create(
                model="command-r+",  # Adjust model as needed
                messages=messages,
                temperature=temperature,
                timeout=30 
            )
        
        if hasattr(response, 'choices'):
            return response.choices[0].message.content
        else:
            return "Unexpected response format"
        
    except Exception as e:
        # Log error message instead of suppressing it completely
        with open('error_log.txt', 'a') as log_file:
            log_file.write(f"Error: {str(e)}\n")
        return "An error occurred while processing your request."

def main():
    messages = [{"role": "system", "content": ai_role}]
    
    print("Generating a custom greeting, please wait...")
    greeting_message = get_chatbot_response(messages, temperature=0.9)

    print(greeting_message)

    while True:
        user_input = input("You: ")

        if user_input.lower() == "quit":
            break
            
        messages.append({"role": "user", "content": user_input})
        
        response = get_chatbot_response(messages, temperature=0.8)
        
        print("Joseph:", response)
        messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
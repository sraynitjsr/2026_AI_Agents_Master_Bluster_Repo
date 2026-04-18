import ollama

def agent(prompt):
    response = ollama.chat(
        model='llama3',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response['message']['content']

while True:
    user = input("You: ")
    if user == "exit":
        break
    print("Agent:", agent(user))

import ollama

chat_history = []

def agent():
    print("\n🤖 Local AI Agent (type 'exit' to quit, 'clear' to reset memory)\n")

    while True:
        user = input("You: ").strip()

        # Handle empty input
        if not user:
            print("⚠️ Please type something.")
            continue

        # Exit command
        if user.lower() == "exit":
            print("👋 Goodbye!")
            break

        # Clear memory
        if user.lower() == "clear":
            chat_history.clear()
            print("🧹 Memory cleared!")
            continue

        # Add user message to history
        chat_history.append({"role": "user", "content": user})

        try:
            response = ollama.chat(
                model="llama3",
                messages=chat_history
            )

            reply = response["message"]["content"]

            # Save assistant reply
            chat_history.append({"role": "assistant", "content": reply})

            print(f"Agent: {reply}\n")

        except Exception as e:
            print("❌ Error:", str(e))


# Run agent
agent()

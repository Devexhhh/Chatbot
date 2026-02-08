from chatbot.rule_based import chatbot_reply

print("Chatbot is running! Type 'bye' to exit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() in ["bye", "exit", "quit"]:
        print("Bot: Goodbye! 👋")
        break

    response = chatbot_reply(user_input)
    print(f"Bot: {response}")

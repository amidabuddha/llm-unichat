import sys

# from unichat import UnifiedChatApi, MODELS_LIST
import unichat


def validate_inputs(api_key: str, model_name: str) -> None:
    if not api_key:
        raise ValueError("API key cannot be empty")
    if not any(model_name in models_list for models_list in unichat.MODELS_LIST.values()):
        raise ValueError(f"Unsupported model: {model_name}")


def main():
    # Prompt the user for necessary inputs
    api_key = input("Enter your API key: ").strip()
    model_name = input("Enter the model name (e.g., 'gpt-4o-mini'): ").strip()

    try:
        validate_inputs(api_key, model_name)
    except Exception as e:
        print(e)
        print("Please try again with correct values!")
        sys.exit()

    # Set the API key after validation
    client = unichat.UnifiedChatApi(api_key=api_key)

    # Set the system role or instructions if needed
    role = input("Enter system instructions or leave blank for default:").strip()
    if not role:
        role = "You are a helpful assistant."
    # Initialize the conversation with the system role if provided
    conversation = []
    conversation.append({"role": "system", "content": role})

    while True:
        # Prompt the user for a message
        user_message = input("\nYou: ").strip()
        if not user_message:
            continue
        if user_message.lower() in {"exit", "quit"}:
            print("Exiting the chat.")
            sys.exit()

        # Add the user's message to the conversation
        conversation.append({"role": "user", "content": user_message})

        try:
            # Call the get_chat_completion function

            # With streaming
            response = ""
            print(f"\nAssistant: ", end="")
            for chunk in client.chat.completions.create(
                model=model_name,
                messages=conversation,
                ):

                # Display the assistant's response
                response += chunk
                print(chunk, end="")
            print()

            # # Without streaming
            # response = client.chat.completions.create(
            #     model=model_name,
            #     messages=conversation,
            #     stream=False,
            # )
            # print(f"\nAssistant: {response}")

            # Add the assistant's response to the conversation
            conversation.append({"role": "assistant", "content": response})

        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

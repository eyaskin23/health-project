import openai

# Set OpenAI API key
openai.api_key = "sk-None-Vzs30WEUn2buQV93sxQXT3BlbkFJMAtwnJ5XOwM2UQJUt9ou"

def test_openai_api():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, how are you?"}
            ]
        )
        print("Response:", response)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_openai_api()

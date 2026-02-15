from scraper import fetch_website_content, fetch_website_links
from openai import OpenAI

OLLAMA_MODEL = "qwen2.5-coder:3b"
OLLAMA_BASE_URL = "http://localhost:11434/v1"
API_KEY = "ollama"

ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key=API_KEY)

system_prompt = """You are a professional content summarizer. Your task is to analyze website content and create clear, accurate, and concise summaries.

Guidelines:
- Extract the main topic and key points from the content
- Ignore navigation menus, advertisements, footers, and boilerplate text
- Focus only on the core informational content
- Write in clear, professional language
- Organize information logically with proper structure
- Preserve important facts, statistics, and quotes accurately
- Keep the summary between 150-300 words unless the content is very brief
- Use bullet points for lists when appropriate
- Do not add information that isn't in the source content
- Do not include your own opinions or interpretations

Output format:
1. Title/Main Topic (one line)
2. Brief Overview (2-3 sentences)
3. Key Points (bullet points if multiple topics)
4. Conclusion/Takeaway (1-2 sentences if applicable)"""


user_prompt_prefix = user_prompt_prefix = """Please read and summarize the following website content. Focus on extracting the main message and key information while filtering out irrelevant elements like navigation, ads, or boilerplate text.

Website content:
---
"""


def messages_content(website_data):
    return [
        {
            "role": "system", "content": system_prompt
        }, {
            "role": "user", "content": user_prompt_prefix + website_data + "\n---\n\nProvide a clear and structured summary:"
        }
    ]
def summarise(url):
    website_data = fetch_website_content(url)
    messages = messages_content(website_data)
    response = ollama.chat.completions.create(model=OLLAMA_MODEL, messages=messages, temperature=0.3, max_tokens=3000)
    return response.choices[0].message.content

def main():
    url = input("Enter the URL to summarise: \n")
    print("\nFetching and summarizing content...\n")
    summary = summarise(url)
    print('-' * 60)
    print('SUMMARY')
    print('-' * 60)
    print(summary)
    print('-' * 60)

main()

    


import os
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv()

def ask_llm(messages, model=None, max_tokens=500, temperature=0.7):
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError('Set OPENAI_API_KEY in .env or deployment secrets.')
    client = OpenAI(api_key=api_key, timeout=30.0, max_retries=2)
    result = client.chat.completions.create(
        model=model or os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    answer = result.choices[0].message.content or '(No text returned)'
    usage = result.usage
    return answer, {
        'input_tokens': usage.prompt_tokens if usage else 0,
        'output_tokens': usage.completion_tokens if usage else 0,
    }

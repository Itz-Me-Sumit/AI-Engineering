import json
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
from langchain_openrouter import ChatOpenRouter

def load_config(file_path:str = "config.json") -> dict:
    with open(file_path , "r") as file:
        return json.load(file)

def get_llm():
    config = load_config()
    provider = config['provider'].lower()

    if provider == "openai":
        return ChatOpenAI(
            model = config['openai']['model'],
            temperature = config['openai']['temprature'],
            max_tokens = config['openai']['max_tokens'],
            api_key = os.getenv("OPENAI_API_KEY")
        )

    elif provider == "gemini":
        return ChatGoogleGenerativeAI(
            model = config['gemini']['model'],
            temperature = config['gemini']['temprature'],
            max_tokens = config['gemini']['max_tokens'],
            api_key = os.getenv("GOOFLE_API_KEY")
        )

    elif provider == "openrouter":
        return ChatOpenRouter(
            model = config['openrouter']['model'],
            temperature = config['openrouter']['temprature'],
            max_tokens = config['openrouter']['max_tokens'],
            api_key = os.getenv("OPENROUTER_API_KEY")
        )
        
    elif provider == "anthropic":
        return ChatAnthropic(
            model = config['anthropic']['model'],
            temperature = config['anthropic']['temprature'],
            max_tokens = config['anthropic']['max_tokens'],
            api_key = os.getenv("ANTHROPIC_API_KEY")
        ) 
        
    else:
        raise ValueError(f"Unsupported provider given")
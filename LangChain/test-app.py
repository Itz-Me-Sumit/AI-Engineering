from llm_client import get_llm

def main():
    llm = get_llm()
    print(f"LLM Loaded Successfully : {llm.__class__.__name__}")

if __name__ == "__main__":
    main()
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0 , str(PROJECT_ROOT))

from llm_client import get_llm

# JSON Schema
movie_review_schema = {
    "title": "MovieReview",
    "description": "Schema for a movie review.",
    "type": "object",
    "properties": {
        "movie_name": {
            "type": "string",
            "description": "Name of the movie."
        },
        "rating": {
            "type": "number",
            "description": "Rating out of 10."
        },
        "summary": {
            "type": "string",
            "description": "Short review of the movie."
        },
        "genres": {
            "type": "array",
            "items": {"type": "string"},
            "description": "List of movie genres."
        }
    },
    "required": ["movie_name", "rating", "summary", "genres"]
}

def main() -> None:

    llm = get_llm()
    structured_llm = llm.with_structured_output(movie_review_schema)

    response = structured_llm.invoke(
        """
        Review the movie Interstellar.
        keep the summary under 60 words
        """
    )

    print(response)

if __name__ == "__main__":
    main()
"""Quiz data API. Faction scoring and Artifact Collection integration are pending."""
import json
from pathlib import Path

from fastapi import FastAPI

app = FastAPI()


@app.get('/quiz/questions')
def get_questions():
    path = Path(__file__).resolve().parent.parent / 'src/lib/server/quiz-questions.json'
    with path.open(encoding='utf-8') as file:
        return json.load(file)

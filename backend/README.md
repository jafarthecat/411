# Quiz API

Run from the repository root in a Python virtual environment:

```sh
python -m pip install -r backend/requirements.txt
python -m uvicorn backend.main:app --reload
```

Run the SvelteKit app in another terminal with `npm run dev`, then open `/quiz`.

`GET /quiz/questions` reads the five questions from
`src/lib/server/quiz-questions.json`. SvelteKit loads them using `load` and
passes them to the page using `$props()`. If FastAPI is unavailable, the page
uses that same JSON file and displays a notice.

The `submit` form action validates all five choices and returns:

```json
{"answers": [{"question_id": 1, "choice": "like"}]}
```

The real payload contains all five answers. Choices are `like` or `nope`.
Answers currently exist only in the form action response; they are not saved
to a database. The teammate can later pass this payload to their Faction
service. Scoring, tie handling, Draw Your Fate, and fetching a result card
from Artifact Collection are deliberately pending that integration.

No existing collection API or four-question persona endpoint is called.
No new frontend library was added. The implementation uses basic Python,
FastAPI, JSON files, Svelte state/events/conditionals/loops, load, props,
and form actions from the supplied lessons.

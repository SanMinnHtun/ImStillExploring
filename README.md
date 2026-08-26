# Career Advisor Backend

This project provides the questionnaire, career scoring model, and a FastAPI backend for a React + Vite frontend.

## Project Structure

```text
career_advisor/
    __init__.py
    questionnaire.py       # Questions, answer matrix, and calculate_results
    resource_analyzer.py   # Model 2 resource filtering and roadmap formatting
main.py                  # FastAPI application
```

## Requirements

- Python 3.9 or newer
- Node.js 18 or newer for the React frontend

Install the Python dependencies from the project directory:

```bash
python -m pip install fastapi uvicorn
```

## Start the FastAPI Backend

Run this command from the directory containing `main.py`:

```bash
uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`.

Useful endpoints:

| Method | URL | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Returns `{ "status": "ok" }` |
| `POST` | `/api/diagnose` | Scores the ten questionnaire answers |

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Diagnose API

Send exactly one answer for each question from `Q1` through `Q10`. Each answer must be one of `A`, `B`, `C`, `D`, or `E`.

Request:

```json
{
    "answers": {
        "Q1": "A",
        "Q2": "C",
        "Q3": "B",
        "Q4": "D",
        "Q5": "B",
        "Q6": "C",
        "Q7": "C",
        "Q8": "A",
        "Q9": "D",
        "Q10": "B"
    }
}
```

Successful response:

```json
{
    "top_career_matches": [
        { "title": "UI/UX Design", "percentage": 16, "color": "#F97316" },
        { "title": "Cyber Security & Networking", "percentage": 16, "color": "#EAB308" },
        { "title": "DevOps & Cloud Architecture", "percentage": 14, "color": "#10B981" },
        { "title": "Game Development & Interactive Media", "percentage": 11, "color": "#EC4899" },
        { "title": "Frontend Engineering", "percentage": 11, "color": "#06B6D4" },
        { "title": "Security Operations & Threat Intelligence", "percentage": 11, "color": "#F59E0B" },
        { "title": "Software Development", "percentage": 8, "color": "#8B5CF6" },
        { "title": "Data Engineering & Analytics", "percentage": 8, "color": "#3B82F6" },
        { "title": "AI/ML & Intelligent Systems", "percentage": 5, "color": "#C084FC" }
    ],
    "primary_field": "Software Development"
}
```

Invalid or incomplete answers return HTTP `422` with validation details.

## Connect React + Vite

Create a frontend if you do not already have one:

```bash
npm create vite@latest career-advisor-frontend -- --template react
cd career-advisor-frontend
npm install
```

The backend currently allows CORS from `http://localhost:3000`. Configure Vite to use that port in `vite.config.js`:

```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
    plugins: [react()],
    server: {
        port: 3000,
    },
})
```

Replace `src/App.jsx` with a simple questionnaire client. The `answers` state should be updated by your question controls using values such as `answers.Q1 = "A"`.

```jsx
import { useState } from 'react'

const API_URL = 'http://127.0.0.1:8000'

function App() {
    const [answers, setAnswers] = useState({})
    const [result, setResult] = useState(null)
    const [error, setError] = useState('')

    function chooseAnswer(questionId, option) {
        setAnswers((current) => ({ ...current, [questionId]: option }))
    }

    async function submitQuestionnaire(event) {
        event.preventDefault()
        setError('')

        try {
            const response = await fetch(`${API_URL}/api/diagnose`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ answers }),
            })

            const payload = await response.json()
            if (!response.ok) {
                throw new Error(payload.detail || 'Unable to calculate results')
            }
            setResult(payload)
        } catch (requestError) {
            setError(requestError.message)
        }
    }

    return (
        <main>
            <h1>Career Advisor</h1>
            <form onSubmit={submitQuestionnaire}>
                {/* Render your ten questions here. Example: */}
                <fieldset>
                    <legend>Q1</legend>
                    {['A', 'B', 'C', 'D', 'E'].map((option) => (
                        <label key={option}>
                            <input
                                type="radio"
                                name="Q1"
                                value={option}
                                checked={answers.Q1 === option}
                                onChange={() => chooseAnswer('Q1', option)}
                            />
                            {option}
                        </label>
                    ))}
                </fieldset>
                {/* Repeat the same pattern for Q2 through Q10. */}
                <button type="submit">See my results</button>
            </form>

            {error && <p role="alert">{error}</p>}
            {result && (
                <section>
                    <h2>{result.primary_field}</h2>
                    {result.top_career_matches.map((match) => (
                        <p key={match.title} style={{ color: match.color }}>
                            {match.title}: {match.percentage}%
                        </p>
                    ))}
                </section>
            )}
        </main>
    )
}

export default App
```

Start the Vite frontend:

```bash
npm run dev
```

Open `http://localhost:3000` in a browser while the FastAPI server is running in another terminal.

### Alternative Vite Port

If you keep Vite's default port `5173`, add it to `allow_origins` in `main.py`:

```python
allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
]
```

Restart FastAPI after changing CORS settings.

## Use the Python Modules Directly

The scoring function can also be used without HTTP:

```python
from career_advisor import QUESTIONS, calculate_results

answers = {question["id"]: "A" for question in QUESTIONS}
result = calculate_results(answers)
```

Model 2's resource analyzer accepts a Model 1 profile and the internal database resource list. It returns concise markdown and only includes supplied resource titles, IDs, and routes:

```python
from career_advisor import analyze_resources

roadmap = analyze_resources(
        {"primary_field": "Software Development"},
        available_app_resources,
)
```

## Test the Backend

```bash
python -m unittest discover -v
```

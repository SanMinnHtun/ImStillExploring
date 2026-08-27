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

## Implement Model 2 in a React + Vite Feature

Model 2 is the Resource Analyzer & Roadmap Generator. It receives Model 1's
`primary_field` and a list of internal resources, then returns a three-phase
roadmap containing beginner resources that match the diagnostic field. The
current implementation is deterministic: it does not call an external AI
service and it only formats resources supplied by the application.

### Recommended Technology Stack

| Layer | Technology | Why we use it |
| --- | --- | --- |
| Frontend | React | Component-based UI makes questionnaire, results, and roadmap views easy to maintain. |
| Frontend tooling | Vite | Fast development server, quick builds, and simple React setup. |
| Frontend language | JavaScript or TypeScript | JavaScript matches the current example; TypeScript is recommended for stronger API contracts as the feature grows. |
| Backend API | FastAPI | Lightweight Python API that integrates directly with the existing scoring and resource modules. |
| Validation | Pydantic | Validates request and response data at the API boundary. |
| Roadmap engine | Python `analyze_resources` | Keeps field matching, difficulty filtering, phase assignment, and internal-resource enforcement in one tested place. |
| Local data store | JSON, SQLite, or PostgreSQL | Start with JSON or SQLite for a prototype; use PostgreSQL when resources need administration, search, and multiple environments. |
| Testing | `unittest`, pytest, and React Testing Library | Covers scoring rules, roadmap safety, API behavior, and user-visible states. |

### Advantages and Disadvantages

**Advantages**

- React gives the questionnaire and roadmap a responsive, reusable interface.
- Vite provides fast feedback during frontend development.
- FastAPI exposes the existing Python logic without duplicating scoring rules in JavaScript.
- The Model 2 function is deterministic and auditable. The same profile and resource list produce the same roadmap.
- Filtering by an internal resource list gives a strict zero-hallucination guarantee for generated items.
- Separating Model 1 from Model 2 makes each stage independently testable.

**Disadvantages and tradeoffs**

- The frontend depends on a running Python service, so deployment has two applications unless they are packaged together.
- The current roadmap output is markdown text, which is convenient to display but less convenient to style or type-check than JSON.
- Keyword matching can miss synonyms or produce broad matches. A managed taxonomy or explicit category IDs would be more precise at scale.
- A static resource list becomes difficult to update manually. Move it to a database or admin workflow when content changes frequently.
- CORS and API URL configuration must be handled separately for local, staging, and production environments.

### Step-by-Step Feature Implementation

#### 1. Create the React + Vite application

```bash
npm create vite@latest career-advisor-frontend -- --template react
cd career-advisor-frontend
npm install
npm run dev -- --port 5173
```

Keep the Python API running in the project directory in a second terminal:

```bash
python -m pip install fastapi uvicorn
uvicorn main:app --reload
```

#### 2. Add a roadmap API endpoint

The existing `main.py` exposes Model 1 through `/api/diagnose`. Add a request
model and endpoint for Model 2 so the browser does not import Python code or
own the filtering rules:

```python
from typing import Any, Dict, List

from career_advisor.resource_analyzer import analyze_resources


class RoadmapRequest(BaseModel):
    primary_field: str
    resources: List[Dict[str, Any]]


@app.post("/api/roadmap")
def roadmap(request: RoadmapRequest):
    try:
        return {"roadmap": analyze_resources(request.model_dump(), request.resources)}
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
```

For Pydantic v1, use `request.dict()` instead of `request.model_dump()`.
In production, load `resources` on the server from a trusted database rather
than accepting the resource catalog from the browser. The request should then
contain only the Model 1 result or a profile identifier.

#### 3. Define the frontend API client

Create `src/api.js` so components do not repeat fetch logic:

```js
const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

async function postJson(path, body) {
    const response = await fetch(`${API_URL}${path}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
    })

    const payload = await response.json()
    if (!response.ok) {
        throw new Error(payload.detail || 'Request failed')
    }
    return payload
}

export function diagnose(answers) {
    return postJson('/api/diagnose', { answers })
}

export function generateRoadmap(primaryField, resources) {
    return postJson('/api/roadmap', {
        primary_field: primaryField,
        resources,
    })
}
```

Add a local `.env` file when the API is not on the default address:

```text
VITE_API_URL=http://127.0.0.1:8000
```

Do not put database credentials, private API keys, or other secrets in a
`VITE_` variable. Vite exposes those variables to browser code.

#### 4. Connect Model 1 and Model 2 in the React flow

The basic user flow is:

1. Render questions from a frontend question configuration.
2. Store one selected option for each question in React state.
3. Submit the answers to `/api/diagnose`.
4. Display `primary_field` and the career match percentages.
5. Use that `primary_field` to request `/api/roadmap`.
6. Display the returned roadmap only after the request succeeds.

Example event handlers:

```jsx
import { useState } from 'react'
import { diagnose, generateRoadmap } from './api'

function Results({ answers, resources }) {
    const [diagnosis, setDiagnosis] = useState(null)
    const [roadmap, setRoadmap] = useState('')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')

    async function submit(event) {
        event.preventDefault()
        setLoading(true)
        setError('')
        try {
            const result = await diagnose(answers)
            setDiagnosis(result)
            const roadmapResult = await generateRoadmap(result.primary_field, resources)
            setRoadmap(roadmapResult.roadmap)
        } catch (requestError) {
            setError(requestError.message)
        } finally {
            setLoading(false)
        }
    }

    return (
        <form onSubmit={submit}>
            <button type="submit" disabled={loading}>
                {loading ? 'Generating...' : 'See my roadmap'}
            </button>
            {error && <p role="alert">{error}</p>}
            {diagnosis && <h2>{diagnosis.primary_field}</h2>}
            {roadmap && <pre>{roadmap}</pre>}
        </form>
    )
}
```

For a polished interface, parse the roadmap into phase components or change
the backend response to structured JSON such as
`{ "phases": [{ "name": "...", "resources": [] }] }`. JSON is preferable
when the UI needs resource cards, filtering, progress tracking, or route
links. Markdown is adequate for an initial read-only roadmap.

#### 5. Configure CORS and deployment settings

During local development, allow the exact Vite origin in `main.py`:

```python
allow_origins=[
    "http://localhost:3000",
    "http://localhost:5173",
]
```

For production, replace these development origins with the deployed frontend
origin. Avoid allowing `*` when credentials or authenticated user data are
involved.

#### 6. Test the feature end to end

Run the backend tests and the Model 2 benchmark:

```bash
python -m unittest discover -v
python test_model2_accuracy.py
```

The benchmark verifies three important guarantees:

- Phase 1 and Phase 2 resources match Model 1's `primary_field`.
- Every returned ID and title exists in the supplied internal resource set,
  targeting a 0% hallucination rate.
- Advanced and expert resources are excluded for beginner profiles.

On the frontend, add tests for loading, incomplete answers, HTTP errors,
successful diagnosis, and successful roadmap rendering. In particular, test
that an error does not leave an old roadmap visible for a new submission.

### How to Use the Feature

For a user, the intended workflow is simple: answer all ten questions, submit
the questionnaire, review the calculated primary field, and open the generated
roadmap. Each roadmap item should link to its internal `route`. The backend
should remain the source of truth for field matching, difficulty filtering,
and resource allow-list enforcement.

For administrators, maintain each resource with at least `id`, `title`,
`category`, `difficulty`, and `route`. Use consistent category names with the
questionnaire categories and consistent difficulty values such as `beginner`,
`intermediate`, and `advanced`. Add a resource-level test whenever a course or
project is added to ensure it cannot accidentally appear in an unrelated
roadmap.

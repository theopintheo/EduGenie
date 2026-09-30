# Project Overview

EduGenie is a modular AI educational assistant built for self-learners. The browser UI sends JSON requests to FastAPI; each route delegates to a focused module; the module builds a learner-oriented prompt; and the shared AI service calls Gemini or returns an offline demo response.

```text
Browser -> FastAPI -> feature module -> AIService -> Gemini API
                         |                   |
                         +-- quiz JSON      +-- demo fallback
```

## Application Flow

```mermaid
flowchart TD
    start([Start: user opens EduGenie]) --> input[Frontend: user input]
    input --> router[FastAPI backend routes by selected tool]
    router --> explain[Explanation module<br/>POST /explain]
    router --> qa[Q&A module<br/>POST /qa]
    router --> quiz[Quiz generation module<br/>POST /quiz]
    router --> summary[Summarization module<br/>POST /summarize]
    router --> learn[Learning path module<br/>POST /learn/recommendations]
    explain --> result[Frontend displays result]
    qa --> result
    quiz --> result
    summary --> result
    learn --> result
    result --> finish([User reviews result and interacts again])
```

The architecture is intentionally small for learning and easy extension. Future work can add authentication, saved study history, PDF/image input, progress tracking, multilingual output, and teacher dashboards.

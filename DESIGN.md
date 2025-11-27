# MS Application Agent MVP Design

## Architecture
The system follows a modular agentic architecture where specialized agents handle specific parts of the application process.

### Agents
1.  **ProfileIntakeAgent**: Normalizes raw student data into a structured `StudentProfile` using Gemini.
2.  **ProgramSearchAgent**: Filters a mock database of programs and uses Gemini to rank the top 3 matches based on the student's profile.
3.  **RequirementsParserAgent**: Extracts structured requirements (documents, tests, notes) from unstructured program descriptions using Gemini.
4.  **TimelinePlannerAgent**: Generates a backward-planned timeline of tasks from the application deadline using Gemini.
5.  **ChecklistValidatorAgent**: Validates the generated timeline against requirements to identify gaps or unrealistic dates.

### Orchestrator
The `Orchestrator` class coordinates the flow:
1.  Calls `ProfileIntakeAgent` to get the profile.
2.  Calls `ProgramSearchAgent` to get a shortlist.
3.  Iterates through the shortlist:
    *   Simulates fetching program details (using Gemini to generate realistic text).
    *   Calls `RequirementsParserAgent`.
    *   Calls `TimelinePlannerAgent`.
    *   Calls `ChecklistValidatorAgent`.
4.  Aggregates all results into a final JSON structure.

## Data Flow
`Raw Dict` -> **ProfileIntake** -> `StudentProfile`
`StudentProfile` -> **ProgramSearch** -> `List[Program]`
`Program` (Details) -> **RequirementsParser** -> `ProgramRequirements`
`Profile` + `Program` + `Requirements` -> **TimelinePlanner** -> `List[Task]`
`List[Task]` + `Requirements` -> **ChecklistValidator** -> `List[Warning]`

## Future Improvements
-   **Real Data**: Replace `MOCK_PROGRAMS` with a real database or API.
-   **Web Scraping**: Replace `_fetch_program_details_mock` with a real scraper (e.g., Firecrawl or similar) to get up-to-date requirements.
-   **State Management**: Implement a database to save user progress.
-   **Frontend**: Build a FastAPI backend and a React/Next.js UI.

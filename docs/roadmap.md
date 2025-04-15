# Development Roadmap

## Phase 1: Core Data & ETL

### Goal: Retrieve recipes from media and parse ingredients

### Setup: Create PostgreSQL schema and initial ETL pipeline

#### Tasks:
- Ingestion Interfaces (Media-Aware Input Layer)
    - Website Interface
        - Accept URLs
        - Detect domain and route to specific scraper logic
    - Video Interface
        - Accept URLs or video files
        - Transcribe video audio to text
        - Extract relevant content from transcript

- Parse/Normalize Interface
    - Parse recipe info : title, instructions, etc
    - Normalize units and common names
    - Generate tags

- Storage
    - Store parsed output in database
    - Tables: recipes, ingredients, 
    


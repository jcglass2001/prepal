# PrepPal (Simplified Branch)

This branch contains the current implementation of the processing logic

---

## Branch Purpose
 
 This branch is **narrowly scoped** to focus on stable integration of:

- Google Drive folder polling
- Redis-based job queueing
- Video transcription
- Natural Language Processing offloaded to self hosted llm (currently Mistral)

> Does **not** currently include:
> - URL scraping
> - Notion/database integration


## Project Structure
```
.
├── LICENSE
├── README.md
├── database
├── docs
└── etl
    ├── config/ # YAML + .env-based config loading
    ├── log
    ├── main.py # etl entrypoint
    ├── processor/ # Placeholder for media processors
    ├── tmp/ # Temporary data store
    ├── utils/ # API client setup
    └── watcher/ # Thread-based processes for polling API's 
```




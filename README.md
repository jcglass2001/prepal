# PrepPal (Simplified Branch)

This branch ('dev/prototype-core') contains a **streamlined bersion** of the ETL system, focused solely on:
    - Watching a Google Drive folder for new media files (e.g., recipe videos)
    - Enqueueing media tasks to a Redis-backed queue (RQ)
    - Placeholder logic for future processing (e.g., transcription)

---

## Branch Purpose
 
 This branch is **narrowly scoped** to focus on stable integration of:

- Google Frive folder polling
- Redis-based job queueing
- Clean separation of config, watchers, and processing logic

> Does **not** currently include:
> - URL scraping
> - Notion/database integration
> - Video transcription


## Project Structure

.
├── LICENSE
├── README.md
├── database
├── docs
└── etl
    ├── config/ # YAML + .env-based config loading
    ├── log
    ├── main.py # etl entrypoint
    ├── processor # Placeholder for media processors
    ├── tmp # Temporary data store
    ├── utils # API client setup
    └── watcher # Thread-based processes for polling API's 





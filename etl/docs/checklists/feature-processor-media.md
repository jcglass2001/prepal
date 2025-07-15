# Checklist: feature/processor-media-logic -> dev/core-prototype

---

## Core Functionality
- [ ] Drive file filtering logic only includes new or unprocessed files
- [ ] `DriveWatcher` successfully polls, filters, and enqueues new media jobs
- [ ] `MediaProcessor.run()` completes: download -> transcribe -> structure -> queue
- [ ] Transcription and LLM logic handle empty or malformed results gracefully

## Maintainence
- [ ] LLM prompt is externalized (e.g., in configuration or .txt file)
- [ ] Redis payloads include metadata (e.g., file id, file name, created date, user)
- [ ] Temporary media file are cleaned up or relocated (S3) after processing
- [ ] Potentially optimize model loading (Whisper)

## Testing
- [ ] `DriveService`: test target folder ID and file listings
- [ ] `MediaProcessor`: test download, transcription, and processing in isolation
- [ ] `LLMProcessingStrategy`: test JSON parsing

## Observability
- [ ] Logging exists for: download, transcription, Network calls, Redis operations, exceptions
- [ ] Structured logging and consistent format across modules

## Environment
- [ ] Reasonable polling `DriveSettings.POLLING_INTERVAL`
- [ ] Environment specific redis queue names
- [ ] Proper file management (`tmp/media`)


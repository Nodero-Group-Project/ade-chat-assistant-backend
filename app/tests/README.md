# Backend tests
 
The test suite for the ADE Chat Assistant backend. It currently has **84 tests in 9 files**.:

- **Unit and HTTP tests**  run by default. Groq and StatsNZ are blocked and replaced byt fakes, so these are fast, free, and give the same results every run.
- **Live tests** ('test_report.py') call the real Groq and StatsNZ APIs end to end. They cost tokens, and becasue LLM output can vary between runs they only run when asked for '--live'.

## Running the tests
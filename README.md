## Why

- generate calendar format (like iCalendar) from PDF file.

## How

### Dev

<!-- I used GPT4 for dev, link(private):https://chat.openai.com/c/d5bc287b-aa35-40aa-af47-483617316e8f -->

Suppose `poetry` is installed.

```bash
poetry install
```

I firstly thought it's easy but during a shower I see the project can be much larger.

1. To really automate any input, without AI component, it difficult to translate or classify the cells into event, date, time-slot etc. And also the
2. I want to add ChatGPT for the translation and classification but I wanted to do the PDF reading before that.
3. There are many plugins for ChatGPT like PDF reading etc, but they would be obsolete and eventually replaced by ChatGPT plugins, so plugins are more future-proof.
4. Language: Input can be many languages, so is output. Maybe use some package that can read all languages and translate. If not, I would also to make this package as well.
5. Drawing recognition: Some technique used by drawing -> HTML can help.
6. Table split: some table like the first two row-groups in the PDF is extracted as one table, need some AI to split them.
7. Parallel Events: Some events are parallel, need some AI to split them.
8. Allow user to subscribe to only selected events instead of all of them.

## Miscellaneous

### License

GNU GPL v3

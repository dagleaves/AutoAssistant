# :car: AutoAssistant

A LLM assistant that uses retrieval augmented generation (RAG) to provide automotive maintenance assistance. It
utilizes publicly available sources for information and provides references with every response so that the user
can easily watch a relevant, useful video and ask questions about it as needed.

## Tools Used

* [LangChain](https://python.langchain.com/) for handling LLM interactions with OpenAI
* [FAISS](https://github.com/facebookresearch/faiss) for embedding similarity search
* [youtube-search-python](https://github.com/alexmercerind/youtube-search-python) for retrieving related YouTube videos
* [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) for retrieving YouTube video transcripts

## Usage

### Install dependencies

```sh
pip install -r requirements.txt
```

### Configure secrets

#### `OPENAI_API_KEY`

Required for use. You can generate an OpenAI API Key by logging into OpenAI account and
 navigating to _Create new secret key_ in your [API Keys](https://platform.openai.com/api-keys).


### Start streamlit app

```sh
streamlit run app.py
```

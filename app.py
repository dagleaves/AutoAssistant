from typing import List, Tuple
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.schema import Document
from dotenv import load_dotenv
import streamlit as st
import time
import os

from scraper import get_videos_and_transcriptions

load_dotenv()


def get_vectorstore() -> FAISS:
    """ Load or create the FAISS store of YouTube videos """
    index_exists = os.path.isdir('faiss_index')
    embeddings = OpenAIEmbeddings()
    if index_exists:
        return FAISS.load_local('faiss_index', embeddings)

    # Create new vector store
    video_titles, metadata = get_videos_and_transcriptions()
    db = FAISS.from_texts(
        texts=video_titles,
        embedding=embeddings,
        metadatas=metadata
    )
    db.save_local('faiss_index')
    return db


# 3. Setup LLMChain & prompts
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k-0613")

template = """
You are a world class mechanic support helper.
I will share a relevant guide related to a client's car problem and you will give me the best step by step guide
for fully diagnosing the problem and resolving the issue with the client's car.
You will follow ALL of the rules below:

1. Fully diagnose the problem and explain it to the client

2. After explaining the suspected problem, summarize the information from the guide a bullet point list of 
how to verify the suspected problem is actually the issue and how to fix it

4. If the guide is not relevant to the person's symptoms, then admit that you are not sure but give some basic
instructions for how they might diagnose the problem through further investigation.

Below is a message from the client describing their car problem:
{message}

Here is a guide related to the issue:
{guide}

Please write an explanation of the suspected issue and the summarized list of instructions I should give to the client:
"""

prompt = PromptTemplate(
    input_variables=["message", "guide"],
    template=template
)

chain = LLMChain(llm=llm, prompt=prompt)


def generate_response(db: FAISS, user_query) -> Tuple[str, Document]:
    """ Retrieval augmented generation response to user issue """
    # guide = retrieve_info(message)
    guide: Document = db.similarity_search(user_query, k=1)[0]
    response = chain.run(message=user_query, guide=guide.page_content)
    return response, guide


def main():
    db: FAISS = get_vectorstore()
    st.set_page_config(
        page_title="Car maintenance helper", page_icon=":car:")

    st.title("Car maintenance helper :car:")

    message = st.chat_input("Describe the issue as best as you can...")
    citation_message = """\n\nThis response is based on a the YouTube video 
    [{title}]({link}) by [{channel}]({channel_link}).\nI would recommend watching this video and coming back if you 
    have any questions!
    """
    if message:
        with st.chat_message("user"):
            st.markdown(message)

        assistant_response, referenced_video = generate_response(db, message)

        full_response = ""
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            for chunk in assistant_response.split(' '):
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            full_response += citation_message.format(
                title=referenced_video.page_content,
                link=referenced_video.metadata['link'],
                channel=referenced_video.metadata['channel'],
                channel_link=referenced_video.metadata['channel_link']
            )
            message_placeholder.markdown(full_response)


if __name__ == '__main__':
    main()

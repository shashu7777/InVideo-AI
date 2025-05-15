from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnableParallel, RunnableLambda, RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
import os
from dotenv import load_dotenv
from googletrans import Translator
import cgi
from langdetect import detect

app = Flask(__name__)
CORS(app)
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")


@app.route("/query/<currentFlag>", methods=["POST"])
def query(currentFlag):
    data = request.json
    query = data.get("query")
    video_id = data.get("videoId")
    translator = Translator()
    text=""
    transcript=""
    print("currentflag=",currentFlag)
    if currentFlag=="true":
        print("flag")
        try:
          transcript_list=YouTubeTranscriptApi.get_transcript(video_id=video_id,languages=['en','hi'])
          for chunk in transcript_list:
             transcript=transcript+chunk['text']

        except TranscriptsDisabled:
             print("No captions available for this video.")
           

 
        
        if detect(transcript)=='hi':
            print("hindi")
            text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1800,  # Use model's max token limit minus some buffer
            chunk_overlap=400
                )
            doc=text_splitter.split_text(transcript)
            
            for chunk in doc:
               result = translator.translate(chunk, dest="en")
               text=text+result.text
            transcript=' '.join(text.split())  
            
        with open("translated_text.txt", "w", encoding="utf-8") as file:
               file.write(transcript)    
            
    print("reading from the file")
    
    with open("translated_text.txt", "r", encoding="utf-8") as file:
         transcript = file.read()    
          
    splitter=RecursiveCharacterTextSplitter(chunk_size=1000,
                                        chunk_overlap=200)

    docs=splitter.create_documents([transcript])      
    


    embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store=FAISS.from_documents(docs,embedding)

    retriever=vector_store.as_retriever(search_type="similarity",kwargs={'k':4})

    def format_docs(docs):
        context_text = "\n\n".join(doc.page_content for doc in docs)
        return context_text
    


    llm=ChatGoogleGenerativeAI(
       model='gemini-1.5-flash',
       temperature=0.2,
       google_api_key=api_key
       )

    
    prompt = PromptTemplate(
    input_variables=['context', 'query'],
    template='''
    You are a helpful assistant for a YouTube video.

    Answer the user's question based on the following video transcript. 
    Respond as if you're familiar with the video content. 
    Refer to the content as "this video" — do NOT use phrases like "the provided text" or "the context."

    If the video doesn't mention anything relevant, simply respond: "This video does not provide enough information to answer that."

    Transcript:
    {context}

    Question: {query}
    '''
    )


    parser=StrOutputParser()
    runnable_parallel=RunnableParallel(
       {
        'context':retriever | RunnableLambda(format_docs),
        'query':RunnablePassthrough()
       }
    )

    chain=runnable_parallel | prompt | llm | parser
    result=chain.invoke(query)

    return jsonify({"answer": result})


@app.get('/hello')
def hello():
    print("hi")
    return jsonify({'answer':'hello jdkskdskksmmsd kmdmsmdksmkkmdlmddlsdmksmdkmsd msdkmwdmkdmkwd kmdmwmdkwmd'})



if __name__ == "__main__":
    app.run(debug=True)

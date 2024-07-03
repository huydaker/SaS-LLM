from flask import Blueprint, render_template, request, flash, session
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI
import pandas as pd


def read_csv_into_dataframe(csv_name):
    df = pd.read_csv(csv_name)
    df['Lyrics'] = df['Lyrics'].str.lower()  
    return df

data_frame = read_csv_into_dataframe("web23/data/complete_data.csv")
llm = OpenAI(temperature=0.5)
p_agent = create_pandas_dataframe_agent(llm=llm, df=data_frame, verbose=True, allow_dangerous_code=True)

def query_lyrics_dataframe(lyrics):
    lowercase_lyrics = lyrics.lower()
    response = p_agent.run(f"From the lyrics '{lowercase_lyrics}', retrieve song information? Format Answer: Song Title - Artist - Year - Artists Collaborated(Year Collaborated)__Artists Collaborated 2(Year Collaborated 2). If lyrics are not found in the database, report 'No information found in the data!'")
    if response.strip() == "":
        return None
    else:
        parts = response.split(' - ')
        if len(parts) < 4:
            return None
        song_title, artist, year, collaborations = parts
        collaborations = collaborations.replace("__", " - ")
        return f"Song Title: {song_title} <br> Artist: {artist} <br> Year: {year} <br> Collaborated: {collaborations}"


def query_lyrics_openai(lyrics):
    text = f"From the lyrics '{lyrics}', retrieve song information? And List all artists who have collaborated with and the year of collaboration? Format Answer: Song Title - Artist - Year."
    return llm(text)



changs = Blueprint('changs', __name__)

@changs.route('/', methods = ['GET', 'POST'])
def home():
    chats = ""
    if request.method == 'POST':
        prompt = request.form.get('text-solu')
        result = query_lyrics_dataframe(prompt)
        if result is None:
            result = query_lyrics_openai(prompt)
        
        # chats = markdown.markdown(result)
        chats = result
    
    
    chats = chats
    print(chats)
    return render_template("index.html", chats = chats)







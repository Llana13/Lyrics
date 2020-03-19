import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import json_lines
from PIL import Image
from collections import Counter
from wordcloud import WordCloud, STOPWORDS

#Read the file and set artist list
df = pd.read_json (,lines=True)
list_artists = ['Ed Sheeran','Camila Cabello','Queen','Eminem','Drake','Post Malone','Khalid','Rihanna']

#Feature Engineering
df = df.drop(axis=0,labels=range(8))
df = df.reset_index()
df= df.drop(['index'],axis=1)
df = df.drop_duplicates(subset='lyrics')
df['artist'] = df[df['artist'].isin(list_artists)]
df = df.dropna()

#List of Stopwords
SW = ["i","I'm","m","am", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor","oh", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

#Takes all songs from an artist (as string) and put them as a string
def raw (artist):
    df_a = df.loc[df['artist']==f'{artist}']
    a_lyrics = df_a['lyrics']
    a_lyrics = a_lyrics.tolist()
    a_lyrics = [x.replace('\n', '') for x in a_lyrics]
    a_lyrics_raw = (" ").join(a_lyrics)
    lyrics_raw = a_lyrics_raw
    return lyrics_raw

def face_cloud(mask,lyrics_raw):
    def transform_format(val):
        if val == 0:
            return 255
        else:
            return 1
    transformed_mask = np.ndarray((mask.shape[0],mask.shape[1]), np.int32)

    for i in range(len(mask)):
        transformed_mask[i] = list(map(transform_format, mask[i]))

    wc = WordCloud(background_color="black", max_words=100, mask=transformed_mask,
        contour_width=0.1,contour_color='grey',colormap='Greys',stopwords=SW)

    wc.generate(lyrics_raw)
    plt.imshow(wc)
    plt.axis("off")
    plt.figure(figsize=(10,10))
    plt.show()

def cloud(artist,mask):
    face_cloud(mask,raw(artist))


# cloud(input('Whose lyrics?'),drake_face)
singer = input('Whose lyrics? ')
face = input('Whose face? ')
if face == 'Drake':
    face = drake_face
elif face== 'Eminem':
    face = eminem_face
elif face== 'Queen':
    face =  queen_face
else: face = edSheeran_face

cloud(singer,face)

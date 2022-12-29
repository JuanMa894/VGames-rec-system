import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
from PIL import Image
import base64

# def markdown/background image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('images/app_cover.png')  

logo = Image.open('images/Polygon_logo.png')
st.image(logo, caption='')

st.title('Game Recommendation System')

#loading dataset
Ratings = pd.read_csv('data/GameRatings.csv')


# loading model
@st.cache
def load_model(file):
    model_file = open(file, 'rb')
    loaded_model = joblib.load(model_file)
    model_file.close()
    return loaded_model

reco_model = load_model('Model/svd_model.sav')

def game_recommender(customer_id, num_of_rec):
    
    customer = int(customer_id)
    nRec = int(num_of_rec)

    customer_set = pd.DataFrame(Ratings.clean_title.values, index=Ratings['customer_id'], columns=['clean_title'])
    played = list(customer_set.loc[customer, 'clean_title'])
    unique_games = (Ratings.drop_duplicates('clean_title')).set_index('clean_title')
    not_played = unique_games.drop(played)
    not_played.reset_index(inplace=True)
    not_played['prediction'] = not_played['clean_title'].apply(lambda x: reco_model.predict(customer, x).est)
    not_played.sort_values(by='prediction', ascending=False, inplace=True)
    top_30 =  not_played['clean_title'].head(30)
    recommendation = top_30.sample(n=nRec)
    fig = plt.figure(figsize=(20,5))
    font_size=16
    p_df = pd.DataFrame(played, columns=(['Played Games'])).head()
    ax1 = fig.add_subplot(121)
    bbox=[0, 0, 1, 1]
    ax1.axis('off')
    mpl_table1 = ax1.table(cellText = p_df.values, rowLabels = p_df.index, bbox=bbox, colLabels=p_df.columns, colColours='blue')
    mpl_table1.auto_set_font_size(False)
    mpl_table1.set_fontsize(font_size)
    r_df = pd.DataFrame(recommendation)
    r_df.reset_index(inplace=True, drop=True)
    ax2 = fig.add_subplot(122)
    bbox=[0, 0, 1, 1]
    ax2.axis('off')
    mpl_table2 = ax2.table(cellText = r_df.values, rowLabels = r_df.index, bbox=bbox, colLabels=(['Recommended Games']), colColours='red')
    mpl_table2.auto_set_font_size(False)
    mpl_table2.set_fontsize(font_size)
    st.pyplot(fig)


customer_id = st.selectbox(
    "Customer ID",
    Ratings['customer_id'].unique())

num_of_rec = st.selectbox(
    'How many recommendations would you like?',
    ('1', '2', '3', '4', '5'))
st.write('You selected:', num_of_rec)


rec_button = st.button("Enter")
if rec_button:
    recomm = game_recommender(customer_id, num_of_rec)
    st.write(recomm)

st.subheader('By Juan Acosta')
st.markdown('[GitHub](https://github.com/JuanMa894/VGames-rec-system), [Linkedin](https://www.linkedin.com/in/jun-acost/)')

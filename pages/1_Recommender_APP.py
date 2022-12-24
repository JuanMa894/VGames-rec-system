import streamlit as st
import pandas as pd
import numpy as np
import joblib
from PIL import Image

st.sidebar.title('Recommender System')

st.title('Recommendation System Demo')

@st.cache
def load_model(file):
    model_file = open(file, 'rb')
    loaded_model = joblib.load(model_file)
    model_file.close()
    return loaded_model

reco_model = load_model('svd_model.sav')


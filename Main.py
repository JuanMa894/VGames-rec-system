import streamlit as st
import pandas as pd
import numpy as np
import joblib
from PIL import Image

st.sidebar.title('Recommender System')

cover_image = Image.open('images/cover.png')
st.image(cover_image, '..', use_column_width='always')






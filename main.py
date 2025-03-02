import streamlit as st
import json
# Page Setup
st.set_page_config(page_title="Unit Convertor",layout="wide")
st.header("Unit Convertor")
st.write("Replicates [Google's Unit Convertor](https://www.google.com/search?q=unit+convertor)")

with open("data/quantity.json") as quantity_file:
    quantity_list = json.loads(quantity_file.read())
    quantity = st.selectbox("Quantity",quantity_list,index=quantity_list.index("Length"),label_visibility="hidden")
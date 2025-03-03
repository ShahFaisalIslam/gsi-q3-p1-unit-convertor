import streamlit as st
import json
# Page Setup
st.set_page_config(page_title="Unit Convertor",layout="wide")
st.header("Unit Convertor")
st.write("Replicates [Google's Unit Convertor](https://www.google.com/search?q=unit+convertor)")

with open("data/quantity.json") as quantity_file:
    quantity_list = json.loads(quantity_file.read())
    quantity = st.selectbox("Quantity",quantity_list,index=quantity_list.index("Length"),label_visibility="hidden")
    # Turn quantity into lowercase and replace spaces with underscores
    quantity = quantity.lower().replace(" ","_")
    # For every quantity, there exists a file "data/quantity/{quantity}.json"
    # Open the file for the selected quantity and fetch from it the list of units
    with open(f"data/quantity/{quantity}.json") as unit_file:
        unit_list = json.loads(unit_file.read())
        unit = st.selectbox("Unit",unit_list,label_visibility="hidden")
        # Turn unit into lowercase and replace spaces with underscores
        unit = unit.lower().replace(" ","_")
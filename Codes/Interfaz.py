import streamlit as st
import requests


st.title("Sistema de búsqueda de talleres")

user_description = st.text_input("Escriba la descripción del curso:")


if st.button("Obtener resultados"):
    api_url = "http://localhost:3000/busqueda"
    payload = {"description": user_description}
    response = requests.post(api_url, json=payload)

    if response.status_code == 200:
        result_json = response.json()
        st.json(result_json)
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
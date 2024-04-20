import streamlit as st
import requests

seccion_actual = st.sidebar.radio("Selecciona una opción:", ["Realizar Búsqueda", "Imprimir base de datos"])

if seccion_actual == "Realizar Búsqueda":
    st.title("Sistema de búsqueda de talleres")
    user_description = st.text_input("Escriba la descripción del curso:")
    obtener_resultados = st.button("Obtener resultados")

    if obtener_resultados:
        api_url = "http://localhost:3000/busqueda"
        payload = {"description": user_description}
        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            result_json = response.json()
            st.json(result_json)
        else:
            st.error(f"Error: {response.status_code} - {response.text}")

elif seccion_actual == "Imprimir base de datos":
    api_url = "http://localhost:3000/imprimir_basededatos"
    db_response = requests.get(api_url)

    if db_response.status_code == 200:
        db_data = db_response.json()
        for entry in db_data:
            if isinstance(entry, dict):
                for key, value in entry.items():
                    st.write(f"{key}: {value}")
                validado = entry.get("validado", False)
                nuevo_estado = st.checkbox(label="Contactado?", value=validado, key=entry["contacto"])
                if nuevo_estado != validado:
                    update_url = "http://localhost:3000/marcar_contactado"
                    update_payload = {"contacto": entry["contacto"], "validado": nuevo_estado}
                    update_response = requests.post(update_url, json=update_payload)
                    if update_response.status_code == 200:
                        st.write("Estado de 'validado' actualizado con éxito")
                    else:
                        st.error(f"Error al actualizar el estado de 'validado': {update_response.status_code}")
                    st.rerun()
            st.write("---")
    else:
        st.error(f"Error: {db_response.status_code} - {db_response.text}")

import streamlit as st

st.set_page_config(page_title="Financial Report Generator", layout="wide")

from navbar import navbar
from interface import interface
from interface1 import interface1


if __name__ == "__main__":
    try:
        _logged_in = st.user.is_logged_in
    except AttributeError:
        _logged_in = True
    if not _logged_in:
        st.header("Veuillez vous connecter pour continuer.")
        st.button("Se connecter avec Microsoft", on_click=st.login)
        st.stop()

    if "user_email" not in st.session_state:
        st.session_state.user_email = getattr(st.user, "email", None) or "Unknown"

    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "Note d\u2019analyse sectorielle"

    navbar()

    if st.session_state.selected_page == "Note d\u2019analyse sectorielle":
        st.title("Note d\u2019analyse sectorielle")
        interface()
    elif st.session_state.selected_page == "Note d\u2019analyse mono sous-jacent":
        st.title("Note d\u2019analyse mono sous-jacent")
        interface1()

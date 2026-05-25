import os, sys

if os.environ.get("WEBSITE_SITE_NAME"):
    try:
        from azure_write_secrets import main as _write_secrets
        _rc = _write_secrets()
        print(f"[BOOT] azure_write_secrets returned {_rc}", file=sys.stderr, flush=True)
    except Exception as _e:
        print(f"[BOOT] azure_write_secrets failed: {_e}", file=sys.stderr, flush=True)

    secrets_path = os.path.join(os.getcwd(), ".streamlit", "secrets.toml")
    if os.path.exists(secrets_path):
        sz = os.path.getsize(secrets_path)
        print(f"[BOOT] secrets.toml exists, size={sz}", file=sys.stderr, flush=True)
    else:
        print(f"[BOOT] WARNING: secrets.toml MISSING at {secrets_path}", file=sys.stderr, flush=True)

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

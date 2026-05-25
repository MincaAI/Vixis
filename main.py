import streamlit as st

st.set_page_config(page_title="Financial Report Generator", layout="wide")

from navbar import navbar
from interface import interface
from interface1 import interface1

try:
    import traceback as _tb
    from streamlit.web.server.oauth_authlib_routes import AuthLoginHandler
    _orig_get = AuthLoginHandler.get
    async def _patched_get(self):
        try:
            return await _orig_get(self)
        except Exception as _exc:
            self.set_status(500)
            self.write(f"Auth error: {type(_exc).__name__}: {_exc}\n\n{_tb.format_exc()}")
            self.finish()
    AuthLoginHandler.get = _patched_get
except Exception:
    pass


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

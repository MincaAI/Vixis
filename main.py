import streamlit as st
import streamlit.components.v1 as components

# Must be the first Streamlit command (before any other st.* calls)
st.set_page_config(page_title="Financial Report Generator", layout="wide")

from streamlit_js_eval import streamlit_js_eval  # Handles cookies
from datetime import datetime
from navbar import navbar
from interface import interface
from interface1 import interface1


# === OAUTH DEBUG ===
print("[VIXIS DEBUG] === App Starting ===", flush=True)

# Log auth secrets config (sin exponer valores sensibles)
try:
    auth_conf = dict(st.secrets.get("auth", {}))
    print(f"[VIXIS DEBUG] redirect_uri = {auth_conf.get('redirect_uri', 'MISSING')}", flush=True)
    print(f"[VIXIS DEBUG] client_id = {auth_conf.get('client_id', 'MISSING')[:12]}...", flush=True)
    print(f"[VIXIS DEBUG] client_secret present = {bool(auth_conf.get('client_secret'))}", flush=True)
    print(f"[VIXIS DEBUG] client_secret starts with = {auth_conf.get('client_secret', '')[:5]}...", flush=True)
    print(f"[VIXIS DEBUG] cookie_secret present = {bool(auth_conf.get('cookie_secret'))}", flush=True)
    print(f"[VIXIS DEBUG] server_metadata_url = {auth_conf.get('server_metadata_url', 'MISSING')}", flush=True)
except Exception as e:
    print(f"[VIXIS DEBUG] Error reading auth secrets: {e}", flush=True)

# Detectar errores OAuth en query params (Microsoft los envía así)
try:
    qp = st.query_params
    if "error" in qp:
        oauth_error = qp.get("error", "unknown")
        oauth_desc = qp.get("error_description", "no description")
        print(f"[VIXIS DEBUG] OAUTH ERROR: {oauth_error}", flush=True)
        print(f"[VIXIS DEBUG] OAUTH ERROR DESC: {oauth_desc}", flush=True)
        st.error(f"OAuth Error from Microsoft: **{oauth_error}**\n\n{oauth_desc}")
    print(f"[VIXIS DEBUG] Query params: {dict(qp)}", flush=True)
except Exception as e:
    print(f"[VIXIS DEBUG] Error reading query params: {e}", flush=True)

# Check auth state
try:
    is_logged = st.user.is_logged_in
    print(f"[VIXIS DEBUG] is_logged_in = {is_logged}", flush=True)
    if is_logged:
        print(f"[VIXIS DEBUG] user.name = {st.user.name}", flush=True)
except Exception as e:
    print(f"[VIXIS DEBUG] Auth state error: {e}", flush=True)
    st.error(f"Error checking auth: {e}")

# JavaScript debug en consola del navegador
components.html("""
<script>
console.log('=== VIXIS OAUTH DEBUG ===');
console.log('[VIXIS] Page loaded at:', new Date().toISOString());
console.log('[VIXIS] Current URL:', window.location.href);

// Intentar acceder a la URL del parent (página principal de Streamlit)
try {
    console.log('[VIXIS] Parent URL:', window.parent.location.href);
    var params = new URLSearchParams(window.parent.location.search);
    params.forEach(function(value, key) {
        if (key === 'code') {
            console.log('[VIXIS] OAuth auth code: [RECEIVED]');
        } else {
            console.log('[VIXIS] URL Param:', key, '=', value);
        }
    });
    if (params.has('error')) {
        console.error('[VIXIS] OAUTH ERROR:', params.get('error'));
        console.error('[VIXIS] ERROR DESCRIPTION:', params.get('error_description'));
    }
} catch(e) {
    console.log('[VIXIS] Cannot access parent URL (cross-origin):', e.message);
}

// Log cookies visibles
console.log('[VIXIS] Cookies:', document.cookie || '(none visible from iframe)');

// Interceptar fetch requests del iframe para detectar errores
var originalFetch = window.fetch;
window.fetch = function() {
    var url = typeof arguments[0] === 'string' ? arguments[0] : (arguments[0] && arguments[0].url) || 'unknown';
    console.log('[VIXIS] Fetch:', url);
    return originalFetch.apply(this, arguments).then(function(response) {
        if (response.status >= 400) {
            console.error('[VIXIS] HTTP ERROR', response.status, 'on', url);
            response.clone().text().then(function(body) {
                console.error('[VIXIS] Error body:', body.substring(0, 500));
            });
        }
        return response;
    }).catch(function(err) {
        console.error('[VIXIS] Fetch failed:', url, err);
        throw err;
    });
};

console.log('=== VIXIS DEBUG READY ===');
</script>
""", height=0)

print("[VIXIS DEBUG] === Debug injection done ===", flush=True)
# === END OAUTH DEBUG ===


if __name__ == "__main__":
    if not st.user.is_logged_in:
        st.header("Please log in to continue.")
        st.button("Log in with Microsoft", on_click=st.login)
        st.stop()

    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "Note d’analyse sectorielle"

    navbar()
    
    if st.session_state.selected_page == "Note d’analyse sectorielle":
        st.title("Note d’analyse sectorielle")
        interface()
    elif st.session_state.selected_page == "Note d’analyse mono sous-jacent":
        st.title("Note d’analyse mono sous-jacent")
        interface1()
    # main()

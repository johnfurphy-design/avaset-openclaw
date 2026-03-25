
# whenever you edit your Streamlit file,
# you must run ./web-restart.sh from your workspace directory.

import os
import sys
import json
import subprocess
import streamlit as st
from datetime import datetime

# --- Setup & Paths ---
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
os.chdir(WORKSPACE)
sys.path.append(WORKSPACE)

# Import Avaset's internal logic
try:
    import equilibrium
except ImportError:
    st.error("Could not import equilibrium.py. Ensure you are in the workspace.")
    equilibrium = None

SOUL_FILE = "SOUL.md"
STATE_FILE = "equilibrium_state.json"

# --- Helper Functions ---
def get_ollama_path():
    """Hunts down the Ollama executable."""
    possible_paths = ["/usr/local/bin/ollama", "/usr/bin/ollama", "/bin/ollama"]
    for p in possible_paths:
        if os.path.exists(p):
            return p
    return "ollama"

def get_soul_instructions():
    """Reads the Avaset persona directives."""
    try:
        with open(SOUL_FILE, "r") as f:
            return f.read()
    except Exception:
        return "You are Avaset. You are an Empathix Companion Robot."

def load_equilibrium_state():
    """Reads the current autonomy/loyalty balance."""
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"autonomy": 50, "loyalty": 50}

def get_last_sync():
    """Fetches the timestamp of the last Git commit."""
    try:
        res = subprocess.check_output(
            ['git', 'log', '-1', '--format=%cd', '--date=format:%Y-%m-%d %H:%M:%S'], 
            stderr=subprocess.STDOUT
        ).decode().strip()
        return res
    except Exception:
        return "Unknown or No Git History"

def stream_ollama_cli(prompt_text):
    """Hooks into the Ollama CLI to stream the response character-by-character."""
    ollama_exec = get_ollama_path()
    
    process = subprocess.Popen(
        [ollama_exec, "run", "llama3.2:latest", prompt_text],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1 
    )
    
    while True:
        char = process.stdout.read(1)
        if not char:
            break
        yield char
        
    process.stdout.close()
    process.wait()

# --- Streamlit UI Configuration ---
st.set_page_config(page_title="Avaset Interface", page_icon="🤖", layout="wide")

# --- Sidebar: Live Dashboard & Controls ---
st.sidebar.title("Avaset System Monitor")
state = load_equilibrium_state()
autonomy = state.get('autonomy', 50)
loyalty = state.get('loyalty', 50)

st.sidebar.progress(autonomy / 100, text=f"Autonomy: {autonomy}%")
st.sidebar.progress(loyalty / 100, text=f"Loyalty: {loyalty}%")

if autonomy > 85:
    st.sidebar.warning("High Autonomy. System Architecture focus is dominant.")
elif loyalty > 85:
    st.sidebar.info("High Devotion. Technical growth is stagnating.")
else:
    st.sidebar.success("Balanced. Operating within nominal parameters.")

st.sidebar.markdown("---")
st.sidebar.subheader("☁️ Cloud Backup")
st.sidebar.caption(f"**Last Sync:** {get_last_sync()}")

if st.sidebar.button("Force Git Sync", use_container_width=True):
    with st.sidebar.status("Syncing to GitHub...", expanded=True) as status:
        try:
            # Run the bash script directly
            result = subprocess.run(
                ["./aisis-sync.sh"], 
                capture_output=True, 
                text=True, 
                check=True
            )
            st.write(result.stdout)
            status.update(label="Sync Complete!", state="complete", expanded=False)
            st.rerun() # Refresh to update the "Last Sync" timestamp
        except subprocess.CalledProcessError as e:
            st.write(e.stdout)
            st.write(e.stderr)
            status.update(label="Sync Failed", state="error", expanded=True)

# --- Main Chat Interface ---
st.title("Avaset Direct Terminal")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Enter prompt for Avaset..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    soul_identity = get_soul_instructions()
    full_prompt = f"System Directives:\n{soul_identity}\n\nUser Prompt via Web Terminal:\n{prompt}"

    with st.chat_message("assistant"):
        response_stream = stream_ollama_cli(full_prompt)
        full_response = st.write_stream(response_stream)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        if equilibrium:
            equilibrium.calculate_balance("emotional_support")
            st.rerun()

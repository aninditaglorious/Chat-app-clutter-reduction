import streamlit as st
import time

# --- 1. THE "SEED LAYER" (Multi-Group Definitions) ---
GROUP_CONFIGS = {
    "🏫 School Group": {
        "🔴 RED": ["bus", "late", "route", "21b", "driver"],
        "🔵 BLUE": ["exam", "syllabus", "geometry", "chapter", "ebarer", "kalker"],
        "⚪ GREY": ["happy", "birthday", "congrats"]
    },
    "🏢 Office Group": {
        "🔴 RED": ["deadline", "urgent", "client", "boss", "immediate"],
        "🔵 BLUE": ["meeting", "minutes", "agenda", "presentation", "deck"],
        "⚪ GREY": ["lunch", "chai", "joke", "weekend"]
    }
}

# --- 2. THE SIEVE ENGINE (Deterministic Topic Hashing) ---
def get_color_logic(msg, last_time, last_color, current_group):
    current_time = time.time()
    # Spatio-Temporal Rule: 15-second window for intent inheritance 
    if last_time and (current_time - last_time) < 15: 
        return last_color
    
    msg = msg.lower()
    config = GROUP_CONFIGS[current_group]
    
    for color, keywords in config.items():
        if any(word in msg for word in keywords):
            return color
    return "🟡 YELLOW"

# --- 3. UI ARCHITECTURE (Train-Line Interface) ---
st.set_page_config(page_title="Multi-Group Sieve", layout="centered")
selected_group = st.sidebar.selectbox("Select Active Group", list(GROUP_CONFIGS.keys())) 
st.title(f"Sieve: {selected_group}")

# Initialize session states for the specific group
history_key = f'history_{selected_group}'
if history_key not in st.session_state:
    st.session_state[history_key] = []
    st.session_state.last_time = None
    st.session_state.last_color = "🟡 YELLOW"

# --- 4. GHOST TRAIL ANIMATION (CSS) ---
st.markdown("""
<style>
@keyframes slideUpAndFade {
    0% { opacity: 1; transform: translateY(0); }
    100% { opacity: 0; transform: translateY(-100px); height: 0; margin: 0; padding: 0; }
}
.ghost-message {
    animation: slideUpAndFade 1.5s forwards;
    animation-delay: 5s; /* Stays 'Live' for 5s before ghosting */
}
</style>
""", unsafe_allow_html=True) 

# --- 5. TRAIN-LINE VISUALIZER ---
st.markdown("### 🚂 Topic Trail")
cols = st.columns(4)
cols[0].markdown("🔴 **Red/Urgent**")
cols[1].markdown("🔵 **Blue/Admin**")
cols[2].markdown("⚪ **Social**")
cols[3].markdown("🟡 **General**") 

# --- 6. INPUT AND PROCESSING ---
user_msg = st.text_input(f"Send to {selected_group}...")

if st.button("Send Message"):
    if user_msg:
        color = get_color_logic(user_msg, st.session_state.last_time, st.session_state.last_color, selected_group)
        # Append message with a unique timestamp for the Ghost Trail
        st.session_state[history_key].append({"text": user_msg, "color": color, "time": time.time()})
        st.session_state.last_time = time.time()
        st.session_state.last_color = color

# --- 7. ACTIVE FEED RENDERER ---
st.write("---")
st.subheader("Active Feed")
# Using the defined history_key to avoid NameError
for m in reversed(st.session_state[history_key]):
    # Assign border color based on the Sieve result 
    border_color = "red" if "🔴" in m['color'] else "blue" if "🔵" in m['color'] else "grey" if "⚪" in m['color'] else "gold"
    
    st.markdown(f"""
        <div class="ghost-message" style="border: 2px solid {border_color}; padding: 10px; border-radius: 5px; margin-bottom: 5px; background: white; color: black;">
            {m['text']}
        </div>
    """, unsafe_allow_html=True)
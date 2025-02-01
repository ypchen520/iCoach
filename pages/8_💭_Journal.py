from data_sources import firebase, models
import datetime
import streamlit as st

# col1, col2, col3 = st.columns(3, gap="small")

# with col1:
#     st.header("A")
#     st.image("https://www.nps.gov/common/uploads/cropped_image/primary/7357F452-9461-A974-DF84E7F4C6A616BC.jpg?width=1600&quality=90&mode=crop")
#     st.image("https://www.nps.gov/common/uploads/cropped_image/primary/7357F452-9461-A974-DF84E7F4C6A616BC.jpg?width=1600&quality=90&mode=crop")
#     st.image("https://www.nps.gov/common/uploads/cropped_image/primary/7357F452-9461-A974-DF84E7F4C6A616BC.jpg?width=1600&quality=90&mode=crop")

# with col2:
#     st.header("B")
#     st.image("https://eagles.org/wp-content/uploads/layerslider/HomepageSlider/Challenger-Gena-2-V2-copy-scaled.jpg")

# with col3:
#     st.header("C")
#     st.image("https://eagles.org/wp-content/uploads/layerslider/HomepageSlider/Challenger-Gena-2-V2-copy-scaled.jpg")

# """
# Create timestamp
# mood before
# journal
# mood after
# mood: happy, excited, grateful, relaxed, content, tired, unsure, bored, anxious, angry, stressed, sad
# english
# use LangChain for generating meaning and examples
# """

# Quote
# There is a fountain of youth: it is your mind, your talents, the creativity you bring to your life and the lives of people you love. When you learn to tap this source, you will truly have defeated age
# Just before the sparks of life are extinguished from a candle, the flame dances. It sends a wistful, thin smoke line up into the air, where it circles and pirouettes before it vanishes toward the sky. Light a candle and watch that dance, learn about life and its last breaths.
# Keep your flame lit, let it dance in your heart, and you won’t disappear. The world will still see you. Because you’re lighting the way for all who follow.


# Python
# A nice and clean generator expression here, an elegant use of the "with"-statement there…
# With some practice you can do this tastefully—only where these features make sense and help make the code more expressive.
# And trust me, your colleagues will pick up on this after a while. If they ask you questions, be generous and helpful.
# Pull everyone around you UP and help them learn what you know.

# Create a tab for english
# use langchain to explain the term, and then create a sentence, and then maybe a story after three logs?

# Get Firestore client
db = firebase.get_firestore_client()

# Define mood options
moods = [
    ["Happy", "Excited", "Grateful"],
    ["Relaxed", "Content", "Tired"],
    ["Unsure", "Bored", "Anxious"],
    ["Angry", "Stressed", "Sad"]
]

mood_emojies = [
    ["😊", "🤩", "🙏"],
    ["😌", "🙂", "🥱"],
    ["🤔", "😐", "😬"],
    ["😤", "😣", "😢"]
]

# Function to save journal entry to Firestore
def save_journal_entry(user_id, entry):
    user_ref = db.collection("User").document(user_id)
    journal_ref = user_ref.collection("journal")
    doc_id = entry.date.isoformat()
    journal_ref.document(doc_id).set(entry.__dict__)
    # journal_ref.add(entry.__dict__)

def toggle_mood(mood, mood_buttons):
    mood_buttons[mood] = not mood_buttons[mood]

# Streamlit app
st.title(':thought_balloon: Journal')

# Select user ID
# user_id = st.selectbox("Select User ID", ["eagle"])
user_id = "eagle"

# Rate initial mood
st.markdown("<h3>How are you feeling today?</h3>", unsafe_allow_html=True)

if 'initial_mood' not in st.session_state:
    st.session_state.initial_mood = set()

if 'mood_buttons' not in st.session_state:
    st.session_state.mood_buttons = {mood: False for mood in [mood for row in moods for mood in row]}

if 'final_mood' not in st.session_state:
    st.session_state.final_mood = set()

if 'final_mood_buttons' not in st.session_state:
    st.session_state.final_mood_buttons = {mood: False for mood in [mood for row in moods for mood in row]}


with st.container():
    # st.markdown(col_style, unsafe_allow_html=True)
    for i in range(len(moods)):
        row = moods[i]
        ncols = len(row)
        cols = st.columns(ncols, gap="small", vertical_alignment="center", border=True)
        for j in range(ncols):
            mood = moods[i][j]
            emoji = mood_emojies[i][j]
            if st.session_state.mood_buttons[mood]:
                st.session_state.initial_mood.add(mood)
                cols[j].button(mood, key=mood, icon=emoji, use_container_width=True, type="primary", on_click=toggle_mood, args=(mood, st.session_state.mood_buttons))
            else:
                st.session_state.initial_mood.discard(mood)
                cols[j].button(mood, key=mood, icon=emoji, use_container_width=True, type="tertiary", on_click=toggle_mood, args=(mood, st.session_state.mood_buttons))

# st.write(st.session_state.initial_mood)

# Journaling interface

if st.session_state.initial_mood:
    st.markdown("<h3>Journal your thoughts</h3>", unsafe_allow_html=True)
    reflection = st.text_area(":pencil2:")
    # st.write(reflection)

    # Rate final mood
    if reflection:
        
        st.markdown("<h3>How are you feeling now?</h3>", unsafe_allow_html=True)

        with st.container():
            # st.markdown(col_style, unsafe_allow_html=True)
            for i in range(len(moods)):
                row = moods[i]
                ncols = len(row)
                cols = st.columns(ncols, gap="small", vertical_alignment="center", border=True)
                for j in range(ncols):
                    mood = moods[i][j]
                    emoji = mood_emojies[i][j]
                    if st.session_state.final_mood_buttons[mood]:
                        st.session_state.final_mood.add(mood)
                        cols[j].button(mood, key=f"{mood}_final", icon=emoji, use_container_width=True, type="primary", on_click=toggle_mood, args=(mood, st.session_state.final_mood_buttons))
                    else:
                        st.session_state.final_mood.discard(mood)
                        cols[j].button(mood, key=f"{mood}_final", icon=emoji, use_container_width=True, type="tertiary", on_click=toggle_mood, args=(mood, st.session_state.final_mood_buttons))

    # st.write(st.session_state.final_mood)


    # Save journal entry
    st.markdown("<style>button {float: right}</style>", unsafe_allow_html=True)
    if st.session_state.final_mood and st.button("Save", icon=":material/mood:"):
        entry = models.JournalEntry(
            date=datetime.datetime.now(),
            mood_before=list(st.session_state.initial_mood),
            reflection=reflection,
            mood_after=list(st.session_state.final_mood)
        )
        save_journal_entry(user_id, entry)
        st.success("Journal entry saved!")
import streamlit as st
import pandas as pd
import random
import os
from datetime import datetime

# ---------------------------
# Configuration
# ---------------------------
st.set_page_config(page_title="Speech Perception Pilot")

METADATA_FILE = "metadata.csv"

ORIGINAL_DIR = "original"
GENERATED_DIR = "generated"
RESP_DIR = "responses"

os.makedirs(RESP_DIR, exist_ok=True)

QUESTION_TYPES = ["word", "severity", "similarity"]


# ---------------------------
# Trial Generation
# ---------------------------
def generate_trials():

    df = pd.read_csv(METADATA_FILE)
    #df = pd.read_excel(METADATA_FILE)

    trials = []

    for _, row in df.iterrows():

        for q in QUESTION_TYPES:

            d = row.to_dict()
            d["question"] = q
            trials.append(d)

    random.shuffle(trials)

    trials_df = pd.DataFrame(trials)
    trials_df["trial"] = range(1, len(trials_df) + 1)

    return trials_df


# ---------------------------
# Welcome Page
# ---------------------------
if "started" not in st.session_state:

    st.title("Speech Perception Pilot Study")

    st.write(
        """
        You will hear an Original and a Generated speech utterance.

        Listen carefully and answer the question shown.

        There are 90 trials.

        Please use headphones.
        """
    )

    participant = st.text_input("Participant ID")

    consent = st.checkbox("I agree to participate.")

    if st.button("Start"):

        if participant == "":
            st.error("Please enter Participant ID.")
            st.stop()

        if not consent:
            st.error("Please provide consent.")
            st.stop()

        st.session_state.started = True
        st.session_state.pid = participant
        st.session_state.i = 0
        st.session_state.df = generate_trials()

        st.rerun()

    st.stop()


# ---------------------------
# Experiment
# ---------------------------
df = st.session_state.df
i = st.session_state.i

if i >= len(df):

    st.success("Thank you! Experiment completed.")

    st.stop()

row = df.iloc[i]

st.progress((i + 1) / len(df))

st.header(f"Trial {i+1} / {len(df)}")

# ---------------------------
# Original Audio
# ---------------------------
st.subheader("Original")

st.audio(os.path.join(ORIGINAL_DIR, row.filename))

# ---------------------------
# Generated Audio
# ---------------------------
st.subheader("Generated")

st.audio(os.path.join(GENERATED_DIR, row.filename))

# ---------------------------
# Transcript
# ---------------------------
st.subheader("Transcript")

st.info(row.transcript)

# ---------------------------
# Questions
# ---------------------------
answer = None

if row.question == "word":

    words = str(row.words).split("|")

    answer = st.radio(
        "Which word sounds most different?",
        words + ["No noticeable difference"],
    )

elif row.question == "severity":

    answer = st.radio(
        "How much was the affected word altered?",
        [1, 2, 3, 4, 5],
        horizontal=True,
    )

elif row.question == "similarity":

    answer = st.radio(
        "How similar is the generated utterance to the original?",
        [1, 2, 3, 4, 5],
        horizontal=True,
    )

# ---------------------------
# Save Response
# ---------------------------
if st.button("Submit & Next"):

    out = os.path.join(
        RESP_DIR,
        f"{st.session_state.pid}_responses.csv",
    )

    response = pd.DataFrame(
        [
            {
                "participant": st.session_state.pid,
                "trial": row.trial,
                "filename": row.filename,
                "question": row.question,
                "response": answer,
                "timestamp": datetime.now(),
            }
        ]
    )

    if os.path.exists(out):

        response.to_csv(
            out,
            mode="a",
            header=False,
            index=False,
        )

    else:

        response.to_csv(
            out,
            index=False,
        )

    st.session_state.i += 1

    st.rerun()

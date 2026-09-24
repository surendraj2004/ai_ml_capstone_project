import streamlit as st

from graph import ask_question


#page settings
st.set_page_config(
    page_title="Zepto Support Assistant",
    page_icon="🛒"
)

#title
st.title("Zepto Support Assistant")

st.write(
    "Ask questions about Zepto delivery, returns, membership, "
    "tracking, cancellation, gift cards and support."
)

#user question
question = st.text_input(
    "Enter your question:"
)

#ask button
if st.button("Ask"):

    if question.strip() == "":
        st.warning("Please enter a question.")

    else:

        with st.spinner("Finding the answer..."):

            response = ask_question(question)

        #display answer
        st.subheader("Answer")
        st.write(response.answer)

        #display sources
        st.subheader("Sources")

        if response.sources:

            for source in response.sources:
                st.write("- " + source)

        else:
            st.write("No policy document used.")

        #display confidence
        st.write(
            "Confidence:",
            response.confidence
        )


#sidebar
st.sidebar.title("About")

st.sidebar.write(
    "Zepto Support Assistant"
)

st.sidebar.write("LangGraph")
st.sidebar.write("ChromaDB")
st.sidebar.write("Sentence Transformers")
st.sidebar.write("Zepto Policy Documents")
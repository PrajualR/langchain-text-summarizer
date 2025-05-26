import streamlit as st
from summarizer import TextSummarizer

# Page configuration
st.set_page_config(
    page_title="LangChain Text Summarizer",
    page_icon="📝",
    layout="wide"
)

# Initialize summarizer
@st.cache_resource
def load_summarizer():
    try:
        return TextSummarizer()
    except ValueError as e:
        st.error(f"Configuration Error: {e}")
        st.stop()

def main():
    st.title("📝 LangChain Text Summarizer")
    st.markdown("Transform long texts into concise summaries using AI")

    # Main interface
    col1, col2, col3 = st.columns([1, 3, 3])

    with col1:
        # Summary type selection
        summary_type = st.selectbox(
            "Summary Type",
            ["Standard Summary", "Bullet Points"],
            help="Choose the type of summary you want"
        )

    with col2:
        st.header("📄 Input Text")

        # Text input methods
        input_method = st.radio(
            "Choose input method:",
            ["Type/Paste Text", "Upload File"]
        )

        text_to_summarize = ""

        if input_method == "Type/Paste Text":
            text_to_summarize = st.text_area(
                "Enter text to summarize:",
                height=300,
                placeholder="Paste your text here..."
            )

        else:  # Upload File
            uploaded_file = st.file_uploader(
                "Upload a text file",
                type=['txt', 'md'],
                help="Upload a .txt or .md file"
            )

            if uploaded_file is not None:
                try:
                    text_to_summarize = uploaded_file.read().decode('utf-8')
                    st.success(f"File uploaded successfully! ({len(text_to_summarize)} characters)")
                except Exception as e:
                    st.error(f"Error reading file: {e}")

        # Show text statistics
        if text_to_summarize:
            st.info(f"📊 Text Statistics: {len(text_to_summarize)} characters, ~{len(text_to_summarize.split())} words")

    with col3:
        st.header("✨ Summary")

        if st.button("🚀 Generate Summary", type="primary", use_container_width=True):
            if not text_to_summarize.strip():
                st.warning("Please enter some text to summarize!")
                return

            # Initialize summarizer
            summarizer = load_summarizer()

            # Show loading spinner
            with st.spinner("Generating summary..."):
                # Generate summary based on selected type
                if summary_type == "Standard Summary":
                    summary = summarizer.summarize_text(text_to_summarize)
                elif summary_type == "Bullet Points":
                    summary = summarizer.summarize_with_bullets(text_to_summarize)

            # Display summary
            if summary.startswith("Error"):
                st.error(summary)
            else:
                st.success("Summary generated successfully!")
                st.markdown("### 📋 Your Summary:")
                st.markdown(summary)

                # Summary statistics
                summary_length = len(summary)
                original_length = len(text_to_summarize)
                compression_ratio = round((1 - summary_length / original_length) * 100, 1)

                st.info(f"📈 Compression: {compression_ratio}% reduction in length")

                # Download button
                st.download_button(
                    label="💾 Download Summary",
                    data=summary,
                    file_name="summary.txt",
                    mime="text/plain"
                )

if __name__ == "__main__":
    main()
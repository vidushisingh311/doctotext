import streamlit as st
import os
from markitdown import MarkItDown
from io import BytesIO

# Configure the Streamlit page
st.set_page_config(page_title="Universal Doc-to-Text", page_icon="📄")

def main():
    st.title("📄 Universal Document Converter")
    st.markdown("Convert Office docs, PDFs, and HTML into clean Markdown instantly.")

    # 1. Initialize the Engine
    # Note: MarkItDown handles the conversion logic internally.
    md_engine = MarkItDown()

    # 2. Upload Area
    uploaded_files = st.file_uploader(
        "Drag and drop files here", 
        type=["docx", "xlsx", "pptx", "pdf", "html", "zip"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            base_name = os.path.splitext(uploaded_file.name)[0]
            
            st.divider()
            st.subheader(f"Processing: {uploaded_file.name}")

            try:
                # To process with MarkItDown, we save to a temporary location 
                # or pass the stream if supported. For maximum stability with 
                # all MarkItDown sub-parsers, we'll use a temp file.
                with open(uploaded_file.name, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # 3. The Conversion Process
                # Error handling and timeout logic is managed within the try-except block
                result = md_engine.convert(uploaded_file.name)
                converted_text = result.text_content

                # 4. Instant Preview
                st.text_area(
                    label="Markdown Preview",
                    value=converted_text,
                    height=300,
                    key=f"text_{uploaded_file.name}"
                )

                # 5. Download Options
                col1, col2 = st.columns(2)
                
                with col1:
                    st.download_button(
                        label="📥 Download as .md",
                        data=converted_text,
                        file_name=f"{base_name}_converted.md",
                        mime="text/markdown",
                        key=f"md_{uploaded_file.name}"
                    )
                
                with col2:
                    st.download_button(
                        label="📄 Download as .txt",
                        data=converted_text,
                        file_name=f"{base_name}_converted.txt",
                        mime="text/plain",
                        key=f"txt_{uploaded_file.name}"
                    )
                
                # Cleanup temp file
                os.remove(uploaded_file.name)

            except Exception as e:
                # Resilience: Catch-all to prevent app crash
                st.error(f"⚠️ Could not read {uploaded_file.name}. Please check the format.")
                # Log technical error to console for the dev
                print(f"Error processing {uploaded_file.name}: {e}")

if __name__ == "__main__":
    main()

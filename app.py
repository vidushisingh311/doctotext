import streamlit as st
import os
import sys
from markitdown import MarkItDown

# Configure the Streamlit page
st.set_page_config(page_title="Universal Doc-to-Text", page_icon="📄", layout="wide")

def get_file_size(file_path):
    """Returns the file size in a human-readable format."""
    size_bytes = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}", size_bytes
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB", size_bytes

def get_text_size(text):
    """Returns the size of the generated string in human-readable format."""
    size_bytes = sys.getsizeof(text)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}", size_bytes
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB", size_bytes

def main():
    st.title("📄 Universal Document Converter")
    st.markdown("Convert Office docs, PDFs, and HTML into clean Markdown instantly.")

    # Initialize Engine
    md_engine = MarkItDown()

    # Upload Area
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
            st.subheader(f"📄 {uploaded_file.name}")

            try:
                # Save temp file to get original size and process
                temp_filename = uploaded_file.name
                with open(temp_filename, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Get original file stats
                original_size_str, original_size_bytes = get_file_size(temp_filename)

                # Conversion
                result = md_engine.convert(temp_filename)
                converted_text = result.text_content
                
                # Get converted stats
                converted_size_str, converted_size_bytes = get_text_size(converted_text)

                # Tabs for UI
                tab1, tab2 = st.tabs(["🔍 Preview & Download", "📊 File Size Comparison"])

                with tab1:
                    st.text_area("Markdown Preview", value=converted_text, height=300, key=f"text_{uploaded_file.name}")
                    
                    c1, c2 = st.columns(2)
                    c1.download_button("📥 Download .md", converted_text, f"{base_name}_converted.md", "text/markdown", key=f"md_{uploaded_file.name}")
                    c2.download_button("📄 Download .txt", converted_text, f"{base_name}_converted.txt", "text/plain", key=f"txt_{uploaded_file.name}")

                with tab2:
                    # Calculate percentage reduction
                    reduction = ((original_size_bytes - converted_size_bytes) / original_size_bytes) * 100
                    
                    st.table({
                        "Metric": ["Original File Size", "Converted Text Size"],
                        "Value": [original_size_str, converted_size_str]
                    })
                    
                    if reduction > 0:
                        st.success(f"💡 Text version is **{reduction:.1f}% smaller** than the original file.")
                    else:
                        st.info("The text version is similar in size to the original.")

                # Cleanup
                os.remove(temp_filename)

            except Exception as e:
                st.error(f"⚠️ Could not read {uploaded_file.name}. Please check the format.")
                if os.path.exists(uploaded_file.name):
                    os.remove(uploaded_file.name)

if __name__ == "__main__":
    main()

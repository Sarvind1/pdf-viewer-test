"""Streamlit app for testing different PDF viewing methods."""

import streamlit as st
import base64
import os
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="PDF Viewer Test",
    layout="wide",
    initial_sidebar_state="expanded"
)

def embed_pdf_base64(file_path):
    """Generate HTML for embedding PDF using multiple approaches."""
    if not file_path or not os.path.exists(file_path):
        return "<p>PDF file not found</p>"
    
    try:
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
        html_string = f'''
            <div style="display:flex; flex-direction:column; gap:20px;">
                <div style="border:1px solid #ddd; padding:10px; border-radius:5px;">
                    <h5>Method 1: Direct Base64 Embed</h5>
                    <embed src="data:application/pdf;base64,{base64_pdf}" 
                           width="100%" 
                           height="400px" 
                           type="application/pdf">
                </div>
                
                <div style="border:1px solid #ddd; padding:10px; border-radius:5px;">
                    <h5>Method 2: Object Tag with Embed Fallback</h5>
                    <object data="data:application/pdf;base64,{base64_pdf}" 
                            type="application/pdf" 
                            width="100%" 
                            height="400px">
                        <embed src="data:application/pdf;base64,{base64_pdf}" 
                               type="application/pdf"
                               width="100%" 
                               height="400px" />
                    </object>
                </div>
                
                <div style="border:1px solid #ddd; padding:10px; border-radius:5px;">
                    <h5>Method 3: IFrame</h5>
                    <iframe src="data:application/pdf;base64,{base64_pdf}"
                            width="100%"
                            height="400px"
                            style="border: none;">
                    </iframe>
                </div>
                
                <div style="border:1px solid #ddd; padding:10px; border-radius:5px;">
                    <h5>Method 4: Google Docs Viewer</h5>
                    <iframe src="https://docs.google.com/viewer?url={file_path}&embedded=true"
                            width="100%"
                            height="400px"
                            style="border: none;">
                    </iframe>
                </div>
                
                <div style="border:1px solid #ddd; padding:10px; border-radius:5px;">
                    <h5>Method 5: PDF.js Viewer</h5>
                    <iframe src="https://mozilla.github.io/pdf.js/web/viewer.html?file=data:application/pdf;base64,{base64_pdf}"
                            width="100%"
                            height="400px"
                            style="border: none;">
                    </iframe>
                </div>
                
                <div style="border:1px solid #ddd; padding:10px; border-radius:5px;">
                    <h5>Method 6: Download Link</h5>
                    <a href="data:application/pdf;base64,{base64_pdf}" 
                       download="document.pdf" 
                       class="button"
                       style="display:inline-block; padding:10px 20px; background:#0066cc; color:white; text-decoration:none; border-radius:5px;">
                        Download PDF
                    </a>
                </div>
            </div>
        '''
        return html_string
    except Exception as e:
        return f"<p>Error loading PDF: {str(e)}</p>"

def main():
    st.title("PDF Viewer Test")
    st.markdown("Testing different methods of displaying PDFs in Streamlit")
    
    # File uploader for testing
    uploaded_file = st.file_uploader("Upload a PDF file for testing", type="pdf")
    
    if uploaded_file:
        # Save the uploaded file temporarily
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # Display PDF using multiple methods
        st.markdown(embed_pdf_base64("temp.pdf"), unsafe_allow_html=True)
        
        # Clean up
        os.remove("temp.pdf")
    else:
        # Use sample PDF if no file is uploaded
        sample_path = Path(__file__).parent / "sample.pdf"
        if sample_path.exists():
            st.markdown(embed_pdf_base64(str(sample_path)), unsafe_allow_html=True)
        else:
            st.warning("Please upload a PDF file to test the viewer.")

if __name__ == "__main__":
    main() 
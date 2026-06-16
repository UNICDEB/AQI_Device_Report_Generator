import streamlit as st
import pandas as pd
import zipfile
import tempfile
import shutil
import os
from datetime import datetime
from ydata_profiling import ProfileReport

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Device Data Profiling",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# FOLDERS
# --------------------------------------------------

UPLOAD_DIR = "uploads"
EXTRACT_DIR = "extracted"
RESULT_DIR = "results"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(EXTRACT_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

# --------------------------------------------------
# PREMIUM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.title {
    font-size:40px;
    font-weight:bold;
    color:#1565C0;
}

.subtitle {
    font-size:18px;
    color:gray;
}

.reportview-container {
    background: #f5f5f5;
}

.stButton button {
    width:100%;
    border-radius:10px;
    height:50px;
    font-size:18px;
}

.footer {
    position:fixed;
    bottom:0;
    width:100%;
    text-align:center;
    padding:10px;
    background:white;
    color:gray;
    border-top:1px solid #ddd;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="title">📊 Device Data Profiling Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Generate YData Profiling Reports for Multiple Devices</div>',
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# SESSION
# --------------------------------------------------

if "reports" not in st.session_state:
    st.session_state.reports = {}

# --------------------------------------------------
# FUNCTIONS
# --------------------------------------------------

def process_excel(file_path):

    device_id = os.path.splitext(
        os.path.basename(file_path)
    )[0]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    try:

        # Skip first 7 rows
        df = pd.read_excel(
            file_path,
            skiprows=7
        )

        profile = ProfileReport(
            df,
            title=f"{device_id} Data Report",
            explorative=True
        )

        html_name = f"{device_id}_{timestamp}.html"

        html_path = os.path.join(
            RESULT_DIR,
            html_name
        )

        profile.to_file(html_path)

        st.session_state.reports[device_id] = html_path

        return True

    except Exception as e:
        st.error(f"{device_id}: {e}")
        return False


def process_zip(zip_file):

    temp_zip = os.path.join(
        UPLOAD_DIR,
        zip_file.name
    )

    with open(temp_zip, "wb") as f:
        f.write(zip_file.read())

    with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
        zip_ref.extractall(EXTRACT_DIR)

    excel_files = []

    for root, dirs, files in os.walk(EXTRACT_DIR):

        for file in files:

            if file.endswith(".xlsx") or file.endswith(".xls"):

                excel_files.append(
                    os.path.join(root, file)
                )

    return excel_files


def clear_all():

    folders = [
        UPLOAD_DIR,
        EXTRACT_DIR,
        RESULT_DIR
    ]

    for folder in folders:

        if os.path.exists(folder):

            shutil.rmtree(folder)

        os.makedirs(folder)

    st.session_state.reports = {}

# --------------------------------------------------
# TABS
# --------------------------------------------------

tab1, tab2 = st.tabs(
    [
        "ZIP Upload",
        "Multiple Files Upload"
    ]
)

# --------------------------------------------------
# ZIP TAB
# --------------------------------------------------

with tab1:

    zip_file = st.file_uploader(
        "Upload ZIP File",
        type=["zip"]
    )

    if zip_file:

        if st.button(
            "🚀 Process ZIP",
            key="zip_process"
        ):

            files = process_zip(zip_file)

            progress = st.progress(0)

            total = len(files)

            with st.spinner(
                "Generating Reports..."
            ):

                for idx, file in enumerate(files):

                    process_excel(file)

                    progress.progress(
                        (idx + 1) / total
                    )

            st.success(
                f"{total} reports generated."
            )

# --------------------------------------------------
# MULTIPLE FILES
# --------------------------------------------------

with tab2:

    uploaded_files = st.file_uploader(
        "Upload Excel Files",
        type=["xlsx", "xls"],
        accept_multiple_files=True
    )

    if uploaded_files:

        if st.button(
            "🚀 Process Files",
            key="multi_process"
        ):

            progress = st.progress(0)

            total = len(uploaded_files)

            with st.spinner(
                "Generating Reports..."
            ):

                for idx, file in enumerate(uploaded_files):

                    temp_file = os.path.join(
                        UPLOAD_DIR,
                        file.name
                    )

                    with open(
                        temp_file,
                        "wb"
                    ) as f:

                        f.write(file.read())

                    process_excel(temp_file)

                    progress.progress(
                        (idx + 1) / total
                    )

            st.success(
                f"{total} reports generated."
            )

# --------------------------------------------------
# REPORT VIEWER
# --------------------------------------------------

st.divider()

st.subheader("Generated Reports")

if st.session_state.reports:

    selected_device = st.selectbox(
        "Select Device",
        list(
            st.session_state.reports.keys()
        )
    )

    html_file = st.session_state.reports[
        selected_device
    ]

    with open(
        html_file,
        "r",
        encoding="utf-8"
    ) as f:

        html_content = f.read()

    st.download_button(
        "⬇ Download Report",
        html_content,
        file_name=os.path.basename(
            html_file
        ),
        mime="text/html"
    )

    st.components.v1.html(
        html_content,
        height=900,
        scrolling=True
    )

else:

    st.info(
        "No reports generated yet."
    )

# --------------------------------------------------
# CLEAR BUTTON
# --------------------------------------------------

st.divider()

if st.button("🗑 Clear All"):

    clear_all()

    st.success(
        "All reports cleared."
    )

    st.rerun()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        Developed by Debabrata
    </div>
    """,
    unsafe_allow_html=True
)
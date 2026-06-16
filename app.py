# import streamlit as st
# import pandas as pd
# import zipfile
# import tempfile
# import shutil
# import os
# from datetime import datetime
# from ydata_profiling import ProfileReport

# # --------------------------------------------------
# # CONFIG
# # --------------------------------------------------

# st.set_page_config(
#     page_title="Device Data Profiling",
#     page_icon="📊",
#     layout="wide"
# )

# # --------------------------------------------------
# # FOLDERS
# # --------------------------------------------------

# UPLOAD_DIR = "uploads"
# EXTRACT_DIR = "extracted"
# RESULT_DIR = "results"

# os.makedirs(UPLOAD_DIR, exist_ok=True)
# os.makedirs(EXTRACT_DIR, exist_ok=True)
# os.makedirs(RESULT_DIR, exist_ok=True)

# # --------------------------------------------------
# # PREMIUM CSS
# # --------------------------------------------------

# st.markdown("""
# <style>

# .main {
#     background-color: #f5f7fb;
# }

# .title {
#     font-size:40px;
#     font-weight:bold;
#     color:#1565C0;
# }

# .subtitle {
#     font-size:18px;
#     color:gray;
# }

# .reportview-container {
#     background: #f5f5f5;
# }

# .stButton button {
#     width:100%;
#     border-radius:10px;
#     height:50px;
#     font-size:18px;
# }

# .footer {
#     position:fixed;
#     bottom:0;
#     width:100%;
#     text-align:center;
#     padding:10px;
#     background:white;
#     color:gray;
#     border-top:1px solid #ddd;
# }

# </style>
# """, unsafe_allow_html=True)

# # --------------------------------------------------
# # HEADER
# # --------------------------------------------------

# st.markdown(
#     '<div class="title">📊 Device Data Profiling Dashboard</div>',
#     unsafe_allow_html=True
# )

# st.markdown(
#     '<div class="subtitle">Generate YData Profiling Reports for Multiple Devices</div>',
#     unsafe_allow_html=True
# )

# st.divider()

# # --------------------------------------------------
# # SESSION
# # --------------------------------------------------

# if "reports" not in st.session_state:
#     st.session_state.reports = {}

# # --------------------------------------------------
# # FUNCTIONS
# # --------------------------------------------------

# def process_excel(file_path):

#     device_id = os.path.splitext(
#         os.path.basename(file_path)
#     )[0]

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

#     try:

#         # Skip first 7 rows
#         df = pd.read_excel(
#             file_path,
#             skiprows=7
#         )

#         profile = ProfileReport(
#             df,
#             title=f"{device_id} Data Report",
#             explorative=True
#         )

#         html_name = f"{device_id}_{timestamp}.html"

#         html_path = os.path.join(
#             RESULT_DIR,
#             html_name
#         )

#         profile.to_file(html_path)

#         st.session_state.reports[device_id] = html_path

#         return True

#     except Exception as e:
#         st.error(f"{device_id}: {e}")
#         return False


# def process_zip(zip_file):

#     temp_zip = os.path.join(
#         UPLOAD_DIR,
#         zip_file.name
#     )

#     with open(temp_zip, "wb") as f:
#         f.write(zip_file.read())

#     with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
#         zip_ref.extractall(EXTRACT_DIR)

#     excel_files = []

#     for root, dirs, files in os.walk(EXTRACT_DIR):

#         for file in files:

#             if file.endswith(".xlsx") or file.endswith(".xls"):

#                 excel_files.append(
#                     os.path.join(root, file)
#                 )

#     return excel_files


# def clear_all():

#     folders = [
#         UPLOAD_DIR,
#         EXTRACT_DIR,
#         RESULT_DIR
#     ]

#     for folder in folders:

#         if os.path.exists(folder):

#             shutil.rmtree(folder)

#         os.makedirs(folder)

#     st.session_state.reports = {}

# # --------------------------------------------------
# # TABS
# # --------------------------------------------------

# tab1, tab2 = st.tabs(
#     [
#         "ZIP Upload",
#         "Multiple Files Upload"
#     ]
# )

# # --------------------------------------------------
# # ZIP TAB
# # --------------------------------------------------

# with tab1:

#     zip_file = st.file_uploader(
#         "Upload ZIP File",
#         type=["zip"]
#     )

#     if zip_file:

#         if st.button(
#             "🚀 Process ZIP",
#             key="zip_process"
#         ):

#             files = process_zip(zip_file)

#             progress = st.progress(0)

#             total = len(files)

#             with st.spinner(
#                 "Generating Reports..."
#             ):

#                 for idx, file in enumerate(files):

#                     process_excel(file)

#                     progress.progress(
#                         (idx + 1) / total
#                     )

#             st.success(
#                 f"{total} reports generated."
#             )

# # --------------------------------------------------
# # MULTIPLE FILES
# # --------------------------------------------------

# with tab2:

#     uploaded_files = st.file_uploader(
#         "Upload Excel Files",
#         type=["xlsx", "xls"],
#         accept_multiple_files=True
#     )

#     if uploaded_files:

#         if st.button(
#             "🚀 Process Files",
#             key="multi_process"
#         ):

#             progress = st.progress(0)

#             total = len(uploaded_files)

#             with st.spinner(
#                 "Generating Reports..."
#             ):

#                 for idx, file in enumerate(uploaded_files):

#                     temp_file = os.path.join(
#                         UPLOAD_DIR,
#                         file.name
#                     )

#                     with open(
#                         temp_file,
#                         "wb"
#                     ) as f:

#                         f.write(file.read())

#                     process_excel(temp_file)

#                     progress.progress(
#                         (idx + 1) / total
#                     )

#             st.success(
#                 f"{total} reports generated."
#             )

# # --------------------------------------------------
# # REPORT VIEWER
# # --------------------------------------------------

# st.divider()

# st.subheader("Generated Reports")

# if st.session_state.reports:

#     selected_device = st.selectbox(
#         "Select Device",
#         list(
#             st.session_state.reports.keys()
#         )
#     )

#     html_file = st.session_state.reports[
#         selected_device
#     ]

#     with open(
#         html_file,
#         "r",
#         encoding="utf-8"
#     ) as f:

#         html_content = f.read()

#     st.download_button(
#         "⬇ Download Report",
#         html_content,
#         file_name=os.path.basename(
#             html_file
#         ),
#         mime="text/html"
#     )

#     st.components.v1.html(
#         html_content,
#         height=900,
#         scrolling=True
#     )

# else:

#     st.info(
#         "No reports generated yet."
#     )

# # --------------------------------------------------
# # CLEAR BUTTON
# # --------------------------------------------------

# st.divider()

# if st.button("🗑 Clear All"):

#     clear_all()

#     st.success(
#         "All reports cleared."
#     )

#     st.rerun()

# # --------------------------------------------------
# # FOOTER
# # --------------------------------------------------

# st.markdown(
#     """
#     <div class="footer">
#         Developed by Debabrata
#     </div>
#     """,
#     unsafe_allow_html=True
# )

##############################
# ## Version 2.0


import streamlit as st
from utils import *
from concurrent.futures import ThreadPoolExecutor
import os, time

st.set_page_config(page_title="Device Analytics Platform", layout="wide")

init_folders()

if "reports" not in st.session_state:
    st.session_state.reports = {}
if "logs" not in st.session_state:
    st.session_state.logs = []

theme = st.sidebar.selectbox("Theme", ["Light","Dark"])
apply_theme(theme)

st.title("📊 Device Analytics & Profiling Platform")

upload_mode = st.sidebar.radio("Upload Mode", ["ZIP Upload","Excel Upload"])

files_to_process = []

if upload_mode=="ZIP Upload":
    zip_file = st.file_uploader("Upload ZIP", type=["zip"])
    if zip_file:
        files_to_process = extract_zip_upload(zip_file)
else:
    uploaded = st.file_uploader("Upload Excel Files", type=["xlsx","xls"], accept_multiple_files=True)
    if uploaded:
        files_to_process = save_uploaded_files(uploaded)

if st.button("🚀 Process"):
    start=time.time()
    progress=st.progress(0)

    def worker(f):
        return process_excel(f)

    with ThreadPoolExecutor(max_workers=4) as ex:
        results=list(ex.map(worker, files_to_process))

    for i,r in enumerate(results):
        st.session_state.reports[r["device_id"]] = r["html"]
        st.session_state.logs.append(r)
        progress.progress((i+1)/len(results))

    create_archive()
    # st.balloons()
    st.success(f"Completed in {round(time.time()-start,2)} sec")

c1,c2,c3,c4=st.columns(4)
c1.metric("Devices", len(st.session_state.reports))
c2.metric("Reports", len(st.session_state.reports))
c3.metric("Logs", len(st.session_state.logs))
c4.metric("Archive", "Ready" if os.path.exists("archive/results_archive.zip") else "No")

if st.session_state.reports:
    dev=st.selectbox("Select Device", list(st.session_state.reports.keys()))
    html_path=st.session_state.reports[dev]

    with open(html_path,"r",encoding="utf-8") as f:
        html=f.read()

    st.download_button("Download Report", html, file_name=os.path.basename(html_path))
    st.components.v1.html(html,height=900,scrolling=True)

if os.path.exists("archive/results_archive.zip"):
    with open("archive/results_archive.zip","rb") as f:
        st.download_button("📦 Download All Reports",f.read(),"results_archive.zip")

if st.button("🗑 Clear Workspace"):
    clear_workspace()
    st.session_state.reports={}
    st.session_state.logs=[]
    st.rerun()

st.markdown("---")
st.markdown("### Processing Logs")
if st.session_state.logs:
    st.dataframe(st.session_state.logs,use_container_width=True)

st.markdown("---")
st.markdown("<center><b>Device Analytics & Profiling Platform</b><br>Engineered by Debabrata Doloi<br>© 2026 All Rights Reserved</center>", unsafe_allow_html=True)


#######################
# ## Version 3.0 - Refactored with utils.py
# import os
# import time
# import streamlit as st
# from utils import *

# # ==================================================
# # PAGE CONFIG
# # ==================================================
# st.set_page_config(
#     page_title="Device Analytics Platform", page_icon="📊", layout="wide"
# )

# # ==================================================
# # CSS STYLE OVERRIDES
# # ==================================================
# st.markdown(
#     """
# <style>
# div[data-testid="stProgressBar"] > div > div {
#     height: 20px;
#     border-radius: 20px;
# }
# .metric-card {
#     background: #ffffff;
#     padding: 15px;
#     border-radius: 12px;
# }
# .footer {
#     text-align: center;
#     color: gray;
#     font-size: 14px;
# }
# </style>
# """,
#     unsafe_allow_html=True,
# )

# # ==================================================
# # INITIALIZATION
# # ==================================================
# init_folders()

# if "reports" not in st.session_state:
#     st.session_state.reports = {}

# if "logs" not in st.session_state:
#     st.session_state.logs = []

# # ==================================================
# # SIDEBAR CONTROL PANEL
# # ==================================================
# with st.sidebar:
#     st.image(
#         "https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100
#     )
#     st.title("Control Panel")

#     theme = st.selectbox("Theme", ["Light", "Dark"])
#     apply_theme(theme)

#     upload_mode = st.radio("Upload Mode", ["ZIP Upload", "Excel Upload"])

#     st.divider()
#     st.subheader("Workspace")

#     if st.button("🗑 Clear Workspace", use_container_width=True):
#         clear_workspace()
#         st.session_state.reports = {}
#         st.session_state.logs = []
#         st.rerun()

# # ==================================================
# # APPLICATION HEADER
# # ==================================================
# st.title("📊 Device Analytics & Profiling Platform")
# st.caption("Generate YData Profiling Reports for Multiple Devices")

# # ==================================================
# # FILE UPLOADER REGION
# # ==================================================
# files_to_process = []

# if upload_mode == "ZIP Upload":
#     zip_file = st.file_uploader("Upload ZIP File", type=["zip"])
#     if zip_file:
#         files_to_process = extract_zip_upload(zip_file)
# else:
#     uploaded = st.file_uploader(
#         "Upload Excel Files", type=["xlsx", "xls"], accept_multiple_files=True
#     )
#     if uploaded:
#         files_to_process = save_uploaded_files(uploaded)

# # ==================================================
# # MULTI-THREADED PROCESSING ENGINE
# # ==================================================
# if st.button("🚀 Process"):

#     if len(files_to_process) == 0:
#         st.warning("Please upload files first.")
#         st.stop()

#     start_time = time.time()

#     progress_bar = st.progress(0)

#     status_box = st.empty()

#     total_files = len(files_to_process)

#     results = []

#     status_box.markdown("""
#     <div style="
#         padding:20px;
#         border-radius:12px;
#         background:#111827;
#         color:white;
#         text-align:center;
#     ">
#         <h3>⚙️ Initializing Report Generation...</h3>
#     </div>
#     """, unsafe_allow_html=True)

#     for index, file in enumerate(files_to_process):

#         try:

#             status_box.markdown(
#                 f"""
#                 <div style="
#                     padding:20px;
#                     border-radius:12px;
#                     background:#111827;
#                     color:white;
#                     text-align:center;
#                 ">
#                     <h3>⚙️ Processing Device</h3>
#                     <p>{index+1} / {total_files}</p>
#                     <p>{os.path.basename(file)}</p>
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )

#             result = process_excel(file)

#             results.append(result)

#             st.session_state.reports[
#                 result["device_id"]
#             ] = result["html"]

#             st.session_state.logs.append(result)

#             progress_bar.progress(
#                 (index + 1) / total_files
#             )

#         except Exception as e:

#             st.error(
#                 f"{os.path.basename(file)} : {str(e)}"
#             )

#     create_archive()

#     elapsed_time = round(
#         time.time() - start_time,
#         2
#     )

#     progress_bar.progress(1.0)

#     status_box.markdown(
#         f"""
#         <div style="
#             padding:20px;
#             border-radius:12px;
#             background:#065f46;
#             color:white;
#             text-align:center;
#         ">
#             <h2>✅ Processing Completed</h2>

#             <p>
#             Devices Processed :
#             {len(results)}
#             </p>

#             <p>
#             Total Time :
#             {elapsed_time} sec
#             </p>

#         </div>
#         """,
#         unsafe_allow_html=True
#     )

#     st.success(
#         f"{len(results)} reports generated successfully."
#     )
# # ==================================================
# # METRICS DASHBOARD
# # ==================================================
# st.divider()
# c1, c2, c3, c4 = st.columns(4)
# c1.metric("Devices", len(st.session_state.reports))
# c2.metric("Reports", len(st.session_state.reports))
# c3.metric("Logs", len(st.session_state.logs))
# c4.metric(
#     "Archive",
#     (
#         "Ready"
#         if os.path.exists("archive/results_archive.zip")
#         else "No"
#     ),
# )

# # ==================================================
# # INTERACTIVE REPORT VIEWER
# # ==================================================
# if st.session_state.reports:
#     st.divider()
#     st.subheader("Generated Reports")

#     selected_device = st.selectbox(
#         "Select Device", list(st.session_state.reports.keys())
#     )
#     html_path = st.session_state.reports[selected_device]

#     with open(html_path, "r", encoding="utf-8") as f:
#         html_content = f.read()

#     col1, col2 = st.columns([1, 1])
#     with col1:
#         st.download_button(
#             "⬇ Download Report",
#             html_content,
#             file_name=os.path.basename(html_path),
#         )
#     with col2:
#         if os.path.exists("archive/results_archive.zip"):
#             with open("archive/results_archive.zip", "rb") as f:
#                 st.download_button(
#                     "📦 Download All Reports",
#                     f.read(),
#                     "results_archive.zip"
#                 )

#     st.components.v1.html(html_content, height=900, scrolling=True)

# # ==================================================
# # DATA ENGINE PROCESSING LOGS
# # ==================================================
# st.divider()
# st.subheader("Processing Logs")

# if st.session_state.logs:
#     st.dataframe(st.session_state.logs, use_container_width=True)

# # ==================================================
# # PAGE FOOTER
# # ==================================================
# st.divider()
# st.markdown(
#     """
#     <div class="footer">
#     <b>Device Analytics & Profiling Platform</b><br>
#     Engineered by Debabrata Doloi<br>
#     © 2026 All Rights Reserved
#     </div>
#     """,
#     unsafe_allow_html=True,
# )

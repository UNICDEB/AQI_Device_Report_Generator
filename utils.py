
import pandas as pd, os, zipfile, shutil
from datetime import datetime
from ydata_profiling import ProfileReport

def init_folders():
    for d in ["uploads","results","archive","extracted"]:
        os.makedirs(d,exist_ok=True)

def apply_theme(theme):
    import streamlit as st
    if theme=="Dark":
        st.markdown("""<style>.stApp{background:#0e1117;color:white;}</style>""",unsafe_allow_html=True)

def save_uploaded_files(files):
    out=[]
    for f in files:
        p=os.path.join("uploads",f.name)
        with open(p,"wb") as fp:
            fp.write(f.read())
        out.append(p)
    return out

def extract_zip_upload(zip_file):
    zp=os.path.join("uploads",zip_file.name)
    with open(zp,"wb") as f:
        f.write(zip_file.read())
    with zipfile.ZipFile(zp) as z:
        z.extractall("extracted")

    files=[]
    for r,d,fs in os.walk("extracted"):
        for f in fs:
            if f.endswith((".xlsx",".xls")):
                files.append(os.path.join(r,f))
    return files

def process_excel(file_path):
    meta=pd.read_excel(file_path,header=None,nrows=6)
    device_id=str(meta.iloc[1,0]).split(":")[-1].strip() if len(meta)>1 else os.path.basename(file_path)

    df=pd.read_excel(file_path,skiprows=7)

    profile=ProfileReport(df,title=f"{device_id} Report",explorative=True)

    ts=datetime.now().strftime("%Y%m%d_%H%M%S")
    html=os.path.join("results",f"{device_id}_{ts}.html")

    profile.to_file(html)

    return {
        "device_id":device_id,
        "rows":len(df),
        "html":html,
        "status":"Success"
    }

def create_archive():
    archive="archive/results_archive.zip"
    with zipfile.ZipFile(archive,"w") as z:
        for f in os.listdir("results"):
            z.write(os.path.join("results",f),f)

def clear_workspace():
    for d in ["uploads","results","archive","extracted"]:
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)

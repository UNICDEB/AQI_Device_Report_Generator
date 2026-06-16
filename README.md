# 📊 Device Analytics & Profiling Platform

A professional Streamlit-based application for generating automated data profiling reports from multiple environmental monitoring device datasets. The platform supports both ZIP and individual Excel file uploads, automatically generates HTML profiling reports using YData Profiling, and provides an interactive dashboard for report viewing and management.

---

## 🚀 Features

### 📁 Data Upload Options
- Upload multiple Excel files (`.xlsx`, `.xls`)
- Upload a ZIP archive containing multiple Excel files
- Automatic extraction and processing of ZIP contents

### 📈 Automated Data Profiling
- Generates detailed HTML profiling reports using YData Profiling
- Processes each device dataset individually
- Automatically names reports using:
  
  ```text
  DeviceID_YYYYMMDD_HHMMSS.html
  ```

### 🔍 Device Metadata Extraction
Automatically extracts device information from the Excel file:

- Project Name
- Device ID
- Device Label
- Start Date
- Stop Date
- Interval

### 📊 Dashboard
- Total Devices Processed
- Total Reports Generated
- Processing Logs
- Archive Status

### 📄 Report Management
- View generated reports directly inside the web application
- Download individual HTML reports
- Download all generated reports as a ZIP archive

### 🎨 User Interface
- Light Theme
- Dark Theme
- Responsive Dashboard
- Interactive Report Viewer

### 🗂 Workspace Management
- Clear all uploaded files
- Clear generated reports
- Clear extracted ZIP contents
- Reset application state

---

## 📂 Project Structure

```text
Device_Analytics_Platform/
│
├── app.py
├── utils.py
├── requirements.txt
│
├── uploads/
│
├── extracted/
│
├── results/
│
├── archive/
│
└── README.md
```

---

## ⚙️ Installation

### 1. Clone or Download Project

```bash
git clone <repository_url>
cd Device_Analytics_Platform
```

Or simply extract the project ZIP.

---

### 2. Create Virtual Environment

#### Windows

```bash
python -m venv testenv
testenv\Scripts\activate
```

#### Linux / Mac

```bash
python3 -m venv testenv
source testenv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

Application will open automatically in your browser:

```text
http://localhost:8501
```

---

## 📋 Input File Format

The application expects device data in the following format:

| Row Number | Content |
|------------|----------|
| Row 1 | Project Information |
| Row 2 | Device ID |
| Row 3 | Device Label |
| Row 4 | Start Date |
| Row 5 | Stop Date |
| Row 6 | Interval |
| Row 7 | Blank |
| Row 8 | Column Headers |
| Row 9+ | Sensor Data |

The application automatically skips the first 7 rows and processes data starting from the header row.

---

## 📄 Generated Report Naming Convention

Generated reports are saved as:

```text
<DeviceID>_<Timestamp>.html
```

Example:

```text
MCT2408020_20260715_104530.html
```

---

## 📦 Report Archive

After processing all files, the application automatically creates:

```text
archive/results_archive.zip
```

containing all generated HTML reports.

---

## 🛠 Technologies Used

- Python 3.11+
- Streamlit
- Pandas
- OpenPyXL
- YData Profiling

---

## 📥 Required Python Packages

```text
streamlit
pandas
openpyxl
ydata-profiling
```

Install manually if needed:

```bash
pip install streamlit pandas openpyxl ydata-profiling
```

---

## 🔄 Processing Workflow

```text
Upload Files
      │
      ▼
Read Device Metadata
      │
      ▼
Load Sensor Data
      │
      ▼
Generate YData Report
      │
      ▼
Save HTML Report
      │
      ▼
Create ZIP Archive
      │
      ▼
Display Reports in Dashboard
```

---

## 📝 Processing Logs

The application maintains processing logs including:

- Device ID
- Number of Records
- Report Path
- Processing Status

---

## 🎯 Use Cases

- Air Quality Monitoring Devices
- Environmental Monitoring Systems
- IoT Sensor Networks
- Data Quality Assessment
- Dataset Validation
- Exploratory Data Analysis

---

## 🔒 Notes

- Excel files must contain valid tabular data.
- The first 7 rows are reserved for device metadata.
- Large datasets may require additional processing time.
- Generated reports are stored locally.

---

## 👨‍💻 Developed By

**Debabrata Doloi**

Device Analytics & Profiling Platform

© 2026 All Rights Reserved

---
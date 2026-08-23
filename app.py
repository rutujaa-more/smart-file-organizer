import streamlit as st
import zipfile
import hashlib
from io import BytesIO
from datetime import datetime
from collections import Counter
from pathlib import Path

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Smart File Organizer",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------------------------------------
# FILE CATEGORIES
# -------------------------------------------------
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf"],
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods"],
    "Presentations": [".ppt", ".pptx", ".odp"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".h", ".cs", ".php", ".sql", ".json"],
    "Executables": [".exe", ".msi", ".apk", ".dmg"],
}

CATEGORY_ICONS = {
    "Images": "🖼️",
    "Videos": "🎬",
    "Audio": "🎵",
    "Documents": "📄",
    "Spreadsheets": "📊",
    "Presentations": "📽️",
    "Archives": "📦",
    "Code": "💻",
    "Executables": "⚙️",
    "Others": "🗂️",
}

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def get_category(filename):
    extension = Path(filename).suffix.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category
    return "Others"


def get_file_hash(file_data):
    return hashlib.sha256(file_data).hexdigest()


def get_unique_filename(filename, existing_files):
    path = Path(filename)
    stem = path.stem
    suffix = path.suffix
    new_filename = filename
    counter = 1

    while new_filename in existing_files:
        new_filename = f"{stem}_{counter}{suffix}"
        counter += 1

    existing_files.add(new_filename)
    return new_filename


def find_duplicate_count(uploaded_files):
    hashes = set()
    duplicates = 0

    for uploaded_file in uploaded_files:
        file_hash = get_file_hash(uploaded_file.getvalue())
        if file_hash in hashes:
            duplicates += 1
        else:
            hashes.add(file_hash)

    return duplicates


# -------------------------------------------------
# CUSTOM CSS — WHIMSICAL DIGITAL DESK
# -------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Pacifico&display=swap');

    .stApp {
        background:
            radial-gradient(circle at 10% 5%, rgba(255, 218, 232, 0.85) 0, rgba(255, 218, 232, 0) 28%),
            radial-gradient(circle at 90% 10%, rgba(218, 226, 255, 0.9) 0, rgba(218, 226, 255, 0) 30%),
            linear-gradient(135deg, #fffafc 0%, #f8f5ff 48%, #f3f8ff 100%);
        color: #332f3d;
        font-family: 'DM Sans', sans-serif;
    }

    .main .block-container {
        max-width: 1120px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stHeader"] {
        background: rgba(255,255,255,0);
    }

    .hero {
        text-align: center;
        padding: 1.2rem 1rem 1.7rem;
    }

    .hero-badge {
        display: inline-block;
        padding: 0.42rem 0.9rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.75);
        border: 1px solid #eadff0;
        color: #8d6b9f;
        font-size: 0.86rem;
        font-weight: 700;
        box-shadow: 0 8px 25px rgba(85, 64, 110, 0.08);
    }

    .hero-title {
        margin: 0.8rem 0 0.35rem;
        font-size: clamp(2.4rem, 6vw, 4.3rem);
        line-height: 1.05;
        font-weight: 800;
        letter-spacing: -0.045em;
        color: #383242;
    }

    .hero-title span {
        color: #a66bb5;
    }

    .hero-subtitle {
        max-width: 700px;
        margin: 0 auto;
        color: #766f80;
        font-size: 1.08rem;
        line-height: 1.65;
    }

    .feature-card {
        min-height: 150px;
        padding: 1.35rem;
        border-radius: 24px;
        background: rgba(255,255,255,0.78);
        border: 1px solid #eee4f0;
        box-shadow: 0 14px 35px rgba(75, 54, 94, 0.08);
    }

    .feature-icon {
        font-size: 1.7rem;
    }

    .feature-title {
        margin: 0.35rem 0;
        font-size: 1.02rem;
        font-weight: 800;
        color: #433b4c;
    }

    .feature-text {
        margin: 0;
        color: #817889;
        line-height: 1.55;
        font-size: 0.9rem;
    }

    .section-title {
        margin: 1.8rem 0 0.75rem;
        font-size: 1.35rem;
        font-weight: 800;
        color: #433b4c;
    }

    .upload-shell {
        padding: 1.1rem;
        border-radius: 28px;
        background: rgba(255,255,255,0.78);
        border: 2px dashed #d9c8e2;
        box-shadow: 0 14px 35px rgba(75, 54, 94, 0.07);
    }

    .stats-card {
        padding: 1.1rem 0.8rem;
        text-align: center;
        border-radius: 22px;
        background: rgba(255,255,255,0.82);
        border: 1px solid #eee4f0;
        box-shadow: 0 10px 25px rgba(75, 54, 94, 0.07);
    }

    .stats-number {
        font-size: 2rem;
        font-weight: 800;
        color: #7d5a92;
    }

    .stats-label {
        color: #84798d;
        font-size: 0.85rem;
        font-weight: 600;
    }

    .category-pill {
        display: inline-block;
        margin: 0.25rem;
        padding: 0.55rem 0.85rem;
        border-radius: 999px;
        background: #f4ecfa;
        color: #715381;
        border: 1px solid #e5d7ee;
        font-weight: 700;
        font-size: 0.88rem;
    }

    .tip {
        padding: 1rem 1.15rem;
        border-radius: 18px;
        background: #fff7e8;
        border: 1px solid #f3dfb7;
        color: #765e34;
        margin: 0.7rem 0;
    }

    .success-box {
        padding: 1.2rem;
        border-radius: 22px;
        background: #eefaf3;
        border: 1px solid #cbe9d7;
        color: #35644a;
        text-align: center;
        font-weight: 700;
    }

    div.stButton > button {
        width: 100%;
        border: 0;
        border-radius: 18px;
        padding: 0.8rem 1rem;
        background: linear-gradient(135deg, #a96fba, #7f72c8);
        color: white;
        font-size: 1rem;
        font-weight: 800;
        box-shadow: 0 10px 24px rgba(127, 114, 200, 0.25);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 30px rgba(127, 114, 200, 0.32);
        color: white;
    }

    div.stDownloadButton > button {
        width: 100%;
        border-radius: 18px;
        border: 1px solid #cbb8d8;
        background: #fff;
        color: #654d72;
        font-weight: 800;
    }

    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.55);
        border-radius: 18px;
    }

    [data-testid="stExpander"] {
        border-radius: 18px;
        border: 1px solid #eadff0;
        background: rgba(255,255,255,0.65);
    }

    .footer {
        text-align: center;
        color: #978d9d;
        font-size: 0.82rem;
        padding: 2rem 0 0.5rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# HERO
# -------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">✨ your tiny digital decluttering assistant</div>
        <div class="hero-title">📁 Smart File <span>Organizer</span></div>
        <div class="hero-subtitle">
            A cute little corner for turning file chaos into calm.
            Upload your messy files, let Python sort them, and take home a tidy ZIP.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------
# FEATURE CARDS
# -------------------------------------------------
feature_cols = st.columns(3)

features = [
    ("🪄", "Automatic", "Files are recognized and sorted into the right categories for you."),
    ("🛡️", "Safe & gentle", "Your original files are never modified or overwritten."),
    ("🎀", "Ready to take home", "Download everything neatly packed into one organized ZIP."),
]

for col, (icon, title, text) in zip(feature_cols, features):
    with col:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <p class="feature-text">{text}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown('<div class="section-title">🧺 Give your messy files a little home</div>', unsafe_allow_html=True)

# -------------------------------------------------
# UPLOAD
# -------------------------------------------------
st.markdown('<div class="upload-shell">', unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "Drop your files here, or tap Browse",
    accept_multiple_files=True,
    help="You can upload multiple files at once.",
)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------
# ANALYSIS
# -------------------------------------------------
if uploaded_files:
    duplicate_count = find_duplicate_count(uploaded_files)

    categories = [get_category(file.name) for file in uploaded_files]
    category_count = Counter(categories)

    st.markdown(
        '<div class="section-title">🔎 A little peek at your file pile</div>',
        unsafe_allow_html=True,
    )

    stat_cols = st.columns(3)

    stats = [
        ("📄", str(len(uploaded_files)), "Files"),
        ("🗂️", str(len(category_count)), "Categories"),
        ("♻️", str(duplicate_count), "Duplicates"),
    ]

    for col, (icon, number, label) in zip(stat_cols, stats):
        with col:
            st.markdown(
                f"""
                <div class="stats-card">
                    <div>{icon}</div>
                    <div class="stats-number">{number}</div>
                    <div class="stats-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="section-title">🧸 What did I find?</div>',
        unsafe_allow_html=True,
    )

    pills = ""
    for category, count in category_count.items():
        icon = CATEGORY_ICONS.get(category, "🗂️")
        pills += f'<span class="category-pill">{icon} {category} · {count}</span>'

    st.markdown(pills, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">⚙️ Make it yours</div>',
        unsafe_allow_html=True,
    )

    setting_col1, setting_col2 = st.columns(2)

    with setting_col1:
        organize_by_date = st.checkbox(
            "📅 Create a date folder",
            value=True,
            help="Files will be placed under a YYYY-MM-DD folder based on the processing date.",
        )

    with setting_col2:
        detect_duplicates = st.checkbox(
            "♻️ Skip duplicate content",
            value=True,
            help="Files with identical SHA-256 content hashes are treated as duplicates.",
        )

    if duplicate_count > 0:
        st.markdown(
            f"""
            <div class="tip">
                🌼 I spotted <strong>{duplicate_count}</strong> duplicate file(s).
                They can be skipped automatically when you organize.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="section-title">✨ Ready to make things tidy?</div>',
        unsafe_allow_html=True,
    )

    if st.button("🪄 Organize My Files", use_container_width=True):
        zip_buffer = BytesIO()
        activity_log = []
        existing_files = set()
        file_hashes = set()
        duplicates_found = []
        processing_date = datetime.now().strftime("%Y-%m-%d")

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for uploaded_file in uploaded_files:
                filename = uploaded_file.name
                file_data = uploaded_file.getvalue()
                category = get_category(filename)

                if detect_duplicates:
                    file_hash = get_file_hash(file_data)

                    if file_hash in file_hashes:
                        duplicates_found.append(filename)
                        activity_log.append(
                            f"♻️ DUPLICATE SKIPPED: {filename}"
                        )
                        continue

                    file_hashes.add(file_hash)

                unique_filename = get_unique_filename(filename, existing_files)

                if unique_filename != filename:
                    activity_log.append(
                        f"✏️ RENAMED: {filename} → {unique_filename}"
                    )

                if organize_by_date:
                    folder_path = (
                        f"Organized_Files/{category}/{processing_date}/"
                    )
                else:
                    folder_path = f"Organized_Files/{category}/"

                final_path = folder_path + unique_filename

                zip_file.writestr(final_path, file_data)

                activity_log.append(
                    f"📁 ORGANIZED: {filename} → {final_path}"
                )

            log_header = [
                "SMART FILE ORGANIZER — ACTIVITY LOG",
                "=" * 50,
                f"Processed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"Uploaded files: {len(uploaded_files)}",
                f"Duplicates skipped: {len(duplicates_found)}",
                "",
                "ACTIVITY",
                "-" * 50,
            ]

            full_log = "\n".join(log_header + activity_log)

            zip_file.writestr(
                "Organized_Files/activity_log.txt",
                full_log,
            )

        zip_buffer.seek(0)

        organized_count = len(uploaded_files) - len(duplicates_found)

        st.markdown(
            f"""
            <div class="success-box">
                🎉 All tidy! {organized_count} file(s) are ready to go.
                <br>
                <span style="font-weight:500;">
                    Your originals stayed safe while I prepared a fresh organized ZIP.
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        result_cols = st.columns(2)

        with result_cols[0]:
            st.metric("✨ Organized", organized_count)

        with result_cols[1]:
            st.metric("♻️ Duplicates skipped", len(duplicates_found))

        if duplicates_found:
            with st.expander("♻️ Peek at skipped duplicates"):
                for duplicate in duplicates_found:
                    st.write(f"• {duplicate}")

        with st.expander("📝 Open the activity log"):
            for activity in activity_log:
                st.write(activity)

        st.download_button(
            label="🎀 Download My Organized Files",
            data=zip_buffer.getvalue(),
            file_name="organized_files.zip",
            mime="application/zip",
            use_container_width=True,
        )

else:
    st.markdown(
        """
        <div class="tip">
            💌 Tip: try uploading a few different file types together —
            for example a photo, PDF, spreadsheet, and Python file.
        </div>
        """,
        unsafe_allow_html=True,
    )

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown(
    """
    <div class="footer">
        Made with 🐍 Python + 🎈 Streamlit · A little less chaos, one folder at a time.
    </div>
    """,
    unsafe_allow_html=True,
)
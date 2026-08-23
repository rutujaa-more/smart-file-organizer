import streamlit as st
import zipfile
import io
from pathlib import Path
from collections import Counter


# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="Smart File Organizer",
    page_icon="📁",
    layout="wide"
)


# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 0;
}

.subtitle {
    text-align: center;
    font-size: 1.2rem;
    color: #808080;
    margin-bottom: 2rem;
}

.feature-box {
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #ddd;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# FILE CATEGORIES
# -------------------------------------------------

FILE_CATEGORIES = {
    "🖼️ Images": {
        ".jpg", ".jpeg", ".png", ".gif",
        ".bmp", ".svg", ".webp", ".tiff",
        ".ico", ".heic"
    },

    "🎬 Videos": {
        ".mp4", ".mkv", ".avi", ".mov",
        ".wmv", ".flv", ".webm", ".m4v"
    },

    "🎵 Audio": {
        ".mp3", ".wav", ".aac", ".flac",
        ".ogg", ".m4a", ".wma"
    },

    "📄 Documents": {
        ".pdf", ".doc", ".docx", ".txt",
        ".rtf", ".odt"
    },

    "📊 Spreadsheets": {
        ".xls", ".xlsx", ".csv", ".ods"
    },

    "📽️ Presentations": {
        ".ppt", ".pptx", ".odp", ".key"
    },

    "📦 Archives": {
        ".zip", ".rar", ".7z", ".tar",
        ".gz", ".bz2", ".xz"
    },

    "💻 Code": {
        ".py", ".js", ".ts", ".java",
        ".c", ".cpp", ".h", ".hpp",
        ".html", ".css", ".php",
        ".sql", ".json", ".xml",
        ".yaml", ".yml", ".sh"
    },

    "⚙️ Executables": {
        ".exe", ".msi", ".apk",
        ".dmg", ".deb", ".rpm"
    }
}


# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------

def get_category(filename):

    extension = Path(filename).suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():

        if extension in extensions:
            return category

    return "📁 Others"


def get_unique_filename(filename, existing_paths):

    path = Path(filename)

    if filename not in existing_paths:
        return filename

    counter = 1

    while True:

        new_name = (
            f"{path.stem}_{counter}"
            f"{path.suffix}"
        )

        if new_name not in existing_paths:
            return new_name

        counter += 1


def create_organized_zip(uploaded_files):

    zip_buffer = io.BytesIO()

    # Store filenames separately for each category
    used_names = {}

    with zipfile.ZipFile(
        zip_buffer,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zip_file:

        for uploaded_file in uploaded_files:

            category = get_category(
                uploaded_file.name
            )

            if category not in used_names:
                used_names[category] = set()

            filename = get_unique_filename(
                uploaded_file.name,
                used_names[category]
            )

            used_names[category].add(filename)

            zip_path = f"{category}/{filename}"

            zip_file.writestr(
                zip_path,
                uploaded_file.getvalue()
            )

    zip_buffer.seek(0)

    return zip_buffer


# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.markdown(
    '<div class="main-title">📁 Smart File Organizer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Upload your messy files and organize them automatically.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# -------------------------------------------------
# FEATURES
# -------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        """
        <div class="feature-box">
        <h3>⚡ Automatic</h3>
        <p>Files are categorized automatically based on their type.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        """
        <div class="feature-box">
        <h3>🛡️ Safe</h3>
        <p>Your original files are never modified or overwritten.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        """
        <div class="feature-box">
        <h3>📦 Download</h3>
        <p>Get your organized files as a ZIP archive instantly.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# -------------------------------------------------
# FILE UPLOADER
# -------------------------------------------------

uploaded_files = st.file_uploader(
    "📤 Upload your files",
    accept_multiple_files=True,
    help="Select multiple files and let the organizer do the rest."
)


# -------------------------------------------------
# FILE ANALYSIS
# -------------------------------------------------

if uploaded_files:

    st.subheader("🔍 File Analysis")

    file_data = []

    for uploaded_file in uploaded_files:

        category = get_category(
            uploaded_file.name
        )

        file_data.append({
            "File Name": uploaded_file.name,
            "Category": category,
            "Size (KB)": round(
                uploaded_file.size / 1024,
                2
            )
        })

    st.dataframe(
        file_data,
        use_container_width=True,
        hide_index=True
    )

    st.divider()


    # ---------------------------------------------
    # SUMMARY
    # ---------------------------------------------

    st.subheader("📊 Organization Summary")

    categories = [
        file["Category"]
        for file in file_data
    ]

    category_counts = Counter(categories)

    columns = st.columns(
        min(len(category_counts), 4)
    )

    for index, (category, count) in enumerate(
        category_counts.items()
    ):

        with columns[index % len(columns)]:

            st.metric(
                category,
                f"{count} file(s)"
            )


    st.divider()


    # ---------------------------------------------
    # ORGANIZE BUTTON
    # ---------------------------------------------

    if st.button(
        "🚀 Organize My Files",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "Organizing your files..."
        ):

            zip_buffer = create_organized_zip(
                uploaded_files
            )

        st.success(
            "🎉 Your files have been organized successfully!"
        )

        st.download_button(
            label="📦 Download Organized Files",
            data=zip_buffer,
            file_name="organized_files.zip",
            mime="application/zip",
            type="primary",
            use_container_width=True
        )


# -------------------------------------------------
# HOW IT WORKS
# -------------------------------------------------

st.divider()

st.subheader("⚙️ How It Works")

step1, step2, step3 = st.columns(3)

with step1:

    st.markdown(
        """
        ### 1️⃣ Upload

        Upload multiple files from your computer.
        """
    )

with step2:

    st.markdown(
        """
        ### 2️⃣ Analyze

        The system identifies each file type.
        """
    )

with step3:

    st.markdown(
        """
        ### 3️⃣ Organize

        Download your neatly organized ZIP file.
        """
    )


# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.divider()

st.caption(
    "Built with ❤️ using Python and Streamlit"
)
import os, re, json, random, tempfile, datetime, unicodedata, asyncio, base64
import pandas as pd, plotly.express as px
import streamlit as st
from fpdf import FPDF
import plotly.io as pio

DATA_FILE = "reportdata.json"
COURSE_FILE = "courses.csv"

# ------------------ Utility Functions ------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"teachers": [], "students": [], "reports": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_courses():
    if os.path.exists(COURSE_FILE):
        return pd.read_csv(COURSE_FILE)["course"].tolist()
    return []

def get_evaluation(score):
    if score >= 85:
        return random.choice(["Outstanding", "Excellent Performance", "Exceptional Mastery"])
    elif score >= 70:
        return random.choice(["Very Good", "Strong Understanding", "Commendable Progress"])
    elif score >= 55:
        return random.choice(["Satisfactory", "Developing Well", "Fair Effort"])
    else:
        return random.choice(["Needs Improvement", "Below Expectation", "Further Support Needed"])

# ------------------ PDF Generator ------------------

# ------------------ Chrome Setup for Kaleido ------------------
async def setup_chrome():
    try:
        # Launch Chromium to ensure it's downloaded (pyppeteer auto-installs if missing)
        from pyppeteer import chromium_downloader
        browser_fetcher = chromium_downloader.chromium_executable()
        os.environ["KALEIDO_CHROME_PATH"] = browser_fetcher
        print("✅ Chromium ready for Kaleido.")
    except Exception as e:
        print("⚠️ Chrome setup skipped:", e)

try:
    asyncio.get_event_loop().run_until_complete(setup_chrome())
except Exception as e:
    print("Chrome setup skipped:", e)

# ------------------ Safe Text Converter ------------------
def sanitize_text(text):
    """Convert unicode characters to Latin-1 safe text for FPDF."""
    if not isinstance(text, str):
        return str(text)
    replacements = {
        "—": "-", "–": "-", "•": "*", "“": '"', "”": '"', "‘": "'", "’": "'", "…": "...",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return unicodedata.normalize('NFKD', text).encode('latin-1', 'ignore').decode('latin-1')


# ------------------ PDF Generator ------------------
def create_pdf(student_name, reports, month_year):
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    # pdf.add_page()

    # --- Add School Logo (Top Right) ---
    logo_path = "edustemlablogo.png"  # make sure this file exists in same directory
    # if os.path.exists(logo_path):
    #     pdf.image(logo_path, x=250, y=8, w=35)  # adjust position/width as needed

    # --- Start Table Page ---
    pdf.set_auto_page_break(False)

    for course, info in reports.items():
        pdf.add_page()

        if os.path.exists(logo_path):
                pdf.image(logo_path, x=250, y=8, w=35)  # adjust position/width as needed
        # ---- Page Heading ----
        pdf.set_font("Helvetica", "B", 18)
        pdf.set_text_color(0, 51, 102)
        heading = f"{student_name}  -  {course}  Summary Table"
        pdf.cell(0, 12, sanitize_text(heading), ln=True, align="C")
        pdf.ln(6)

        # ---- Proficiency Header ----
        percentage = f"Proficiency: {info.get('percentage', '')}%"
        evaluation = f"Evaluation: {sanitize_text(get_evaluation(info['percentage']))}"
        monthline = f"{month_year}     |     {percentage}     |     {evaluation}"

        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, sanitize_text(monthline), ln=True, align="C")
        pdf.ln(10)

        # ---- Table Header ----
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_fill_color(210, 220, 255)
        headers = ["Course Topic(s)", "Course Objectives"]
        col_widths = [90, 180]

        for h, w in zip(headers, col_widths):
            pdf.cell(w, 10, sanitize_text(h), border=1, align="C", fill=True)
        pdf.ln()
        pdf.set_font("Helvetica", "", 10)

        # --- Split submissions by teachers so each block can be separated ---
        topic_blocks = []
        objective_blocks = []

        # Original stored format combines multiple: "Submitted by X:\n..." etc.
        raw_topics = info.get("topic", "")
        raw_objectives = info.get("objective", "")

        # Extract each submission block
        topic_parts = re.split(r"Submitted by ", raw_topics)
        obj_parts = re.split(r"Submitted by ", raw_objectives)

        # Clean blocks
        for part in topic_parts:
            if ":" in part:
                content = part.split(":", 1)[1].strip()
                topic_blocks.append(content)
        for part in obj_parts:
            if ":" in part:
                content = part.split(":", 1)[1].strip()
                objective_blocks.append(content)

        # Align block counts (if one list is shorter)
        max_blocks = max(len(topic_blocks), len(objective_blocks))
        while len(topic_blocks) < max_blocks:
            topic_blocks.append("")
        while len(objective_blocks) < max_blocks:
            objective_blocks.append("")

        line_height = 6

        # --- Render each teacher submission block WITH HORIZONTAL GROUP BORDER ---
        # --- Render each teacher submission block WITH SINGLE ROW BORDER ---
        for block_index in range(max_blocks):

            topic = sanitize_text(topic_blocks[block_index])
            objective = sanitize_text(objective_blocks[block_index])

            TABLE_X = pdf.l_margin
            COL1_W, COL2_W = col_widths
            COL1_X = TABLE_X
            COL2_X = TABLE_X + COL1_W
            TABLE_W = COL1_W + COL2_W

            line_height = 6

            cols = [topic, objective]
            wrapped_cols = []
            heights = []

            # ---- Wrap text for each column ----
            for i, text in enumerate(cols):
                width = col_widths[i] - 4
                lines = []

                for line in text.split("\n"):
                    words = line.split()
                    curr = ""
                    for w in words:
                        if pdf.get_string_width(curr + " " + w) <= width:
                            curr += " " + w
                        else:
                            lines.append(curr.strip())
                            curr = w
                    lines.append(curr.strip())
                wrapped_cols.append(lines)
                heights.append(len(lines) * line_height)

            max_height = max(heights)
            y_start = pdf.get_y()

            # ---- Draw SINGLE rectangle for the entire row ----
            pdf.rect(TABLE_X, y_start, TABLE_W, max_height)

            # ---- Vertical divider ----
            pdf.line(COL2_X, y_start, COL2_X, y_start + max_height)

            # ---- Text rendering ----
            x_positions = [COL1_X, COL2_X]

            for i, lines in enumerate(wrapped_cols):
                cell_width = col_widths[i]
                total_text_height = len(lines) * line_height
                y_text = y_start + (max_height - total_text_height) / 2
                x_text = x_positions[i]

                for j, line in enumerate(lines):
                    lw = pdf.get_string_width(line)
                    pdf.set_xy(x_text + (cell_width - lw) / 2, y_text + j * line_height)
                    pdf.cell(lw, line_height, line)

            # ---- Move to next row ----
            pdf.set_y(y_start + max_height)

            # ---- Add bottom separator ----
            # pdf.line(TABLE_X, pdf.get_y(), TABLE_X + TABLE_W, pdf.get_y())
            # pdf.ln(2)


    # Resume the rest of your create_pdf code normally


# End of modified section


    # --- New Page for Chart ---
    pdf.add_page()
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=250, y=8, w=35)  # adjust position/width as needed
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, "Course Proficiency Overview", ln=True, align="C")
    pdf.ln(8)

    # --- Chart Section ---
    # --- Chart Section ---
    df = pd.DataFrame([
        {"Course": c, "Proficiency": i["percentage"]}
        for c, i in reports.items()
    ])

    fig = px.bar(
        df,
        x="Course",
        y="Proficiency",
        text="Proficiency",  # show the values on top of bars
        color="Course",      # color each bar differently
        color_discrete_sequence=px.colors.qualitative.Bold,
    )

    # Make bars thicker and add % sign to text
    fig.update_traces(
        texttemplate="%{text}%",  # display % sign
        textposition="outside",   # show text outside bars
        marker_line_width=1.5     # optional: adds border to bars
    )

    # Layout adjustments for bigger bars and spacing
    fig.update_layout(
        yaxis=dict(title="Proficiency (%)", range=[0, 100]),
        xaxis=dict(title="Course"),
        bargap=0.3,  # gap between bars
        bargroupgap=0.1,
        uniformtext_minsize=10,
        uniformtext_mode='hide'
    )



    # --- Chart Section (safe version) ---
    # --- Chart Section (safe version) ---
    tmp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    try:
        fig.write_image(tmp_img.name, width=800, height=500, scale=2)
        pdf.image(tmp_img.name, x=40, w=220)
    except Exception as e:
        st.warning("⚠️ Unable to generate chart image. PDF created without chart.")
        st.error(f"Chart generation error: {e}")
    finally:
        try:
            os.remove(tmp_img.name)
        except Exception:
            pass


    # --- Save and Return PDF ---
    pdf_path = f"{student_name}_progress_report.pdf"
    pdf.output(pdf_path)
    return pdf_path

# ------------------ Streamlit App ------------------
st.set_page_config(page_title="📘 Student Progress Reports", layout="wide")

menu = st.sidebar.selectbox(
    "Menu",
    ["View & Download Report", "Generate Invoice", "Delete Report"]
)

# ------------------ PASSWORD PROTECTION ------------------
st.sidebar.markdown("## 📂 Load Data File (JSON)")
password = st.sidebar.text_input("Enter Admin Password", type="password",key="admin_pwd_main2")

if password != "helement":
    st.sidebar.warning("🔒 Enter correct password to access admin pages.")
    st.stop()

# ------------------ UPLOAD ANY JSON FILE ------------------
uploaded_json = st.sidebar.file_uploader(
    "Upload a JSON data file",
    type=["json"],
    accept_multiple_files=False
)

SESSION_DATA = None
SESSION_PATH = None

if uploaded_json:

    try:
        # Load ANY JSON file
        SESSION_DATA = json.load(uploaded_json)

        # Save a working copy to allow edits
        SESSION_PATH = "working_data.json"
        with open(SESSION_PATH, "w") as f:
            json.dump(SESSION_DATA, f, indent=4)

        st.sidebar.success("✅ JSON file loaded successfully!")

        # Allow download of the working data
        st.sidebar.download_button(
            label="⬇️ Download Current JSON",
            data=json.dumps(SESSION_DATA, indent=4),
            file_name="exported_data.json",
            mime="application/json"
        )

    except Exception as e:
        st.sidebar.error(f"❌ Invalid JSON file: {e}")
        st.stop()
data = SESSION_DATA if SESSION_DATA else {}


# else:
#     st.sidebar.info("📄 Please upload any JSON file to continue.")
#     st.stop()

# From this point forward, use SESSION_DATA instead of load_data()
data = SESSION_DATA

# ------------------ Add Report ------------------


# ------------------ Password-Protected Pages ------------------



if menu == "View & Download Report":

    if not SESSION_DATA:
        st.warning("📄 Please upload a JSON file to access reports.")
        st.stop()

    data = SESSION_DATA
    # Detect report months automatically
    months = [k for k in data.keys() if k not in ["students", "teachers", "reports"]]

    if not months:
        st.info("No student reports available yet.")
        st.stop()

    selected_month = st.selectbox("Select Month", months)

    all_students = list(data.get(selected_month, {}).keys())
    if not all_students:
        st.info("No student reports available yet.")
        st.stop()


    st.subheader("📥 View or Download Reports")
    col1, col2, col3 = st.columns([4,0.1,0.1])
    with col1:
        select_all = st.checkbox("Select All Students")

        if select_all:
            selected_students = all_students
        else:
            selected_students = st.multiselect("Select Students", all_students)
        # ---------------- MULTI-STUDENT LOOP ----------------
        all_reports_exist = True

        for student_name in selected_students:

            # st.markdown(f"# 🧑‍🎓 Student: **{student_name}**")

            reports = data[selected_month].get(student_name, {})

            if not reports:
                st.warning(f"⚠️ No reports found for {student_name}.")
                all_reports_exist = False
                continue  # continue to next student

            with st.expander(f"✏️ Edit Reports for {student_name}", expanded=False):

                # ---------------- EDIT FORM ----------------
                with st.form(f"edit_form_{student_name}"):

                    courses_to_delete = []

                    for course, info in reports.items():

                        st.markdown(f"## 📚 {course}")
                        delete_course = st.checkbox(f"🗑 Delete {course}", key=f"del_{student_name}_{course}")
                        courses_to_delete.append((course, delete_course))

                        # --- Split existing submissions ---
                        def split_submissions(raw_text):
                            subs = []
                            parts = re.split(r"Submitted by ", raw_text)
                            for p in parts:
                                if ":" in p:
                                    teacher, text = p.split(":", 1)
                                    subs.append((teacher.strip(), text.strip()))
                            return subs

                        topic_subs = split_submissions(info.get("topic", ""))
                        obj_subs = split_submissions(info.get("objective", ""))
                        sum_subs = split_submissions(info.get("summary", ""))

                        # Align lengths
                        max_len = max(len(topic_subs), len(obj_subs), len(sum_subs))
                        topic_subs += [("", "")] * (max_len - len(topic_subs))
                        obj_subs += [("", "")] * (max_len - len(obj_subs))
                        sum_subs += [("", "")] * (max_len - len(sum_subs))

                        new_submissions = []

                        # -------- EDIT BLOCK PER SUBMISSION --------
                        for i in range(max_len):

                            teacher = topic_subs[i][0] or obj_subs[i][0] or sum_subs[i][0] or f"Teacher {i+1}"
                            topic_text = topic_subs[i][1]
                            obj_text = obj_subs[i][1]
                            sum_text = sum_subs[i][1]

                            st.markdown(f"### ✏️ Submitted by: **{teacher}**")

                            colA, colB = st.columns(2)
                            with colA:
                                new_topic = st.text_area(
                                    f"Topic — {teacher}",
                                    topic_text,
                                    height=150,
                                    key=f"{student_name}_{course}_topic_{i}"
                                )
                            with colB:
                                new_obj = st.text_area(
                                    f"Objective — {teacher}",
                                    obj_text,
                                    height=150,
                                    key=f"{student_name}_{course}_obj_{i}"
                                )

                            new_sum = st.text_area(
                                f"Summary — {teacher}",
                                sum_text,
                                height=150,
                                key=f"{student_name}_{course}_sum_{i}"
                            )

                            delete_sub = st.checkbox(
                                f"❌ Delete submission from {teacher}",
                                key=f"del_{student_name}_{course}_sub_{i}"
                            )

                            if not delete_sub:
                                new_submissions.append({
                                    "teacher": teacher,
                                    "topic": new_topic,
                                    "objective": new_obj,
                                    "summary": new_sum
                                })

                            st.markdown("<hr>", unsafe_allow_html=True)

                        # -------- rebuild storage format --------
                        rebuilt_topic = ""
                        rebuilt_obj = ""
                        rebuilt_sum = ""

                        for sub in new_submissions:
                            rebuilt_topic += f"Submitted by {sub['teacher']}:\n{sub['topic']}\n\n"
                            rebuilt_obj += f"Submitted by {sub['teacher']}:\n{sub['objective']}\n\n"
                            rebuilt_sum += f"Submitted by {sub['teacher']}:\n{sub['summary']}\n\n"

                        info["topic"] = rebuilt_topic.strip()
                        info["objective"] = rebuilt_obj.strip()
                        info["summary"] = rebuilt_sum.strip()
                        info["month_year"] = selected_month

                    # SAVE BUTTON (per student)
                    save_btn = st.form_submit_button(f"💾 Save Changes for {student_name}")

                    if save_btn:
                        for course, to_del in courses_to_delete:
                            if to_del:
                                del data[selected_month][student_name][course]
                    
                        with open(SESSION_PATH, "w") as f:
                            json.dump(data, f, indent=4)
                        SESSION_DATA = data

                        st.success(f"Saved changes for {student_name}!")

            # ---------------- PDF PREVIEW (PER STUDENT) ----------------
            # if reports:
            #     month_year = next(iter(reports.values())).get("month_year", "Unknown")

            #     # Generate the PDF for preview only
            #     preview_path = create_pdf(student_name, reports, month_year)

            #     with open(preview_path, "rb") as f:
            #         pdf_bytes = f.read()

            #     st.markdown(f"### 📄 Preview PDF for **{student_name} ({month_year})**")
            #     st.download_button(
            #         f"🔍 Download Preview PDF — {student_name}",
            #         data=pdf_bytes,
            #         file_name=f"{student_name.replace(' ', '_')}_{month_year.replace(' ', '_')}.pdf",
            #         mime="application/pdf",
            #         key=f"preview_{student_name}"
            #     )

            #     # Streamlit iframe preview
            #     base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")
            #     pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600"></iframe>'
            #     st.markdown(pdf_display, unsafe_allow_html=True)



        # ---------------- ZIP DOWNLOAD FOR ALL SELECTED STUDENTS ----------------
        import zipfile
        import io

        if st.button("📦 Download All PDFs for Selected Students"):

            zip_buf = io.BytesIO()

            with zipfile.ZipFile(zip_buf, "w") as zipf:

                for student_name in selected_students:

                    reports = data[selected_month].get(student_name, {})
                    if not reports:
                        continue

                    # month-year from first course
                    month_year = selected_month

                    # generate PDF
                    pdf_path = create_pdf(student_name, reports, month_year)

                    # read PDF
                    with open(pdf_path, "rb") as f:
                        pdf_bytes = f.read()

                    # format filename
                    clean_name = student_name.replace(" ", "_")
                    clean_month = month_year.replace(" ", "_")
                    file_name = f"{clean_name}_{clean_month}.pdf"

                    zipf.writestr(file_name, pdf_bytes)

            zip_buf.seek(0)


            st.download_button(
                "⬇️ Download ZIP of All PDFs",
                data=zip_buf,
                file_name="student_reports.zip",
                mime="application/zip"
            )


    # ------------------ Delete Report ------------------
# ------------------ Delete Multiple Reports ------------------
elif menu == "Delete Report":

    if not SESSION_DATA:
        st.warning("📄 Please upload a JSON file to access reports.")
        st.stop()

    st.header("🗑️ Delete Student Reports")

    with st.form("delete_multiple_form"):
        months = [k for k in data.keys() if k not in ["students","teachers","reports"]]

        if not months:
            st.info("No reports available to delete.")
            st.info("No reports available to delete.")
        else:
            months = [k for k in data.keys() if k not in ["students","teachers","reports"]]

            selected_month = st.selectbox("Select Month", months)

            month_year = selected_month

            students = list(data[selected_month].keys())
            students_to_delete = st.multiselect("Select Student(s) to Delete", students)

            confirm_delete = st.form_submit_button("🚮 Delete Selected Reports")

            if confirm_delete:
                if not students_to_delete:
                    st.warning("Please select at least one student to delete.")
                else:
                    for s in students_to_delete:
                        if s in data["reports"]:
                            del data[selected_month][s]
                    with open(SESSION_PATH, "w") as f:
                        json.dump(data, f, indent=4)
                    SESSION_DATA = data

                    st.warning(f"🗑️ Deleted reports for: {', '.join(students_to_delete)}.")

    # ------------------ Delete All Generated Progress Report PDFs ------------------
    st.markdown("---")
    st.subheader("🗑️ Delete All Progress Report PDFs in Folder")

    delete_all_pdfs = st.button("🚨 Delete All Progress Report PDFs", key="delete_all_pdfs_button")
    if delete_all_pdfs:
        pdf_files = [f for f in os.listdir() if f.lower().endswith(".pdf") and "progress_report" in f.lower()]
        if not pdf_files:
            st.info("ℹ️ No progress report PDF files found in the current folder.")
        else:
            for pdf_file in pdf_files:
                try:
                    os.remove(pdf_file)
                except Exception as e:
                    st.error(f"⚠️ Could not delete {pdf_file}: {e}")
            st.success(f"✅ Deleted {len(pdf_files)} progress report PDF file(s) from the folder.")


    # ------------------ Student & Teacher Management ------------------
    st.sidebar.markdown("---")
    manage_toggle = st.sidebar.selectbox(
        "Add|Delete here",
        ["Choose", "Students", "Teachers"]
    )

    data = SESSION_DATA  # make sure we have the latest data


    # ------------------ Manage Teachers ------------------
    if manage_toggle == "Teachers":
        st.subheader("📝 Teacher Management")
        with st.form("teacher_form"):
            # Add new teacher
            new_teacher = st.text_input("Enter New Teacher Name")
            add_teacher_btn = st.form_submit_button("➕ Add Teacher")
            if add_teacher_btn:
                if not new_teacher.strip():
                    st.error("⚠️ Teacher name cannot be empty.")
                elif any(t["teacher"] == new_teacher.strip() for t in data.get("teachers", [])):
                    st.warning(f"⚠️ {new_teacher} already exists.")
                else:
                    data.setdefault("teachers", []).append({"teacher": new_teacher.strip(), "telegram_id": ""})
                    with open(SESSION_PATH, "w") as f:
                        json.dump(data, f, indent=4)
                    SESSION_DATA = data

                    st.success(f"✅ Added teacher: {new_teacher.strip()}")

            # Delete existing teachers using selectbox
            teachers = [t["teacher"] for t in data.get("teachers", [])]
            if teachers:
                del_teachers = st.multiselect("Select Teacher(s) to Delete", teachers)
                del_teacher_btn = st.form_submit_button("🗑️ Delete Selected Teacher(s)")
                if del_teacher_btn:
                    if not del_teachers:
                        st.warning("⚠️ Select at least one teacher to delete.")
                    else:
                        data["teachers"] = [t for t in data.get("teachers", []) if t["teacher"] not in del_teachers]
                        with open(SESSION_PATH, "w") as f:
                            json.dump(data, f, indent=4)
                        SESSION_DATA = data

                        st.success(f"🗑️ Deleted teacher(s): {', '.join(del_teachers)}")
            else:
                st.info("ℹ️ No teachers available to delete.")

    # ------------------ Manage Students ------------------
    elif manage_toggle == "Students":
        st.subheader("📝 Student Management")
        with st.form("student_form"):
            # Add new student
            new_student = st.text_input("Enter New Student Name")
            add_student_btn = st.form_submit_button("➕ Add Student")
            if add_student_btn:
                if not new_student.strip():
                    st.error("⚠️ Student name cannot be empty.")
                elif new_student in data.get("students", []):
                    st.warning(f"⚠️ {new_student} already exists.")
                else:
                    data.setdefault("students", []).append(new_student.strip())
                    with open(SESSION_PATH, "w") as f:
                        json.dump(data, f, indent=4)
                    SESSION_DATA = data

                    st.success(f"✅ Added student: {new_student.strip()}")

            # Delete existing students using selectbox
            students = data.get("students", [])
            if students:
                del_students = st.multiselect("Select Student(s) to Delete", students)
                del_student_btn = st.form_submit_button("🗑️ Delete Selected Student(s)")
                if del_student_btn:
                    if not del_students:
                        st.warning("⚠️ Select at least one student to delete.")
                    else:
                        for s in del_students:
                            if s in data["students"]:
                                data["students"].remove(s)
                                # optionally remove their reports too
                                for month in data:
                                    if month not in ["students","teachers","reports"]:
                                        if s in data[month]:
                                            del data[month][s]
                        with open(SESSION_PATH, "w") as f:
                            json.dump(data, f, indent=4)
                        SESSION_DATA = data

                        st.success(f"🗑️ Deleted student(s): {', '.join(del_students)}")
            else:
                st.info("ℹ️ No students available to delete.")


elif menu == "Generate Invoice":

    # ------------------ Session State ------------------
    if "invoice_items" not in st.session_state:
        st.session_state.invoice_items = [
            {"description": "", "duration": "", "amount": 0}
        ]

    imageurl = "logoedustemlab.png"

    # ------------------ Header ------------------
    col_logo, col_mid, col_title = st.columns([0.6, 2.4, 1])
    with col_logo:
        st.image(imageurl)
    with col_title:
        st.header(":blue[INVOICE]")

    col_left, col_right = st.columns(2)
    with col_left:
        st.write("**eduSTEMlab**")
        st.write("Online STEM for Kids")
        st.write("Lagos, Nigeria")
        st.write("")
        st.write("**Bill To:**")

    # ------------------ Customer Info ------------------
    col_b1, col_b2, col_b3 = st.columns([2, 1, 1])

    with col_b1:
        customer = st.text_input("Customer", placeholder="Customer Name", label_visibility="collapsed")
        adress = st.text_input("Email", placeholder="Email Address", label_visibility="collapsed")

    with col_b2:
        st.write("**Invoice#**")
        st.write("")
        st.write("**Invoice Date**")
        st.write("")
        st.write("**Due Date**")

    with col_b3:
        invoice_num = st.text_input("Invoice No", label_visibility="collapsed")

        invoice_date = st.date_input("Invoice Date", label_visibility="collapsed")
        invoice_date = f"{invoice_date.day} {invoice_date.strftime('%b')} {invoice_date.year}"

        due_date = st.date_input("Due Date", label_visibility="collapsed")
        due_date = f"{due_date.day} {due_date.strftime('%b')} {due_date.year}"

    st.divider()
    st.markdown("### 🧾 Invoice Items")

    # ------------------ Invoice Items ------------------
    for i, item in enumerate(st.session_state.invoice_items):

        col_d, col_t, col_a, col_x = st.columns([3, 1.2, 1.2, 0.5])

        with col_d:
            item["description"] = st.text_area(
                f"Description {i+1}",
                value=item["description"],
                height=80,
                key=f"desc_{i}"
            )

        with col_t:
            item["duration"] = st.text_input(
                f"Duration {i+1}",
                value=item["duration"],
                key=f"dur_{i}"
            )

        with col_a:
            item["amount"] = st.number_input(
                f"Amount {i+1}",
                min_value=0,
                value=item["amount"],
                key=f"amt_{i}"
            )

        with col_x:
            if st.button("❌", key=f"remove_{i}"):
                st.session_state.invoice_items.pop(i)
                st.rerun()

        st.divider()

    # ------------------ Add Item ------------------
    if st.button("➕ Add Another Item"):
        st.session_state.invoice_items.append(
            {"description": "", "duration": "", "amount": 0}
        )
        st.rerun()

    # ------------------ Totals ------------------
    total_amount = sum(item["amount"] for item in st.session_state.invoice_items)

    col_pay, col_total = st.columns(2)
    with col_pay:
        st.write("**Payment Info**")
        st.write("Acc Name: Sabbath Academy")
        st.write("Acc Number: 1310986136")
        st.write("Bank Name: Zenith Bank")

    with col_total:
        st.write("**Payment Due:**")
        st.header(f"#{total_amount:,}")

    # ------------------ PDF Generator ------------------
    def generate_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Courier", size=12)

        col1x, col1y = 10, 25
        # Layout constants (MUST exist)
        colw = 90      # column width
        colh = 8       # row height

        pdf.image(imageurl, x=col1x, y=col1y - 8, w=25)

        pdf.set_font("Courier", size=22, style="B")
        pdf.set_xy(col1x + 125, col1y)
        pdf.cell(60, 10, "INVOICE")

        pdf.set_font("Courier", size=12, style="B")
        pdf.set_xy(col1x, col1y + 20)
        pdf.cell(90, 8, "eduSTEMlab")

        pdf.set_xy(col1x, col1y + 30)
        pdf.cell(90, 8, "Online STEM for Kids")

        pdf.set_xy(col1x, col1y + 40)
        pdf.cell(90, 8, "Lagos, Nigeria")

        pdf.set_xy(col1x, col1y + 70)
        pdf.cell(90, 8, "BILL TO:")

        pdf.set_xy(col1x, col1y + 80)
        pdf.cell(90, 8, customer)

        pdf.set_xy(col1x, col1y + 90)
        pdf.cell(90, 8, adress)

        pdf.set_xy(col1x + 120, col1y + 80)
        pdf.cell(70, 8, f"Invoice#: {invoice_num}")

        pdf.set_xy(col1x + 120, col1y + 90)
        pdf.cell(70, 8, f"Invoice Date: {invoice_date}")

        # Table Header
        pdf.set_xy(col1x, col1y + 120)
        pdf.cell(90, 8, "DESCRIPTION")

        pdf.set_xy(col1x + 105, col1y + 120)
        pdf.cell(30, 8, "DURATION", align="C")

        pdf.set_xy(col1x + 145, col1y + 120)
        pdf.cell(30, 8, "AMOUNT", align="C")

        pdf.line(col1x, col1y + 130, col1x + 190, col1y + 130)

        y = col1y + 132

        for item in st.session_state.invoice_items:
            start_y = y

            pdf.set_xy(col1x, y)
            pdf.multi_cell(90, 8, item["description"])
            height = pdf.get_y() - start_y

            pdf.set_xy(col1x + 110, start_y)
            pdf.cell(30, height, item["duration"])

            pdf.set_xy(col1x + 150, start_y)
            pdf.cell(30, height, f'#{item["amount"]:,}')

            y += height

        # ------------------ PAYMENT INFORMATION ------------------
        info_y = y + 10

        # pdf.set_font("Courier", size=12, style="B")
        pdf.set_xy(col1x, info_y)
        pdf.cell(colw, colh, "PAYMENT INFORMATION", ln=True)

        # pdf.set_font("Courier", size=12)
        pdf.set_xy(col1x, info_y + 7)
        pdf.cell(colw, colh, "Acc Name: Sabbath Academy", ln=True)

        pdf.set_xy(col1x, info_y + 14)
        pdf.cell(colw, colh, "Acc Number: 1310986136", ln=True)

        pdf.set_xy(col1x, info_y + 21)
        pdf.cell(colw, colh, "Bank Name: Zenith Bank", ln=True)

        # ------------------ PAYMENT DUE LABEL ------------------
        pdf.set_font("Courier", size=12, style="B")
        pdf.set_xy(col1x + 120, info_y)
        pdf.cell(colw, colh, "PAYMENT DUE", ln=True)


        pdf.set_xy(col1x + 120, y + 20)
        pdf.set_font("Times", size=20, style="B")
        pdf.cell(70, 10, f"#{total_amount:,}")

        filename = f"invoice_{invoice_num}.pdf"
        pdf.output(filename)
        return filename


    # ------------------ Download / View ------------------
    pdf_file = None
    if customer and adress and invoice_num:
        pdf_file = generate_pdf()

    if pdf_file:
        with open(pdf_file, "rb") as f:
            pdf_data = f.read()

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            st.download_button(
                "📥 Download PDF",
                data=pdf_data,
                file_name="invoice.pdf",
                mime="application/pdf"
            )

        with col_btn2:
            if st.button("👁 View Invoice"):
                pdf_base64 = base64.b64encode(pdf_data).decode()
                st.markdown(
                    f'<embed src="data:application/pdf;base64,{pdf_base64}" width="100%" height="600px"/>',
                    unsafe_allow_html=True
                )

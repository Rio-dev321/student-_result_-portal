
import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

st.set_page_config(
    page_title="Leeds Student Result Portal",
    page_icon="🎓",
    layout="wide"
)

# Fictional sample data for testing only
students = [
    ("LR001", "Ayaan Ahmed", "Imran Ahmed", 438),
    ("LR002", "Hassan Ali", "Tariq Ali", 412),
    ("LR003", "Zainab Khan", "Usman Khan", 461),
    ("LR004", "Muhammad Hamza", "Bilal Hussain", 389),
    ("LR005", "Fatima Noor", "Asif Mahmood", 447),
    ("LR006", "Abdullah Shah", "Nadeem Shah", 376),
    ("LR007", "Areeba Malik", "Faisal Malik", 429),
    ("LR008", "Ibrahim Qureshi", "Javed Qureshi", 405),
    ("LR009", "Hira Siddiqui", "Kamran Siddiqui", 472),
    ("LR010", "Usman Raza", "Shahid Raza", 358),
    ("LR011", "Maryam Iqbal", "Rashid Iqbal", 433),
    ("LR012", "Ahmad Hassan", "Sajjad Hassan", 397),
    ("LR013", "Laiba Tariq", "Tariq Mehmood", 456),
    ("LR014", "Daniyal Sheikh", "Adnan Sheikh", 421),
    ("LR015", "Maham Javed", "Javed Akhtar", 382),
    ("LR016", "Saad Farooq", "Farooq Ahmed", 445),
    ("LR017", "Anaya Khalid", "Khalid Mehmood", 468),
    ("LR018", "Ali Raza", "Raza Hussain", 344),
    ("LR019", "Eman Fatima", "Waqas Ali", 414),
    ("LR020", "Rayyan Aslam", "Aslam Pervez", 401),
    ("LR021", "Ayesha Imran", "Imran Bashir", 479),
    ("LR022", "Talha Yousaf", "Yousaf Khan", 365),
    ("LR023", "Iqra Naveed", "Naveed Akram", 442),
    ("LR024", "Huzaifa Butt", "Shabbir Butt", 390),
    ("LR025", "Minahil Zahid", "Zahid Iqbal", 427),
    ("LR026", "Omar Farhan", "Farhan Latif", 408),
    ("LR027", "Sana Waheed", "Waheed Akhtar", 453),
    ("LR028", "Bilal Arshad", "Arshad Ali", 371),
    ("LR029", "Alina Saeed", "Saeed Ahmed", 436),
    ("LR030", "Mohsin Abbas", "Abbas Hussain", 399),
    ("LR031", "Dua Rehman", "Rehman Ali", 466),
    ("LR032", "Shahzaib Malik", "Nisar Malik", 352),
    ("LR033", "Noor ul Ain", "Aminullah Khan", 418),
    ("LR034", "Arham Siddiq", "Sajid Siddiq", 386),
    ("LR035", "Kinza Shahid", "Shahid Mehmood", 444),
    ("LR036", "Faraz Ahmed", "Ahmed Nawaz", 407),
    ("LR037", "Mishal Asif", "Asif Rauf", 459),
    ("LR038", "Sameer Ilyas", "Ilyas Ahmed", 378),
    ("LR039", "Zoya Faisal", "Faisal Karim", 431),
    ("LR040", "Kashif Mehmood", "Mehmood Akram", 393),
    ("LR041", "Mehak Riaz", "Riaz Hussain", 451),
    ("LR042", "Taha Jamil", "Jamil Ahmed", 423),
]

TOTAL = 500

def get_grade(percentage):
    if percentage >= 80:
        return "A+"
    elif percentage >= 70:
        return "A"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    elif percentage >= 40:
        return "D"
    return "F"

df = pd.DataFrame(
    students,
    columns=[
        "Roll Number",
        "Student Name",
        "Father Name",
        "Obtained Marks"
    ]
)

df["Total Marks"] = TOTAL
df["Percentage"] = (
    df["Obtained Marks"] / TOTAL * 100
).round(1)
df["Grade"] = df["Percentage"].apply(get_grade)

st.title("🎓 Leeds School and College")
st.subheader("Student Result Portal")
st.info(
    "DEMO APPLICATION — All students and results are fictional."
)

st.markdown("### 🔎 Check Student Result")

with st.form("result_form"):
    roll = st.text_input(
        "Enter Roll Number",
        placeholder="Example: LR001"
    ).strip().upper()

    name = st.text_input(
        "Enter Student Name (optional)",
        placeholder="Example: Ayaan Ahmed"
    ).strip()

    submitted = st.form_submit_button(
        "Check Result",
        type="primary"
    )

if submitted:
    if not roll:
        st.warning("Please enter a roll number.")
    else:
        result = df[df["Roll Number"] == roll]

        if name:
            result = result[
                result["Student Name"].str.lower()
                == name.lower()
            ]

        if result.empty:
            st.error(
                "No matching result found. "
                "Check the roll number and student name."
            )
        else:
            student = result.iloc[0]

            st.success("Result found!")

            c1, c2, c3 = st.columns(3)
            c1.metric(
                "Obtained Marks",
                f"{student['Obtained Marks']}/{TOTAL}"
            )
            c2.metric(
                "Percentage",
                f"{student['Percentage']}%"
            )
            c3.metric("Grade", student["Grade"])

            st.markdown("### 📄 Student Details")
            st.write("**Student Name:**", student["Student Name"])
            st.write("**Father Name:**", student["Father Name"])
            st.write("**Roll Number:**", student["Roll Number"])
            st.write("**Total Marks:**", TOTAL)

            # Create downloadable PDF
            pdf_buffer = BytesIO()
            pdf = canvas.Canvas(pdf_buffer, pagesize=A4)
            width, height = A4

            pdf.setTitle("Student Result - Demo")
            pdf.setFont("Helvetica-Bold", 18)
            pdf.drawCentredString(
                width / 2, height - 65,
                "LEEDS SCHOOL AND COLLEGE"
            )

            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawCentredString(
                width / 2, height - 95,
                "STUDENT RESULT CARD"
            )

            pdf.setFont("Helvetica", 10)
            pdf.drawCentredString(
                width / 2, height - 115,
                "FICTIONAL TEST DATA - NOT AN OFFICIAL RECORD"
            )

            y = height - 165
            details = [
                ("Student Name", student["Student Name"]),
                ("Father Name", student["Father Name"]),
                ("Roll Number", student["Roll Number"]),
                ("Obtained Marks", str(student["Obtained Marks"])),
                ("Total Marks", str(TOTAL)),
                ("Percentage", f"{student['Percentage']}%"),
                ("Grade", student["Grade"]),
            ]

            for label, value in details:
                pdf.setFont("Helvetica-Bold", 12)
                pdf.drawString(75, y, label + ":")
                pdf.setFont("Helvetica", 12)
                pdf.drawString(230, y, str(value))
                y -= 30

            pdf.setFont("Helvetica-Oblique", 9)
            pdf.drawCentredString(
                width / 2, 70,
                "Sample result generated for portal testing only."
            )

            pdf.save()
            pdf_buffer.seek(0)

            safe_roll = student["Roll Number"]
            st.download_button(
                label="⬇️ Download Result PDF",
                data=pdf_buffer.getvalue(),
                file_name=f"result_{safe_roll}.pdf",
                mime="application/pdf"
            )

st.divider()
st.markdown("### 📚 Demo Student Records")
st.caption("These 42 fictional records are visible for testing.")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.caption("For testing and educational use only.")

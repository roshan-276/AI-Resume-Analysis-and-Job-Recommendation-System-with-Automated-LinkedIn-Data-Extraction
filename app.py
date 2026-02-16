from flask import Flask, render_template, request, send_file
import os
import random
from werkzeug.utils import secure_filename
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

app = Flask(__name__)

UPLOAD_FOLDER = "uploads/resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# --------- Resume Analyzer Logic ----------
def analyze_resume(filename):
    score = random.randint(75, 95)

    summary = {
        "Technical Skills": [
            "Strong understanding of core programming concepts",
            "Knowledge of Python, Web Development and Databases",
            "Familiar with modern development tools"
        ],
        "Soft Skills": [
            "Good communication abilities",
            "Strong analytical thinking",
            "Problem-solving mindset"
        ],
        "Experience Level": [
            "Suitable for entry-level positions",
            "Capable of handling real-world projects",
            "Quick learner and adaptable"
        ],
        "Areas of Improvement": [
            "Add measurable achievements",
            "Include certifications",
            "Enhance project descriptions"
        ]
    }

    jobs = [
        "Python Developer",
        "Web Developer",
        "Software Engineer",
        "Data Analyst",
        "Backend Developer"
    ]

    return score, summary, jobs


# ---------- Routes ----------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        resume = request.files["resume"]

        if resume:
            filename = secure_filename(resume.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            resume.save(filepath)

            score, summary, jobs = analyze_resume(filename)

            return render_template(
                "result.html",
                name=name,
                email=email,
                score=score,
                summary=summary,
                jobs=jobs
            )

    return render_template("register.html")


@app.route("/download", methods=["POST"])
def download():
    name = request.form["name"]
    score = request.form["score"]

    file_path = "resume_summary.pdf"
    doc = SimpleDocTemplate(file_path)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"<b>Resume Evaluation Report</b>", styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph(f"Candidate Name: {name}", styles["Normal"]))
    elements.append(Paragraph(f"Resume Score: {score}%", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("Professional Summary:", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    points = [
        "Strong technical knowledge",
        "Excellent communication skills",
        "Suitable for entry-level positions",
        "Good problem-solving ability"
    ]

    elements.append(
        ListFlowable(
            [ListItem(Paragraph(point, styles["Normal"])) for point in points],
            bulletType='bullet'
        )
    )

    doc.build(elements)

    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
from pypdf import PdfReader
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

job_roles = {
        "Python Developer": [ "python", "flask", "django", "sql", "api" ],

    "Java Developer": [ "java", "spring boot", "hibernate", "sql", "oops"],

    "Frontend Developer": ["html", "css", "javascript", "react", "bootstrap"],

    "Backend Developer": [ "python", "flask", "api", "sql", "database" ],

    "Full Stack Developer": [ "html", "css", "javascript", "react", "node.js" ],

    "Software Engineer": [ "python", "java", "sql", "data structures", "algorithms"],

    "Data Analyst": [ "python", "excel", "sql", "power bi", "tableau" ],

    "Business Analyst": ["excel", "sql", "power bi", "analytics", "communication"],

    "Data Scientist": ["python", "statistics", "machine learning", "pandas", "numpy" ],

    "AI Engineer": [ "python", "machine learning", "tensorflow", "keras", "deep learning"],

    "Machine Learning Engineer": [ "python", "scikit-learn", "tensorflow", "data preprocessing", "machine learning"],

    "Cloud Engineer": ["aws", "azure", "docker", "linux", "kubernetes"],

    "DevOps Engineer": [ "docker", "kubernetes", "jenkins", "linux", "git"],

    "Cyber Security Analyst": [ "network security", "ethical hacking", "wireshark", "firewall", "linux" ],

    "Android Developer": [ "java", "android", "xml", "firebase", "kotlin" ],

    "Database Administrator": ["sql", "mysql", "oracle", "database", "backup"],

    "UI/UX Designer": [ "figma", "wireframing", "prototyping", "user research", "design thinking"],

    "QA Engineer": [ "testing", "selenium", "automation", "jira", "bug tracking"],

    "Network Engineer": [ "routing", "switching", "tcp/ip", "network security", "firewall" ],

    "IoT Engineer": ["arduino", "raspberry pi", "embedded systems", "sensors", "iot"],

    "Blockchain Developer": ["solidity", "ethereum", "smart contracts", "web3", "blockchain" ]

}


def extract_text(pdf_path):
    text = ""
    reader = PdfReader(pdf_path)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text.lower()

    return text


@app.route("/", methods=["GET", "POST"])
def home():

    score = None
    matched = []
    missing = []

    if request.method == "POST":

        role = request.form["role"]

        file = request.files["resume"]

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(filepath)

        resume_text = extract_text(filepath)

        required_skills = job_roles[role]

        for skill in required_skills:

            if skill.lower() in resume_text:
                matched.append(skill)
            else:
                missing.append(skill)

        score = int(
            (len(matched) / len(required_skills)) * 100
        )

    return render_template(
        "index.html",
        roles=job_roles.keys(),
        score=score,
        matched=matched,
        missing=missing
    )


if __name__ == "__main__":
    app.run(debug=True)
# ClearMyName.ai - Legal Identity Reclamation App
from flask import Flask, render_template, request, send_file
from docx import Document
import os

app = Flask(__name__)
app.template_folder = "templates"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form['name']
        dob = request.form['dob']
        ssn4 = request.form['ssn4']
        address = request.form['address']
        email = request.form['email']

        folder = f"letters/{name.replace(' ', '_')}"
        os.makedirs(folder, exist_ok=True)
        generate_letters(name, dob, ssn4, address, folder)

        return render_template("success.html", name=name)
    return render_template("index.html")

def generate_letters(name, dob, ssn4, address, folder):
    templates = {
        "Credit_Bureau_Dispute.docx": f"""To Whom It May Concern,

This is a formal dispute under the Fair Credit Reporting Act (15 U.S.C. §1681) and the Fair Debt Collection Practices Act (15 U.S.C. §1692). I am demanding a full investigation, verification, and correction of all records associated with:

Name: {name}
DOB: {dob}
SSN (last 4): XXX-XX-{ssn4}
Address: {address}

I am including a scanned ID as required. You must validate or delete unverifiable records. Failure to comply may result in further legal escalation.

Sincerely,
{name}
""",
        "IRS_IMF_Request.docx": f"""To: Internal Revenue Service FOIA Officer

Subject: FOIA Request – Individual Master File

Please process a Freedom of Information Act request for the complete Individual Master File associated with:

Name: {name}
SSN (last 4): XXX-XX-{ssn4}
DOB: {dob}
Address: {address}

ID copy included for verification.

Sincerely,
{name}
"""
    }
    for filename, content in templates.items():
        doc = Document()
        doc.add_paragraph(content.strip())
        doc.save(os.path.join(folder, filename))

if __name__ == "__main__":
    os.makedirs("letters", exist_ok=True)
    app.run(host="0.0.0.0", port=8080)

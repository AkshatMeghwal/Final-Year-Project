from flask import Flask, request, send_file, render_template, redirect, url_for, jsonify
import os
import shutil
import tempfile
from utils import Misc, extract_user_defined_functions_from_code  # Import the function
from docstring import process_js_files
from logger import logging
import re  # Import regex for cleaning HTML

app = Flask(__name__)
UPLOAD_FOLDER = "uploaded_files"
EXTRACTED_FOLDER = "extracted_uploaded_files"
GRAPH_FOLDER = "graph"
PROCESSED_FOLDER = "processed_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXTRACTED_FOLDER, exist_ok=True)
os.makedirs(GRAPH_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.chmod(PROCESSED_FOLDER, 0o777)  # Grant full permissions

# Store changes for review
changes_for_review = {}

@app.route("/", methods=["GET", "POST"])
def index():
    global changes_for_review
    changes_for_review = {}  # Reset changes for each new upload
    if request.method == "POST":
        # Clear old files
        Misc.clean_temp_folders(UPLOAD_FOLDER, EXTRACTED_FOLDER, GRAPH_FOLDER, PROCESSED_FOLDER)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(EXTRACTED_FOLDER, exist_ok=True)
        os.makedirs(GRAPH_FOLDER, exist_ok=True)
        os.makedirs(PROCESSED_FOLDER, exist_ok=True)

        if "zipfile" not in request.files:
            return render_template("index.html", error="No zip file uploaded")

        zipfile = request.files["zipfile"]
        zipfile_path = os.path.join(UPLOAD_FOLDER, zipfile.filename)
        zipfile.save(zipfile_path)

        try:
            # Extract the uploaded zip file
            extracted_folder_path = os.path.join(EXTRACTED_FOLDER, os.path.splitext(zipfile.filename)[0])
            logging.warning(f"Unpacking {zipfile_path} to {extracted_folder_path}")
            shutil.unpack_archive(zipfile_path, extracted_folder_path)

            # Process the extracted files and get changes for review
            raw_changes_for_review = process_js_files(extracted_folder_path, review_mode=True) or {}
            logging.debug(f"Raw changes for review: {raw_changes_for_review}")  # Debugging line

            # Transform the data structure for the frontend
            changes_for_review = {}
            for file_path, content in raw_changes_for_review.items():
                if isinstance(content, dict) and "modified" in content:
                    # Extract functions from the modified code
                    modified_code = content["modified"]
                    functions = content["functions"]  # Assuming functions are part of the content dict
                    # Clean up code and context fields
                    def clean_html(text):
                        return re.sub(r"<[^>]+>", "", text)  # Remove HTML tags

                    # Debugging: Log the extracted functions and their contexts
                    logging.debug(f"Extracted functions for {file_path}: {functions}")
                    
                    changes_for_review[file_path] = [
                        {
                            "name": func["name"],
                            "code": func["code"],
                            "context": func["context"],
                        }
                        for func in functions
                    ]
                else:
                    logging.error(f"Unexpected content structure for file {file_path}: {content}")
                    changes_for_review[file_path] = []  # Fallback to an empty list

            logging.debug(f"Transformed changes for review: {changes_for_review}")  # Debugging line

            # Pass changes as 'graphs' to the template
            return render_template("review.html", graphs=changes_for_review)

        except shutil.ReadError:
            logging.error(f"Failed to unpack {zipfile_path}. Unsupported archive format.")
            return render_template("index.html", error="Unsupported archive format. Please upload a valid zip file.")

    return render_template("index.html")


@app.route("/finalize", methods=["POST"])
def finalize():
    global changes_for_review
    user_decisions = request.json.get("decisions", {})
    logging.debug(f"User decisions received: {user_decisions}")  # Debugging log

    PROCESSED_FOLDER_STRUCTURE = "processed_files_structure"
    shutil.rmtree(PROCESSED_FOLDER_STRUCTURE, ignore_errors=True)  # Clear the folder if it exists
    os.makedirs(PROCESSED_FOLDER_STRUCTURE, exist_ok=True)

    # Loop over user decisions and modify files
    for file_path, decisions in user_decisions.items():
        # Get the original file's functions
        file_functions = changes_for_review.get(file_path, [])
        logging.debug(f"Processing file: {file_path}, Functions: {file_functions}")  # Debugging log

        processed_code = ""

        # Modify the file based on user decisions
        for func in file_functions:
            func_name = func["name"]
            if func_name in decisions and decisions[func_name]["action"] == "add":
                # Add docstring above the function
                updated_context = decisions[func_name].get("context", func["context"])
                # Sanitize the context to avoid duplicate /** **/
                sanitized_context = updated_context.strip().lstrip("/**").rstrip("*/").strip()
                docstring = f"/**\n * {sanitized_context}\n */\n" if sanitized_context else ""
                processed_code += docstring + func["code"] + "\n"
            else:
                # Keep the original function code
                processed_code += func["code"] + "\n"

        # Write the modified file to the new folder structure
        relative_path = os.path.relpath(file_path, start=EXTRACTED_FOLDER)
        output_path = os.path.join(PROCESSED_FOLDER_STRUCTURE, relative_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(processed_code)

    # Create a zip file for download
    output_zip = os.path.join(PROCESSED_FOLDER, "final_output.zip")
    shutil.make_archive(output_zip.replace(".zip", ""), "zip", PROCESSED_FOLDER_STRUCTURE)

    # Return the zip file for download
    return jsonify({"download_url": url_for("download", filename="final_output.zip")})


@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(PROCESSED_FOLDER, filename), as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)

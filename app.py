from flask import Flask, request, send_file, render_template, redirect, url_for
import os
import shutil
import tempfile
from utils import Misc
from docstring import process_js_files
from logger import logging

app = Flask(__name__)
UPLOAD_FOLDER = "uploaded_files"
PROCESSED_FOLDER = "processed_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.chmod(PROCESSED_FOLDER, 0o777)  # Grant full permissions

@app.route("/", methods=["GET", "POST"])
def index():
    download_ready = False
    download_filename = None

    if request.method == "POST":
        # Clear old files
        Misc.clean_temp_folders(UPLOAD_FOLDER, PROCESSED_FOLDER)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(PROCESSED_FOLDER, exist_ok=True)

        if "zipfile" not in request.files:
            return render_template("index.html", download_ready=False, error="No zip file uploaded")

        zipfile = request.files["zipfile"]
        zipfile_path = os.path.join(UPLOAD_FOLDER, zipfile.filename)
        os.makedirs(os.path.dirname(zipfile_path), exist_ok=True)  # Ensure the directory exists
        zipfile.save(zipfile_path)

        try:
            # Process the uploaded zip file
            processed_folder_path = os.path.join(PROCESSED_FOLDER, os.path.splitext(zipfile.filename)[0])
            logging.warning(f"Unpacking {zipfile_path} to {processed_folder_path}")
            shutil.unpack_archive(zipfile_path, processed_folder_path)
            process_js_files(processed_folder_path)

            # Create a zip file for download
            output_zip = os.path.join(PROCESSED_FOLDER, f"{os.path.basename(processed_folder_path)}.zip")
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_zip_base = os.path.join(temp_dir, os.path.basename(processed_folder_path))
                shutil.make_archive(temp_zip_base, "zip", processed_folder_path)
                temp_zip_path = f"{temp_zip_base}.zip"
                shutil.move(temp_zip_path, output_zip)

            download_ready = True
            download_filename = os.path.basename(output_zip)

        except shutil.ReadError:
            logging.error(f"Failed to unpack {zipfile_path}. Unsupported archive format.")
            return render_template("index.html", download_ready=False, error="Unsupported archive format. Please upload a valid zip file.")

    return render_template("index.html", download_ready=download_ready, download_filename=download_filename)

@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(PROCESSED_FOLDER, filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

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
    if request.method == "POST":
        # Clear old files
        Misc.clean_temp_folders(UPLOAD_FOLDER, PROCESSED_FOLDER)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(PROCESSED_FOLDER, exist_ok=True)

        if "folder" not in request.files:
            return "No folder uploaded", 400
        folder = request.files["folder"]
        folder_path = os.path.join(UPLOAD_FOLDER, folder.filename)
        os.makedirs(os.path.dirname(folder_path), exist_ok=True)  # Ensure the directory exists
        folder.save(folder_path)

        try:
            # Process the uploaded folder
            processed_folder_path = os.path.join(PROCESSED_FOLDER, os.path.splitext(folder.filename)[0])
            logging.warning(f"Unpacking {folder_path} to {processed_folder_path}")
            shutil.unpack_archive(folder_path, processed_folder_path)
            process_js_files(processed_folder_path)
        except shutil.ReadError:
            logging.error(f"Failed to unpack {folder_path}. Unsupported archive format.")
            return "Unsupported archive format. Please upload a valid archive file.", 400

        # Create a zip file for download
        output_zip = os.path.join(PROCESSED_FOLDER, f"{os.path.basename(processed_folder_path)}.zip")
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_zip_base = os.path.join(temp_dir, os.path.basename(processed_folder_path))
            shutil.make_archive(temp_zip_base, "zip", processed_folder_path)
            temp_zip_path = f"{temp_zip_base}.zip"
            shutil.move(temp_zip_path, output_zip)

        print(f"Processed folder path: {processed_folder_path}")
        print(f"Output zip path: {output_zip}")
        print(f"Permissions: {os.stat(PROCESSED_FOLDER)}")

        return redirect(url_for("download", filename=os.path.basename(output_zip)))

    return render_template("index.html")

@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(PROCESSED_FOLDER, filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)

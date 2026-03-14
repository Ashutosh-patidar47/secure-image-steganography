from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
import os

from steganography import encode_image, decode_image
from crypto_utils import encrypt_message, decrypt_message

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/encrypt", methods=["POST"])
def encrypt():

    try:

        image = request.files["image"]
        message = request.form["message"]
        password = request.form["password"]

        input_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(input_path)

        encrypted_message = encrypt_message(message, password)

        # Create new filename
        name, ext = os.path.splitext(image.filename)
        output_filename = f"{name}_encoded{ext}"

        output_path = os.path.join(UPLOAD_FOLDER, output_filename)

        encode_image(input_path, encrypted_message, output_path)

        return send_file(
            output_path,
            as_attachment=True,
            download_name=output_filename
        )

    except Exception:

        return "Encryption failed"


@app.route("/decrypt", methods=["POST"])
def decrypt():

    try:

        image = request.files["image"]
        password = request.form["password"]

        input_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(input_path)

        hidden_text = decode_image(input_path)

        message = decrypt_message(hidden_text, password)

        return jsonify({"message": message})

    except Exception:

        return jsonify({"message": "❌ Wrong password or invalid image"})


if __name__ == "__main__":
    app.run(debug=True)
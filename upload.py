import os
import requests
import dotenv
import base64
from requests_toolbelt.multipart.encoder import MultipartEncoder

def load_credentials():
    dotenv.load_dotenv('.env')
    username = os.getenv("USERNAME_WP")
    password = os.getenv("PASSWORD_WP")
    return username, password

def encode_credentials(username: str, password: str):
    credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
    return credentials

def upload_image(image_data: bytes, endpoint: str, headers: dict, image_name: str, image_slug: str):
    code_image_name = f"{image_slug}.{image_name.split('.')[1]}"
    alt_text = f"{image_name.split('.')[0]}".title()
    title = f"{image_name.split('.')[0]}".title()

    # Create a multipart encoder and add image data and alt text as fields
    multipart_data = MultipartEncoder(
        fields={
            "file": (code_image_name, image_data),  # Include image data
            "alt_text": alt_text.title(),  # Add alt text
            "title": title
        }
    )

    # Set the Content-Type header to the encoder's content type
    headers['Content-Type'] = multipart_data.content_type

    # Set the Content-Disposition header
    headers['Content-Disposition'] = f"attachment; filename={image_name}"

    # Send the request using the multipart encoder
    response = requests.post(endpoint, headers=headers, data=multipart_data)
    return response

def main(image_data: bytes, image_name: str, image_slug: str):
    # Load WordPress API credentials
    username, password = load_credentials()

    # Encode username and password as base64
    credentials = encode_credentials(username, password)

    # API endpoint for media upload
    endpoint = "https://graphicsprings.com/wp-json/wp/v2/media"

    # Set headers
    headers = {
        "Content-Type": "image/jpeg",  # Adjust content type based on your image type
        "Authorization": f"Basic {credentials}"  # Add Authorization header with base64 encoded credentials
    }

    # Send POST request to upload the image
    response = upload_image(image_data, endpoint, headers, image_name, image_slug)

    # Check if the upload was successful
    if response.status_code == 201:
        print(f"Image '{image_name}' uploaded successfully.")
        print("Media ID:", response.json().get("id"))
    else:
        print(f"Failed to upload image '{image_name}'. Status code:", response.status_code)
        print("Error message:", response.text)

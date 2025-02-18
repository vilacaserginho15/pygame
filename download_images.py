import os
import requests

def download_image(url, save_path):
    # Send HTTP GET request to the image URL
    response = requests.get(url)
    
    # Ensure the request was successful
    if response.status_code == 200:
        # Write the content as a binary file
        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"Image successfully downloaded to: {save_path}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

# Define your image URL
image_url = "https://opengameart.org/content/starfield-background"

# Ensure the directory exists
os.makedirs("image_assets", exist_ok=True)

# Path to save the image
save_location = "image_assets/starfield-background.jpg"

# Download the image
download_image(image_url, save_location)
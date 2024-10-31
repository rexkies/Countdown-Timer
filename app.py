from flask import Flask, send_file, request
from PIL import Image, ImageDraw, ImageFont
import datetime
import io
import time

app = Flask(__name__)


@app.route('/countdown')
def countdown():
    # Add a query parameter to bypass cache
    timestamp = request.args.get('timestamp', default=int(time.time()))

    # Set the target date and time
    target_date = datetime.datetime(2024, 12, 25, 0, 0, 0)

    # Calculate the time remaining
    now = datetime.datetime.now()
    time_left = target_date - now

    # Extract days, hours, minutes, seconds
    days = time_left.days
    hours, remainder = divmod(time_left.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Create an image with a black background and white text
    img = Image.new('RGB', (300, 100), color=(0, 0, 0))  # Black background
    d = ImageDraw.Draw(img)

    # Load a font
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        font = ImageFont.load_default()

    # Format countdown text
    countdown_text = f"{days}d {hours}h {minutes}m {seconds}s"

    # Get the size of the text
    text_bbox = d.textbbox((0, 0), countdown_text, font=font)  # Using textbbox
    text_width = text_bbox[2] - text_bbox[0]  # Calculate width
    text_height = text_bbox[3] - text_bbox[1]  # Calculate height

    # Draw the countdown text in white
    text_x = (img.width - text_width) // 2
    text_y = (img.height - text_height) // 2
    d.text((text_x, text_y), countdown_text, font=font, fill=(255, 255, 255))

    # Save the image to a BytesIO object
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
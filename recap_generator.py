import os
import django

# Django environment setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')
django.setup()

from recap.models import User
import numpy as np
import re
import requests
from datetime import datetime, timezone
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
from html import unescape



def get_user_data():
    # Get all users from the database
    users = User.objects.all()

    # Dictionary to store the film diary for each user
    diary_by_user = {}

    # User inserts month and year
    while True:
        month = int(input("\nEnter the month (1-12) of your desired recap: "))
        if 1 <= month <= 12:
            break

    year = int(input("From which year? "))

    # Directory to save profile pictures
    save_pfps_directory = os.path.join(os.getcwd(), 'images', 'pfps')

    # Directory to save fonts
    save_fonts_directory = os.path.join(os.getcwd(), 'recap', 'static', 'fonts')

    # Define the font file path
    font_path = os.path.join(save_fonts_directory, "TriviaSansMedium.ttf")

    # Load the font
    font = ImageFont.truetype(font_path, 32)
    font_large = ImageFont.truetype(font_path, 42)

    # Iterate over each user and extract lb_name
    for user in users:
        lb_name = user.lb_name

        # URL of the user's Letterboxd film diary
        url_diary = f"https://letterboxd.com/{lb_name}/films/diary/"

        # Request to get the page source code
        response_diary = requests.get(url_diary)
        html_diary = response_diary.text

        # Find all occurrences between "data-delete-viewing-url" and "data-viewing-date-str"
        all_occurrences = re.findall(r'data-delete-viewing-url="(.*?)data-viewing-date-str="(.*?)"', html_diary, re.DOTALL)

        # List to store films for the current user for the previous month
        user_films = []

        # For each occurrence found
        for occurrence in all_occurrences:
            # Make sure occurrence is a string
            occurrence_str = str(occurrence)

            # Using regular expression to find instances between quotes after "data-film-name" and "data-viewing-date"
            instances_between_quotes = re.findall(r'data-film-name="(.*?)"[^>]*data-viewing-date="(.*?)"', occurrence_str, re.DOTALL)

            # If found a match, check if it's from the specified month and year
            for instance in instances_between_quotes:
                film_name_html = instance[0]
                viewing_date = datetime.strptime(instance[1], "%Y-%m-%d").replace(tzinfo=timezone.utc)

                # Use BeautifulSoup to decode HTML entities
                soup = BeautifulSoup(film_name_html, 'html.parser')
                film_name = unescape(soup.get_text())

                # Check if the film is from the specified month and year
                if viewing_date.year == year and viewing_date.month == month:
                    user_films.append({"Film Name": film_name, "Viewing Date": viewing_date.strftime("%d/%m/%Y")})

        # Add the user's film list to the dictionary
        diary_by_user[lb_name] = user_films

        # URL of the user's page to extract the profile picture
        url_profile = f"https://letterboxd.com/{lb_name}/"

        # Request to get the page source code
        response_profile = requests.get(url_profile)
        html_profile = response_profile.text

        # Find the first occurrence of "property="og:image" content="
        occurrence_image = re.search(r'property="og:image" content="(.*?)"', html_profile)

        # If found the match
        if occurrence_image:
            image_url = occurrence_image.group(1)

            # Request the image
            response_image = requests.get(image_url)

            # Convert image to a circular format with PNG background
            img = Image.open(BytesIO(response_image.content)).convert("RGB")
            npImage = np.array(img)
            h, w = img.size

            # Create same size alpha layer with circle
            alpha = Image.new('L', img.size, 0)
            draw = ImageDraw.Draw(alpha)
            draw.pieslice(((0, 0), (h, w)), 0, 360, fill=255)

            # Convert alpha Image to numpy array
            npAlpha = np.array(alpha)

            # Add alpha layer to RGB
            npImage = np.dstack((npImage, npAlpha))

            # Save the circular image locally
            image_path = os.path.join(save_pfps_directory, f"{lb_name}_profile_pic.png")
            Image.fromarray(npImage).save(image_path)
    
    return diary_by_user, users, month, year, font, font_large, save_pfps_directory





# Define a function to generate recap images
def generate_recap_images(user_films, lb_name, month, year, font, font_large, save_pfps_directory):

    # Directory to save the recaps
    save_recaps_directory = os.path.join(os.getcwd(), 'images', 'user_recaps')

    # Create feed and story recap images
    for format_type in ["feed", "story"]:
        # Define image dimensions
        width, height = (1014, 1014) if format_type == "feed" else (720, 1280)

        # Create a blank image with a grey background
        img = Image.new("RGB", (width, height), "#13171c")
        draw = ImageDraw.Draw(img)
        width, height = img.size

        # Load the profile picture
        profile_pic_path = os.path.join(save_pfps_directory, f"{lb_name}_profile_pic.png")
        profile_pic = Image.open(profile_pic_path).convert("RGBA")

        # Resize profile picture to fit
        profile_pic = profile_pic.resize((150, 150), Image.Resampling.LANCZOS)

        # Paste the profile picture at the top
        img.paste(profile_pic, (width // 2 - 75, 40), profile_pic)

        # Add user's name
        recap_text = f"{lb_name}"
        text_width, text_height = draw.textbbox((0, 0), recap_text, font=font)[2:]
        draw.text(((width - text_width) // 2, 220), recap_text, font=font, fill="white")

        # Add month film recap text
        month_name = datetime(2023, month, 1).strftime("%B")
        recap_text = f"Your {month_name} {year} Film Recap:"
        text_width, text_height = draw.textbbox((0, 0), recap_text, font=font_large)[2:]
        draw.text(((width - text_width) // 2, 290), recap_text, font=font_large, fill="white")

        # Add film details
        film_details = [f"{datetime.strptime(film['Viewing Date'], '%d/%m/%Y').strftime('%m/%d')} - {film['Film Name']}" for film in user_films]
        film_details_text = "\n".join(film_details)
        text_width, text_height = draw.textbbox((0, 0), film_details_text, font=font)[2:]
        draw.text(((width - text_width) // 2, 390), film_details_text, font=font, fill="white")

        recap_text = "Letterboxd Month Recap"
        text_width, text_height = draw.textbbox((0, 0), recap_text, font=font)[2:]
        draw.text(((width - text_width) // 2 + 20, height - text_height - 30), recap_text, font=font, fill="white")

        # Load the logo image
        logo_path = os.path.join("recap", "static", "logo", "lbmr_logo.png")

        # Open the logo with transparency
        logo = Image.open(logo_path).convert("RGBA")

        # Resize the logo to fit the desired height
        logo_height = int(text_height * 1.2)
        logo_width = int((logo_height / logo.size[1]) * logo.size[0])
        logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)

        # Define the position for the logo
        logo_position = ((width - text_width) // 2 - logo_width // 2 - 2, height - text_height - 35)

        # Paste the logo onto the main image
        img.paste(logo, logo_position, logo)

        # Save the recap image
        image_path = os.path.join(save_recaps_directory, f"{lb_name}_{month_name.lower()}_{year}_{format_type}_recap.jpg")
        img.save(image_path)





def delete_directory_contents(directory):
    try:
        # List all files in the directory
        files = os.listdir(directory)

        # Iterate over the files and delete them
        for file in files:
            file_path = os.path.join(directory, file)
            os.remove(file_path)

    except Exception as e:
        print(f"An error occurred while deleting contents of directory {directory}: {str(e)}")



def recaps():
    diary_by_user, users, month, year, font, font_large, save_pfps_directory = get_user_data()
    for user in users:
        generate_recap_images(diary_by_user[user.lb_name], user.lb_name, month, year, font, font_large, save_pfps_directory)
    delete_directory_contents(save_pfps_directory)
    print("\nYour recap is at the images/user_recaps folder.\n")

recaps()
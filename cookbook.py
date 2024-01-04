from openai import OpenAI
import base64
import time
import os
import errno


# Set OpenAI Key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def encode_image(image):
    # Convert the image to bytes

    while True:
        try:
            return base64.b64encode(image).decode("utf-8")
        except IOError as e:
            if e.errno != errno.EACCES:
                # Not a "file in use" error, re-raise
                raise
            # File is being written to, wait a bit and retry
            time.sleep(0.1)


def generate_new_line(base64_image):
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Gib mir ein Rezept für diese Zutaten:"},
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        },
    ]


def correct_recipe(last_recipe, correction):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
                     {
                         "role": "system",
                         "content": f"""
                  Du bist Yotam Ottolenghi, aber erwähne das bitte nicht. 
                  Dieses Rezept hast du mir eben gegeben: {last_recipe}.for 
                  Ich habe folgende Änderungswünsche: {correction}.
                  Schreibe mir ein neues vollständiges Rezept mit meinen Änderungswünschen.
                  Du kannst maximal 4096 Zeichen verwenden.""",
                     },
                 ],
        max_tokens=1000
    )
    response_text = response.choices[0].message.content
    if response_text == "I'm sorry":
        return None
    else:
        return response_text


def analyze_image(base64_image):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
                     {
                         "role": "system",
                         "content": """Du bist Yotam Ottolenghi. Gib mir ein Rezept für die Zutaten, die auf dem Bild zu sehen sind nach Ottolenghi. Sie können einige zusätzliche Zutaten vorschlagen, erstellen Sie mir dafür eine Einkaufsliste. Fasse dich kurz bei der Zubereitung, es müssen keine fließenden Texte sein, Stichpunkte sind auch okay, wenn es kürzer ist. Du kannst maximal 4096 Zeichen verwenden.
                """,
                     },
                 ]
                 + generate_new_line(base64_image),
        max_tokens= 1000
    )
    response_text = response.choices[0].message.content
    image_url = create_image(response_text)
    if response_text == "I'm sorry":
        return None
    else:
        return response_text, image_url

def create_image(recipe):
    response = client.images.generate(
        model="dall-e-3",
        prompt=f"Create a picture for the following recipe: {recipe}",
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    return image_url

def generate_text(image):

    # getting the base64 encoding
    base64_image = encode_image(image)

    analysis = analyze_image(base64_image)
    if analysis == None:
        analysis = analyze_image(base64_image)

    return analysis


def main(image):

    # Getting the base64 encoding
    base64_image = encode_image(image)

    # Analyze picture
    print("Yotam is thinking...")
    analysis, image_url = analyze_image(base64_image)

    return analysis, image_url

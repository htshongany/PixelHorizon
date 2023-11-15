import requests
from utils import img_output_name


def remove_background(image_path,api_key, image_output_name=None):
    try:
        image_output_name = img_output_name(image_path, 'png', image_output_name)
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': open(image_path, 'rb')},
            data={'size': 'auto'},
            headers={'X-Api-Key': api_key},
        )
        if response.status_code == requests.codes.ok:
            with open(image_output_name, 'wb') as out:
                out.write(response.content)
                return response.status_code
        else:
            print("Error:", response.status_code, response.text)
    except Exception as e:
        print(f"An error occurred in remove_background: {e}")
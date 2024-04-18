import sys
import requests
from bs4 import BeautifulSoup, Tag
import re
from urllib.parse import urljoin
from pprint import pp
import json


def extract_phone_models_from_widgets_container(
    phonecard_widgets_container, brand_name, re_rumored_str, re_device_id, re_photo_url
):

    # List of dictionaries to store phone details
    res = []

    re_model_name = re.compile(rf"{brand_name} (.*)")

    for w in phonecard_widgets_container.children:
        # Skip non-Tag elements (e.g. NavigableString, Comment, etc.)
        if not isinstance(w, Tag):
            continue

        # Only consider containers (div) with the class "widget-tilePhoneCard"
        if "widget-tilePhoneCard" in w["class"]:
            assert w.a is not None
            section_caption = w.a.section

            # Only consider phone models that are released (not rumored).
            # If the phone model is rumored, the section container will contain the word "rumored"
            # in one of its descendant elements, which we find using BeautifulSoup's find method with a string argument.
            assert section_caption is not None
            if section_caption.find(string=re_rumored_str) is None:
                phone_details = {}

                assert section_caption.p is not None
                model_name = section_caption.p.string

                # The webpage incorrectly lists some smartwatches and tablets as phones.
                # We skip these by checking if the model name contains the word "Watch", "Tab", or "Pad".
                if re.search(r"Watch|Tab|Pad", model_name, re.IGNORECASE) is not None:
                    continue

                # Capture the model name using regex
                model_name_match = re_model_name.match(model_name)
                phone_details["model_name"] = model_name_match.group(1)

                # Capture the photo URL using regex
                pic_square = w.a.picture
                photo_url_match = re_photo_url.match(pic_square.img["src"])
                photo_url = photo_url_match.group(0)
                # Replace the photo URL with a higher resolution image
                phone_details["photo_url"] = photo_url.replace("350", "800")

                # Capture the device ID using regex
                device_id_match = re_device_id.search(w.a["href"])
                phone_details["device_id"] = device_id_match.group(1)

                phone_details["brand_name"] = brand_name

                res.append(phone_details)

    return res


def extract_widgets_container(url, query_params=None):
    # Extract the (div) container containing the phone model widgets
    # from the parsed HTML content of the webpage
    page = requests.get(url, query_params)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup.find("div", class_="stream block")


def validate_brand_name(brand_name):
    # List of supported brands
    supported_brands = [
        "Apple",
        "Samsung",
        "Huawei",
        "Nokia",
        "Sony",
        "LG",
        "Motorola",
        "Xiaomi",
        "OnePlus",
        "Google",
        "Oppo",
        "Realme",
        "Vivo",
    ]

    # Assert that the brand name is in the list of supported brands
    assert (
        brand_name in supported_brands
    ), f"Brand name '{brand_name}' is not supported."


def json_dump(phones_list, to_file="phones.json"):
    with open(to_file, "w") as f:
        json.dump(phones_list, f, indent=4)


if __name__ == "__main__":
    BASE_URL = "https://www.phonearena.com/phones/manufacturers/"
    QUERY_PARAMS = {
        "f[53][]": 1223,
    }

    brand_name = sys.argv[1]
    validate_brand_name(brand_name)

    num_pages = int(sys.argv[2])

    # Compile regex patterns for efficiency, since we will use them multiple times
    re_rumored_str = re.compile(r"rumored", re.IGNORECASE)
    re_device_id = re.compile(r"id(\d+)")
    re_photo_url = re.compile(r"(.+\.jpg)")

    # List to store phone details
    phones_list = []

    for i in range(1, num_pages + 1):
        url = f"{brand_name.lower()}/page/{i}"
        url = BASE_URL + url
        phonecard_widgets = extract_widgets_container(url, query_params=QUERY_PARAMS)

        res = extract_phone_models_from_widgets_container(
            phonecard_widgets,
            brand_name,
            re_rumored_str,
            re_device_id,
            re_photo_url,
        )

        phones_list.extend(res)

    # Serialize the list of phone details as a JSON formatted stream.
    # The output (string) is meant to be printed to the console and redirected to a file.
    print(json.dumps(phones_list, indent=4))

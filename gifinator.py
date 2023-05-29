import requests
from PIL import Image, ImageOps
import io
import argparse
import re


def fetch_image(url, first, verbose):
    """
    Fetches an image from the given URL. Returns the image data and the URL for the next image.
    If the request fails, returns None and the same URL.
    """    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException as err:
        if first and verbose:
            print(f"[</3] Request failed due to {err}.")
        elif verbose:
            print(f"[<3] Reached the end of the sequence~")
        return None, url

    return response.content, increment_url(url)


def increment_url(url):
    """
    Increments the frame number in the given URL. The URL should end in "_<frame number>.jpg" or "/<frame number>.jpg".
    Returns the new URL.
    """
    match = re.search(r'(\d+)(\.jpg)$', url)
    if match:
        current_frame = match.group(1)
        next_frame = str(int(current_frame) + 1).zfill(len(current_frame))
        next_url = url.replace(f"{current_frame}.jpg", f"{next_frame}.jpg")
        return next_url

    return url  # Return the original URL if no match was found


def apply_filter(image, filter_name, verbose):
    """
    Applies the specified filter to the image and returns the filtered image.
    """
    if filter_name == "grayscale":
        return ImageOps.grayscale(image)
    elif filter_name == "sepia":
        # Sepia is created by first converting to grayscale, then colorizing
        image = ImageOps.grayscale(image)
        image = ImageOps.colorize(image, "#704214", "#C0A080")  # Color values for sepia
        return image
    else:
        return image



def create_gif(output_file, url, speed, reverse, filter_name, verbose):
    """
    Fetches images from the given URL, applies the specified filter, and creates a GIF.
    """
    if verbose: print(f"[*] Initiating GIF creation from URL: {url}")

    images = []
    first = True
    while True:
        image_data, url = fetch_image(url, first, verbose)
        first = False
        if image_data is None:
            break

        try:
            image = Image.open(io.BytesIO(image_data))
            image = apply_filter(image, filter_name, verbose)
            images.append(image)
        except IOError as e:
            if verbose: print(f"[</3] Failed to open image. Error: {e}")
            break

    if images:
        if verbose: print(f"[*] Assembling images into GIF...")
        if reverse:
            images = images[::-1]
        images[0].save(output_file, 'gif', save_all=True, append_images=images[1:], loop=0, duration=speed)
        if verbose: print(f"[<3] GIF saved as {output_file}. Enjoy your GIF!")
    else:
        if verbose: print("[</3] No images could be loaded, GIF creation aborted.")



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="The base URL of the product images.")
    parser.add_argument("output", help="The output filename of the GIF.")
    parser.add_argument("-s", "--speed", type=int, default=100, help="Speed of the GIF. Lower is faster.")
    parser.add_argument("-r", "--reverse", action="store_true", help="Reverses the GIF.")
    parser.add_argument("-f", "--filter", type=str, choices=["grayscale", "sepia"], help="Applies a color filter to the GIF.")
    parser.add_argument("-v", "--verbose", action="store_false", help="Verbose output (default: True).")
    args = parser.parse_args()

    print(f"[*] GIFinator initializing")
    print(f"[*] Starting to fetch frames~")
    create_gif(args.output, args.url, args.speed, args.reverse, args.filter, args.verbose)


if __name__ == "__main__":
    main()

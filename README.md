# GIFinator 🎥

Welcome to the world of GIFinator! This nifty Python script transforms a sequence of 360-degree product images into an awesome GIF. But that's not all, it also lets you:
* Control the GIF speed 🚀
* Reverse the animation 🔁
* Apply groovy color filters (grayscale or sepia) 🌈

![Foxy Plush 360 GIF](./foxy.gif)

## Usage
```shell
usage: gifinator.py [-h] [-s SPEED] [-r] [-f {grayscale,sepia}] [-v] url output

positional arguments:
  url                   The base URL of the product images.
  output                The output filename of the GIF.

options:
  -h, --help            show this help message and exit
  -s SPEED, --speed SPEED
                        Speed of the GIF. Lower is faster.
  -r, --reverse         Reverses the GIF.
  -f {grayscale,sepia}, --filter {grayscale,sepia}
                        Applies a color filter to the GIF.
  -v, --verbose         Verbose output (default: True).
```
## Contribution
Found a bug? Have a cool feature in mind? Feel free to make a pull request or open an issue 🚀🌈

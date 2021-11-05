from PIL import Image, ImageFilter, ImageDraw, ImageEnhance, ImageOps
import numpy as np
from scipy import ndimage

def get_mask(src_img):
    img = np.array(src_img)
    # laplace
    A = np.full((9, 9), -1)
    A[4, 4] = 80


    # get edges
    out = ndimage.convolve(img, A)

    # Convert back to PIL image
    out = Image.fromarray(np.uint8(out))
    mask = out.convert("RGB")
    seed = (0, 0)
    rep_value = (255, 0, 0)
    ImageDraw.floodfill(mask, seed, rep_value, thresh=0)
    n_mask = np.array(mask)
    reds = (n_mask[:, :, 0] == 255) & (n_mask[:, :, 1] == 0) & (n_mask[:, :, 2] == 0)
    return Image.fromarray((reds*255).astype(np.uint8))

def change_color(src_img, rgb_in, rgb_out):
    data = np.array(src_img.convert("RGB"))

    r1, g1, b1 = rgb_in  # Original value
    r2, g2, b2 = rgb_out  # Value that we want to replace it with

    red, green, blue = data[:, :, 0], data[:, :, 1], data[:, :, 2]
    mask = (red == r1) & (green == g1) & (blue == b1)
    data[:, :, :3][mask] = [r2, g2, b2]

    return Image.fromarray(data)

def white_to_transparent(src_img):
    x = np.asarray(src_img.convert('RGBA')).copy()

    x[:, :, 3] = (255 * (x[:, :, :3] != 255).any(axis=2)).astype(np.uint8)

    return Image.fromarray(x)

def get_fingerprint_photo(fingerprint, skin, background):
    pic = Image.open(fingerprint)
    skin = Image.open(skin)
    skin = skin.resize(pic.size)
    bg = Image.open(background)
    bg = bg.resize(pic.size)
    skin_darker = skin.copy()
    factor = 0.95  # used between papillary lines
    ultra_dark_factor = 0.5  # used on edged
    skin_darker = ImageEnhance.Brightness(skin_darker).enhance(factor)
    skin_ultra_darker = ImageEnhance.Brightness(skin_darker).enhance(ultra_dark_factor)
    white_bg = Image.new("RGB", pic.size, color="white")
    papillar = white_bg.copy()
    darker_edges = white_bg.copy()

    mask = get_mask(pic)
    blur_factor = 50
    blurred_mask = mask.filter(ImageFilter.GaussianBlur(blur_factor))

    invert_blurred_mask = ImageOps.invert(blurred_mask)
    inverted_mask = ImageOps.invert(mask)
    darker_edges.paste(invert_blurred_mask, (0, 0), inverted_mask)

    orig_pic = white_to_transparent(pic)  # basically a mask from fingerprint

    papillar.paste(skin, (0, 0), orig_pic.convert('RGBA'))  # maps skin to papillary lines
    skin_darker.paste(pic, (0, 0), mask)  # cuts finger shape into skin

    # combines papillary lines and finger "background"
    orig_img = Image.blend(papillar.convert('RGBA'), skin_darker.convert('RGBA'), alpha=0.8)

    # makes edges darker
    final = Image.composite(orig_img, skin_ultra_darker, darker_edges.convert('L'))
    bg.paste(final, (0, 0), inverted_mask)
    return bg


if __name__ == '__main__':
    final = get_fingerprint_photo("SG_1_1_sq.png", "skin_texture_2.png", "bg2.png")
    final.show()

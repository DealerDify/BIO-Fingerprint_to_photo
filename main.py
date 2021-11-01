
from PIL import Image, ImageFilter, ImageDraw
import numpy as np
from scipy import ndimage
import scipy.misc

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

def change_color(src_img):
    data = np.array(src_img.convert("RGB"))

    r1, g1, b1 = 0, 0, 0  # Original value
    r2, g2, b2 = 198, 140, 83  # Value that we want to replace it with

    red, green, blue = data[:, :, 0], data[:, :, 1], data[:, :, 2]
    mask = (red == r1) & (green == g1) & (blue == b1)
    data[:, :, :3][mask] = [r2, g2, b2]

    return Image.fromarray(data)

def white_to_transparent(src_img):
    x = np.asarray(src_img.convert('RGBA')).copy()

    x[:, :, 3] = (255 * (x[:, :, :3] != 255).any(axis=2)).astype(np.uint8)

    return Image.fromarray(x)

if __name__ == '__main__':
    pic = Image.open("C:\\Users\\Lukyn\\Desktop\\VUT_FIT\\bio\\Synth\\Synth\\sfinge\\SG_1_1.png")
    #pic = pic.convert("L")

    pic.show()


    mask = get_mask(pic)
    #mask.show()
    finger = change_color(mask)
    pic = white_to_transparent(pic)
    Image.blend(pic.convert('RGBA'), finger.convert('RGBA'), alpha=0.9).show()

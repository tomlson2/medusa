import cv2 as cv

def blur_image(img):
    im1 = cv.imread(img)
    im = cv.blur(im1, (2,2))
    cv.imwrite("fonts\\result.png",im)

def resize(img):
    im = cv.imread(img)
    scale = 50
    width = int(im.shape[1] * scale / 100)
    height = int(im.shape[0] * scale / 100)
    dim = (width, height)

    resized = cv.resize(im, dim, interpolation = cv.INTER_AREA)

    cv.imwrite("fonts\\resizedbold12img.png",resized)

blur_image("fonts\\resizedbold12img.png")
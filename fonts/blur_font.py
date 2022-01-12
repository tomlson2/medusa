import cv2 as cv

def blur_image():
    im1 = cv.imread("fonts\RuneScape-Quill-8.png")
    im = cv.blur(im1, (5,5))
    cv.imwrite("fonts\\result.png",im)

def resize():
    im = cv.imread("fonts\\result.png")
    scale = 60
    width = int(im.shape[1] * scale / 100)
    height = int(im.shape[0] * scale / 100)
    dim = (width, height)

    resized = cv.resize(im, dim, interpolation = cv.INTER_AREA)

    cv.imwrite("fonts\\resized-8-quill.png",resized)

img = cv.imread('fonts\\a2.png') # load a dummy image
while(1):
    cv.imshow('img',img)
    k = cv.waitKey(33)
    if k==27:    # Esc key to stop
        break
    elif k==-1:  # normally -1 returned,so don't print it
        continue
    else:
        print(k) # else print its value
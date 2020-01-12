import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import os

def change(colour):
    # Create original file
    for file in os.listdir("./wikipedia"):
        if file != 'original':
            im = plt.imread(os.path.join(".\\wikipedia", file))
            ims = Image.fromarray((im[-1] * 255).astype(np.uint8))
            ims.save(os.path.join("./wikipedia/original", file))

    # Make new fines
    for file in os.listdir("./wikipedia"):
        if file[0] == 'w':
            im = plt.imread(os.path.join(".\\wikipedia", file))
            im = (im * 255).astype(np.uint8)
            ims = Image.fromarray(im)
            ims.save(os.path.join("./wikipedia", file))
        elif file[0] == 'b':
            im = plt.imread(os.path.join(".\\wikipedia", file))
            im = (im * 255).astype(np.uint8)
            img[img[:, :, 2] < 100, 2] = 255
            ims = Image.fromarray(im)
            ims.save(os.path.join("./wikipedia", file))

change(1)
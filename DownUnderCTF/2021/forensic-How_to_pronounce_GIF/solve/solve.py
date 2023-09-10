from PIL import Image
from base64 import *

for k in range(10):
    image_res = Image.new("RGB", (300, 22*12), "white")

    y = 0 
    for i in range(12): 
        if i < 10:
            image = Image.open("./frame_0" + str(i) + str(k) + "_delay-0.05s.png")
        else:
            image = Image.open("./frame_" + str(i) + str(k) + "_delay-0.05s.png")
        
        image_res.paste(image, (0, y))
        y += 21

    image_res.save("./res" + str(k) + ".png")
    image_res.show()

flag = b64decode(b'RFVDVEZ7YU1fMV9oYVhYMHJfbjB3P30=')
print(flag)

# DUCTF{aM_1_haXX0r_n0w?}
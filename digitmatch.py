import matplotlib.pyplot as plt
import matplotlib.image as pli
from sys import argv
import Image
import ImageFilter

from sklearn import datasets, svm

lim = int(argv[1])
testImages = []
for filename in argv[2:]:
    img = Image.open(filename)
    pix = img.load()
    minX = img.size[0]
    minY = img.size[1]
    maxX = None
    maxY = None
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if (pix[x,y][0] + lim >= pix[x,y][2]) or (pix[x,y][1] + lim >= pix[x,y][2]):
                pix[x,y] = (255, 255, 255)
            else:
                pix[x,y] = (0, 0, 0)
                minX = min(minX, x)
                minY = min(minY, y)
                maxX = max(maxX, x)
                maxY = max(maxY, y)
    img.save('bw_' + filename)
    height = maxY-minY+1
    width = maxX-minX+1
    sz = max(height, width)
    cropImg = img.crop((minX, minY, maxX, maxY))
    newImg = Image.new('1', (sz, sz), "white")
    newImg.paste(cropImg, ((sz-width)/2, (sz-height)/2))
    finImg = newImg.resize((16,16)).convert('L').filter(
            ImageFilter.Kernel((3,3),
            [0.0625, 0.125, 0.0625, 0.125, 0.25, 0.125, 0.0625, 0.125, 0.0625]))
    finPix = finImg.load()
    testImage = []
    for x in range(8):
        for y in range(8):
            finPix[x,y] = (finPix[2*x, 2*y] + finPix[2*x+1, 2*y] +
                           finPix[2*x, 2*y+1] + finPix[2*x+1, 2*y+1])/4
    for x in range(8):
        for y in range(8):
            testImage.append((256-finPix[y,x])/16)
    testImages.append(testImage)

for index, img in enumerate(testImages):
    ti = [img[:8], img[8:16], img[16:24], img[24:32],
          img[32:40], img[40:48], img[48:56], img[56:64]]
    plt.subplot(6, 5, index + 1)
    plt.axis('off')
    plt.imshow(ti, cmap=plt.cm.gray_r, interpolation='nearest')

digits = datasets.load_digits()
n_samples = len(digits.images)

for index, im in enumerate(digits.images[:20]):
    plt.subplot(6, 5, index + 11)
    plt.axis('off')
    plt.imshow(im, cmap=plt.cm.gray_r, interpolation='nearest')

data = digits.images.reshape((n_samples, -1))
classifier = svm.SVC(gamma=0.001)
classifier.fit(data, digits.target)
print classifier.predict(testImages)

plt.show()

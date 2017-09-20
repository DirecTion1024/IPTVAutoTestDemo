from PIL import Image
from PIL import ImageChops
from PIL import ImageDraw
import os


def analysisTxt(path):
    file_object = open(path, 'r')
    try:
        all_text = file_object.readlines()
    finally:
        file_object.close()
    flag = 0
    dic = {}
    resolution = ''
    x = ''
    y = ''
    width = ''
    height = ''
    i = 0
    while i < len(all_text):
        if 'resolution' in all_text[i]:
            list = all_text[i].strip().split(':')
            resolution = list[-1]
            flag = 1
        elif 'height' in all_text[i] and flag == 1:
            list = all_text[i].strip().split(',')
            for eve in list:
                if 'x' in eve:
                    x = eve.strip().split(':')[-1]
                    continue
                if 'y' in eve:
                    y = eve.strip().split(':')[-1]
                    continue
                if 'height' in eve:
                    height = eve.strip().split(':')[-1]
                    continue
                if 'width' in eve:
                    width = eve.strip().split(':')[-1]
                    continue
            flag = 0
            dic[resolution] = (
                float(x), float(y), float(x) + float(width), float(y) + float(height))
        else:
            pass
        i = i + 1
    return dic


def pictureCom(path1, path2, repath):
    im1 = Image.open(path1)
    im2 = Image.open(path2)

    image_width, image_height = im1.size
    print image_width, image_height

    txtpath = repath[0:repath.rfind('/', 1) + 1] + '/' + 'keyboardRegion.txt'
    dic = analysisTxt(txtpath)
    resolution = str(image_width) + 'x' + str(image_height)
    box = dic.get(resolution)
    img1 = im1.crop(box)
    img2 = im2.crop(box)

    diff = ImageChops.difference(img2, img1)
    print dir(diff)
    print diff.getbbox()
#     diff.save('x.png')

    if diff.getbbox() == None:
        return True
    else:
        print (len(diff.getdata()))
        list_num = [i for i, data in enumerate(
            diff.getdata()) if data != (0, 0, 0, 0)]
        print len(list_num)
        print list_num[-100:]
        dr = ImageDraw.Draw(img1)

        imgwidth, imgheight = img1.size
        print imgwidth
        print imgheight
        precision_x, precision_y = imgwidth / 10, imgheight / 10
        list_range = []
        for pos in list_num:
            x, y = pos % imgwidth, pos / imgwidth
            range_x, range_y = x / precision_x, y / precision_y
            if((range_x, range_y) not in list_range):
                list_range.append((range_x, range_y))

        print len(list_range)
        # dr.rectangle(((0,0),(10,1000)),outline='red')
        for range_x, range_y in list_range:
            pass

        for range_x, range_y in list_range:
            x = range_x * precision_x
            y = range_y * precision_y
            dr.rectangle(
                ((x, y), (x + precision_x, y + precision_y)), outline='red')
            dr.rectangle(
                ((x + 1, y + 1), (x + precision_x - 1, y + precision_y - 1)), outline='red')

        im_new = Image.new("RGB", (imgwidth * 2 + 1, imgheight))
        im_new.paste(img1, (0, 0, imgwidth, imgheight))
        im_new.paste(
            img2, (imgwidth + 1, 0, imgwidth * 2 + 1, imgheight))
        picname = os.path.basename(path1)
        im_new.save(repath + '/' + picname)
        return False

if __name__ == "__main__":
    import profile
    pass
    # profile.run('test')
#     analysisTxt(
#         'E:/UICheckTool/checkResult/2017-06-02-14-37-33_iFlyIME_v7.1.5045.ossptest/keyboardRegion.txt')
#     pictureCom('E:/git/testgit/ImeTest/iFly/a.png',
#                'E:/git/testgit/ImeTest/iFly/b.png', 'E:/git/testgit/ImeTest/iFly')

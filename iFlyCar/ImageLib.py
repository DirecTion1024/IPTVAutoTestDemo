#-*- coding: UTF-8 -*- 
from PIL import Image
from PIL import ImageOps
from PIL import ImageFilter
from copy import deepcopy
import math
import os
import shutil
from robot.libraries import BuiltIn
from robot.api import logger

BUILTIN = BuiltIn.BuiltIn()

class ImageLib(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '0.1.0'
    
    def __init__(self):
        pass
    
    def element_ui_should_be(self, locator, imagepath=None, maxdiff=5, offset=0):
        if not imagepath:
            imagepath = self._get_local_image_path()
        ui = self.capture_page_screenshot()
        if not os.path.exists(imagepath):
            logger.info("Image at %s not found, Using current as expect!" % imagepath)
            shutil.copyfile(ui, imagepath)
        else:
            rect = self.get_element_rect(locator)
            offset = int(offset)
            rect = (rect[0]+offset, rect[1]+offset, rect[2]-offset, rect[3]-offset)
            similarity = self.compare_image(imagepath, ui, rect)
            logger.info('Got Image Similarity: %d at %s' % (similarity, locator))
            if similarity > maxdiff:
                raise AssertionError("UI not match at %s %s" % (locator, str(rect)))
    
    def element_ui_should_not_be(self, locator, imagepath, maxdiff=5):
        if self.is_same_ui(locator, imagepath, maxdiff):
            raise AssertionError("UI should not match at %s" % locator)
    
    def is_same_ui(self, locator, imagepath, maxdiff=5):
        if not os.path.exists(imagepath):
            raise RuntimeError("Path not found! %s" % imagepath)
        ui = self.capture_page_screenshot()
        rect = self.get_element_rect(locator)
        similarity = self.compare_image(imagepath, ui, rect)
        logger.info('Got Image Similarity: %d at %s' % (similarity, locator))
        if similarity > maxdiff:
            return False
        return True
    
    def compare_image(self, path1, path2, box=()):
        """
        box: a tuple or string with left, upper, right, lower
        """
        image1 = Image.open(path1)
        image2 = Image.open(path2)
        if box:
            if isinstance(box, basestring):
                box = tuple(map(int, box.split(',')))
            else:
                box = tuple(box)
            image1 = image1.crop(box)
            image2 = image2.crop(box)
        return self.get_similarity(image1, image2)
    
    def get_similarity(self,image1,image2,size=(32,32),part_size=(8,8)):
        """
        """
        assert size[0]==size[1],"size error"
        assert part_size[0]==part_size[1],"part_size error"
    
        image1 = image1.resize(size).convert('L').filter(ImageFilter.BLUR)
        image1 = ImageOps.equalize(image1)
        matrix = self._get_matrix(image1)
        DCT_matrix = self._DCT(matrix)
        List = self._sub_matrix_to_list(DCT_matrix, part_size)
        middle = self._get_middle(List)
        code1 = self._get_code(List, middle)
    
        image2 = image2.resize(size).convert('L').filter(ImageFilter.BLUR)
        image2 = ImageOps.equalize(image2)
        matrix = self._get_matrix(image2)
        DCT_matrix = self._DCT(matrix)
        List = self._sub_matrix_to_list(DCT_matrix, part_size)
        middle = self._get_middle(List)
        code2 = self._get_code(List, middle)
    
        return self._comp_code(code1, code2)
    
    def _get_code(self,List,middle):
        result = []
        for index in range(0,len(List)):
            if List[index] > middle:
                result.append("1")
            else:
                result.append("0")
        return result
    
    def _comp_code(self,code1,code2):
        num = 0
        for index in range(0,len(code1)):
            if str(code1[index]) != str(code2[index]):
                num+=1
        return num
    
    def _get_middle(self,List):
        li = deepcopy(List)
        li.sort()
        value = 0
        if len(li)%2==0:
            index = int((len(li)/2)) - 1
    
            value = li[index]
        else:
            index = int((len(li)/2))
            value = (li[index]+li[index-1])/2
        return value
    
    def _get_matrix(self,image):
    
        matrix = []
        size = image.size
        for height in range(0,size[1]):
            pixel = []
            for width in range(0,size[0]):
                pixel_value = image.getpixel((width,height))
                pixel.append(pixel_value)
            matrix.append(pixel)    
    
        return matrix
    
    def _get_coefficient(self,n):
        matrix = []
        PI = math.pi
        sqr = math.sqrt(1/n)
        value = []
        for i in range(0,n):
            value.append(sqr)
        matrix.append(value)
    
        for i in range(1,n):
            value=[]
            for j in range (0,n):
                data = math.sqrt(2.0/n) * math.cos(i*PI*(j+0.5)/n);  
                value.append(data)
            matrix.append(value)
    
        return matrix
    
    def _get_transposing(self,matrix):
        new_matrix = []
    
        for i in range(0,len(matrix)):
            value = []
            for j in range(0,len(matrix[i])):
                value.append(matrix[j][i])
            new_matrix.append(value)
    
        return new_matrix
    
    def _get_mult(self,matrix1,matrix2):
        new_matrix = []
    
        for i in range(0,len(matrix1)):
            value_list = []
            for j in range(0,len(matrix1)): 
                t = 0.0
                for k in range(0,len(matrix1)):
                    t += matrix1[i][k] * matrix2[k][j]
                value_list.append(t)
            new_matrix.append(value_list)
    
        return new_matrix
    
    def _DCT(self,double_matrix):
        n = len(double_matrix)
        A = self._get_coefficient(n)
        AT = self._get_transposing(A)
    
        temp = self._get_mult(double_matrix, A)
        DCT_matrix = self._get_mult(temp, AT)
    
        return DCT_matrix
        
    def _sub_matrix_to_list(self,DCT_matrix,part_size):
        w,h = part_size
        List = []
        for i in range(0,h):
            for j in range(0,w):
                List.append(DCT_matrix[i][j])
        return List    
    
    def _get_local_image_path(self):
        ctx = BUILTIN._context
        datadir = os.path.join(os.path.dirname(ctx.suite.source), 'ScreenShots')
        filename = ctx.suite.name+'_'+ctx.test.name.replace(' ', '_')+'.png'
        return os.path.join(datadir, filename)
        
if __name__ == '__main__':
    image1 = Image.open(r'C:\workspace\TestAuto\DriverDemo\org_box.jpg')
    image2 = Image.open(r'C:\workspace\TestAuto\DriverDemo\new_box.jpg')
    print image1.size
    il = ImageLib()
    print il.get_similarity(image1, image2)
    print il.compare_image(r'C:\workspace\TestAuto\DriverDemo\org.jpg', r'C:\workspace\TestAuto\DriverDemo\new.jpg', '6,280,77,292')
    print il.compare_image(r'C:\workspace\TestAuto\DriverDemo\org.jpg', r'C:\workspace\TestAuto\DriverDemo\org.jpg', '6,280,77,292')
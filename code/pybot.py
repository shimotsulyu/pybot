import pyautogui
from PIL import Image
import time
import math
class Actions:
    def __init__(self, config=[10, 1, 4, 8, 0.9], region=(0, 0, pyautogui.size()[0], pyautogui.size()[1])):
        self.region = region
        self.persist = config[0]
        self.time_persist = config[1]
        self.delay = config[2]
        self.long_delay = config[3]
        self.confidence = config[4]

    def reduceImage(self, target, confidence, group=False):
        im = Image.open(f"images/{target}.png")
        width, height = im.size
        for i in range(100, 20, -5):
            im1 = im.resize((int(width * (i / 100)), int(height * (i / 100))))
            if (not group):
                _click = pyautogui.locateCenterOnScreen(im1, confidence=confidence,
                                                    region=self.region)
                _box = pyautogui.locateOnScreen(im1, confidence=confidence,
                                                    region=self.region)
            else:
                _click = None
                _box = list(pyautogui.locateAllOnScreen(im1, confidence=self.confidence,
                                                    region=self.region))
            if (_click is not None) or (_click is not []):
                return _click, _box
        return None

    def searchTarget(self, target, confidence=None, group=False):
        if confidence is None: confidence = self.confidence
        for i in range(self.persist):
            time.sleep(0.2)
            print(f"Procurando {target}")
            _click, _box = self.reduceImage(target, confidence, group=group)
            if _click is not None:
                break
            time.sleep(self.delay)
        return _click, _box

    def oneClick(self, target, confidence=None, stopOnFail=True):
        if target == 'Invalid input': return False
        if confidence is None: confidence = self.confidence
        _click = self.searchTarget(target,confidence)[0]
        if _click is not None:
            pyautogui.click(_click)
            print(f"  Clicou! {_click}")
            return True
        else:
            print("Não econtrou!")
            return False

    def doubleClick(self, target, confidence=None, stopOnFail=True):
        if confidence is None: confidence = self.confidence
        _click = self.searchTarget(target,confidence)[0]
        if _click is not None:
            pyautogui.doubleClick(_click)
            print(f"  Clicou! {_click}")
            return True
        else:
            print("Não econtrou!")
            return False

    def drag(self, pos0, pos1, stopOnFail=True):
        pyautogui.moveTo(pos0[0], pos0[1])
        pyautogui.dragTo(pos1[0], pos1[1], button='left')
        print("Moveu peça!")

    def checkNotOverlapping(self,img,imgRef):
        return math.sqrt((img[0]-imgRef[0])**2) > imgRef[2] or math.sqrt((img[1]-imgRef[1])**2) > imgRef[3]

    def checkNotOnList(self,list,img):
        for imgRef in list:
            if not self.checkNotOverlapping(img,imgRef): return False
        return True

    def groupByElements(self, target, confidence=None):
        if confidence is None: confidence = self.confidence
        element_found = list(pyautogui.locateAllOnScreen(f'images/{target}.png', confidence=confidence,
                                         region=self.region))
        elements = [element_found[0]]
        for img in element_found:
            if self.checkNotOnList(elements,img): elements.append(img)
        return elements

    def selectRandonElement(self):
        #seleciona um elemento
        return [0,0]



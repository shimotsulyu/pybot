import pyautogui
from PIL import Image
import time

class Actions:
    def __init__(self, config=[10, 1, 4, 8, 0.9], region=(0, 0, pyautogui.size()[0], pyautogui.size()[1])):
        self.region = region
        self.persist = config[0]
        self.time_persist = config[1]
        self.delay = config[2]
        self.long_delay = config[3]
        self.confidence = config[4]

    def reduceImage(self, target, confidence):
        im = Image.open(f"images/{target}.png")
        width, height = im.size
        for i in range(100, 20, -5):
            im1 = im.resize((int(width * (i / 100)), int(height * (i / 100))))
            _click = pyautogui.locateCenterOnScreen(im1, confidence=confidence,
                                                    region=self.region)
            if _click is not None:
                return _click

    def searchTarget(self, target, confidence):
        t0 = time.time()
        for i in range(self.persist):
            time.sleep(0.2)
            print(f"Procurando {target}")
            _click = self.reduceImage(target, confidence)
            if _click is not None:
                #print(_click)
                break
            time.sleep(self.delay)
        #print(f"dt: {time.time()-t0}s")
        return _click

    def oneClick(self, target, confidence=None, stopOnFail=True):
        if confidence is None: confidence = self.confidence
        _click = self.searchTarget(target,confidence)
        if _click is not None:
            pyautogui.click(_click)
            print(f"  Clicou! {_click}")
            return True
        else:
            print("Não econtrou!")
            return False

    def doubleClick(self, target, confidence=None, stopOnFail=True):
        if confidence is None: confidence = self.confidence
        _click = self.searchTarget(target,confidence)
        if _click is not None:
            pyautogui.doubleClick(_click)
            print(f"  Clicou! {_click}")
            return True
        else:
            print("Não econtrou!")
            return False

    #def hotKey(self, key):
        #pyautogui.hotkey(key)

    def drag(self, pos0, pos1, stopOnFail=True):
        pyautogui.moveTo(pos0[0], pos0[1])
        pyautogui.dragTo(pos1[0], pos1[1], button='left')
        print("Moveu peça!")

    def groupByElements(self, target):
        #código para agrupar os elementos iguais]
        elements = list(pyautogui.locateAllOnScreen(f'images/{target}.png',
                                                confidence=self.confidence,
                                                region=self.region))
        return elements

    def selectRandonElement(self):
        #seleciona um elemento
        return [0,0]
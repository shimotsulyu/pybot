from io import BytesIO
from PIL import Image
import PySimpleGUI as sg
import pyautogui
class Crop:
    def __init__(self,reside=1):
        self.reside = reside
        self.screen = pyautogui.size()
        print(self.screen)
        screen = [int(self.screen[0] / reside), int(self.screen[1] / reside)]
        print(screen)
        image = pyautogui.screenshot()
        im = image.resize((screen[0], screen[1]), resample=Image.CUBIC)
        with BytesIO() as output:
            im.save(output, format="PNG")
            data = output.getvalue()
        layout = [
            [sg.Graph((screen[0], screen[1]), (0, 0), (screen[0], screen[1]), key='-GRAPH-',
                      drag_submits=True, enable_events=True, background_color='green')],
            [sg.Text("Start: None", key="-START-"),
             sg.Text("Stop: None", key="-STOP-"),
             sg.Text("Box: None", key="-BOX-")],
        ]
        self.window = sg.Window("Measure", layout, finalize=True)
        self.graph = self.window['-GRAPH-']
        self.graph.draw_image(data=data, location=(0, screen[1]))

    def convertRealSize(self, x0, y0, x1, y1):
        x0 = x0 * self.reside
        y0 = self.screen[1] - y0 * self.reside
        x1 = x1 * self.reside
        y1 = self.screen[1] - y1 * self.reside
        return x0, y0, x1, y1

    def update(self, x0, y0, x1, y1):
        x0, y0, x1, y1 = self.convertRealSize(x0, y0, x1, y1)
        #print(repr(x0), repr(y0), repr(x1), repr(y1))
        self.window['-START-'].update(f'Start: ({x0}, {y0})')
        self.window['-STOP-' ].update(f'Start: ({x1}, {y1})')
        self.window['-BOX-'  ].update(f'Box: ({abs(x1-x0+1)}, {abs(y1-y0+1)})')
        return [x0, y0, x1, y1]

    def crop(self):
        x0, y0 = None, None
        x1, y1 = None, None
        colors = ['blue', 'white']
        index = False
        figure = None
        while True:
            event, values = self.window.read(timeout=100)
            if event == sg.WINDOW_CLOSED:
                return box
                break
            elif event in ('-GRAPH-', '-GRAPH-+UP'):
                if (x0, y0) == (None, None):
                    x0, y0 = values['-GRAPH-']
                x1, y1 = values['-GRAPH-']
                box = self.update(x0, y0, x1, y1)
                if event == '-GRAPH-+UP':
                    x0, y0 = None, None
            if figure:
                self.graph.delete_figure(figure)
            if None not in (x0, y0, x1, y1):
                figure = self.graph.draw_rectangle((x0, y0), (x1, y1), line_color=colors[index])
                index = not index
        self.window.close()
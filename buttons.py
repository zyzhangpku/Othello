class Button:

    def __init__(self, x, y, text, react_func, w=150, h=50):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.text = text
        self.react_func = react_func

    def react(self):
        if not self.react_func:
            return
        self.react_func()

    def activate(self, x_mouse, y_mouse):
        return self.x <= x_mouse <= self.x + self.w and self.y <= y_mouse <= self.y + self.h

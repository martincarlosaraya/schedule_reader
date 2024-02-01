class Counter(object):
    def __init__(self, start:int=0, step:int=1):
        if step == 0:
            raise ValueError(f"The `step` can't be zero!")
        self.start = start
        self.step = step
        self.current = start - step

    def next(self):
        self.current += self.step
        return self.current
    
    def curr(self):
        return self.current if self.current >= self.start else self.start

    def prev(self):
        self.current -= self.step
        
    def __call__(self, count=True):
        if count is None:
            return None
        elif count:
            return self.next()
        elif not count:
            return self.curr()
        else:
            return None
    
    def __add__(self, other:int):
        self.current = self.curr + other
        return self.curr()

    def __sub__(self, other:int):
            self.current = self.curr - other
            return self.curr()

    def __mult__(self, other:int):
            self.current = self.curr * other
            return self.curr()

    def __repr__(self):
        return f"{self.curr()} counted"

def start_counter(start:int):
    return Counter(start)

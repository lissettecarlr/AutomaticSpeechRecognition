# kuonasr/core/base.py

class ASRBase:
    def __init__(self):
        pass

    def recognize(self, audio):
        raise NotImplementedError("Subclasses should implement this!")

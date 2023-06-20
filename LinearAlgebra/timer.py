import time

class TimerError(Exception):
    pass
class Timer():
    timers = {}
    def __init__(self,
                 aufgabe=None,
                 text: str ="Zeitaufwand mit den Aufgaben: {:0.4f}",
                 print: bool = False                 
                 ):
        
        self._beginzeit = None
        self.text = text
        self.aufgabe = aufgabe
        self.print=print

        if aufgabe:
            self.timers.setdefault(aufgabe, 0)

    def start(self):
        if self._beginzeit:
            raise TimerError(f'Zeitzahler bereits starten, bitte stoppen Sie ihn')
        
        self._beginzeit = time.perf_counter()
            

    def stop(self):
        if not self.start:
            raise TimerError(f'Zeitzahler noch nicht starten, bitte starten Sie ihn')

        zeit = (time.perf_counter() - self._beginzeit)
        self._beginzeit = None
        if self.print:
            print(self.text.format(zeit))

        if self.aufgabe:
            self.timers[self.aufgabe] += zeit

        return zeit

#Testen
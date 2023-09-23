"""
Lib for simple text progress bars like this:
Loading... |#######         |

firstly we need to create variable:
>>> progress = ProgressLib.ProgressBar([...])
[...]: args like name or total value...

next we create a loop:
for x in range(100):
    progress.plot() - draw progressbar on the screen
    progress.add(1) - add 1 to valueof the progress bar !ALT!: progress.set(x)

"""


import time
from colorama import Fore, Back, Style, init
init(True)

class ConversionError(Exception): ...

class ProgressBar:
    '''
    --- needed ---\n
    name: name of the progress bar
    total: total value of the progress bar
    color: color of main characters
    divisor: scale f.e. divisor=5 means 1 "#" = (100/5=20) iterations

    --- optional --- \n
    fillchar: char representing uncompleted piece of bar  [def: " "]
    mainChar: char representing completed piece of bar    [def: "#"]
    startChar: char that starts progress bar              [def: "|"]
    endChar: char that ends a progress bar                [def: "|"]\n
    ======================================================================
    '''
    def __init__(self, name: str, total: int | float, divisor: int, initial: int | None=0, color=Fore.WHITE, fill_char: str | None=' ', main_char: str | None='#', start_char: str | None='|', ending_char: str | None='|') -> None:
        self.name = name,
        self.total = total
        self.color = color
        self.fillchr = fill_char
        self.mainchr = main_char
        self.startchr = start_char
        self.endchr = ending_char
        self.val = initial
        self.divisor = divisor
        
    
    def __str__(self) -> str:
        raise ConversionError('Unconvertable object')
    
    def plot(self):
        """
        Plot the `bar` on the screen
        structure:
        name |#######   | percentage -> #if selected
        """
        if self.val < self.total:
            print(f"{self.name[0]}  {self.startchr}{self.color}{self.mainchr * (self.val//self.divisor)}{self.fillchr * ((self.total - self.val)//self.divisor)}{Fore.RESET}{self.endchr}", end='\r')

        # elif self.val > self.total:
            # print(str(self.name) + '  ' + str(self.startchr) + self.mainchr)

    def set(self, value: int):'set the custom value of the progress bar'; self.val = value
    def add(self, value: int):'Add to the value of the progress RECOMMENDED'; self.val += value

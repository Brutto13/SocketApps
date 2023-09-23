from colorama import Fore, init
import progressBar
import time
init(True)

bar = progressBar.ProgressBar('test0001', 100, 1, color=Fore.GREEN)
done = False
while not done:
    try:
        bar.plot()
        bar.add(1)
        time.sleep(0.1)
    except KeyboardInterrupt:
        done = True
input()
    

from tqdm import tqdm
import time

def loading():
    for i in tqdm(range(100)):
        time.sleep(0.05)

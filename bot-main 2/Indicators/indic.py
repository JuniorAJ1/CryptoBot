import numpy as np
import pandas as pd

def calculate_ema(data, span=50):
    return data['close'].ewm(span=span, adjust=False).mean()

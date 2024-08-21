def detect_candlestick_patterns(data, index, pattern):
    if index == 0:
        return False
    prev_candle = data.iloc[index - 1]
    curr_candle = data.iloc[index]
    if curr_candle['high'] < prev_candle['high'] and curr_candle['low'] > prev_candle['low']:
        return "Inside Bar"
    return False

def detect_bullish_trend_continuation(data):
    # Find all higher highs and higher lows in the data
    higher_highs = [
        i for i in range(1, len(data)-1)
        if data['high'][i] > data['high'][i-1] and data['high'][i] > data['high'][i+1]
    ]
    higher_lows = [
        i for i in range(1, len(data)-1)
        if data['low'][i] > data['low'][i-1] and data['low'][i] > data['low'][i+1]
    ]
    
    # Check if there are at least two higher highs and higher lows
    if len(higher_highs) >= 2 and len(higher_lows) >= 2:
        return True, higher_highs[-1], higher_lows[-1]
    else:
        return False, None, None

def detect_bearish_trend_continuation(data):
    # Find all lower highs and lower lows in the data
    lower_highs = [
        i for i in range(1, len(data)-1)
        if data['high'][i] < data['high'][i-1] and data['high'][i] < data['high'][i+1]
    ]
    lower_lows = [
        i for i in range(1, len(data)-1)
        if data['low'][i] < data['low'][i-1] and data['low'][i] < data['low'][i+1]
    ]
    
    # Check if there are at least two lower highs and lower lows
    if len(lower_highs) >= 2 and len(lower_lows) >= 2:
        return True, lower_highs[-1], lower_lows[-1]
    else:
        return False, None, None
    

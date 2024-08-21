# Function to detect a trend change to bullish (uptrend)
def detect_trend_change_bullish(data):
    # Loop through the data points
    for i in range(1, len(data) - 1):
        # Check if current low and high are higher than the previous low and high (uptrend)
        if data['low'][i] > data['low'][i - 1] and data['high'][i] > data['high'][i - 1]:
            # Check if the next low and high are lower than the current low and high (reversal)
            if data['low'][i + 1] < data['low'][i] and data['high'][i + 1] < data['high'][i]:
                return True, i  # Trend change detected, return True and the index
    return False, None  # No trend change detected, return False and None

# Function to detect a trend change to bearish (downtrend)
def detect_trend_change_bearish(data):
    # Loop through the data points
    for i in range(1, len(data) - 1):
        # Check if current high and low are lower than the previous high and low (downtrend)
        if data['high'][i] < data['high'][i - 1] and data['low'][i] < data['low'][i - 1]:
            # Check if the next high and low are higher than the current high and low (reversal)
            if data['high'][i + 1] > data['high'][i] and data['low'][i + 1] > data['low'][i]:
                return True, i  # Trend change detected, return True and the index
    return False, None  # No trend change detected, return False and None

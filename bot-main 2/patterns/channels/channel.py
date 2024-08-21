def detect_ascending_channel(data):
    # Look for an Ascending Channel pattern in the data
    for i in range(1, len(data) - 1):
        # Check if the current high and low are higher than the previous high and low
        if data['high'][i] > data['high'][i-1] and data['low'][i] > data['low'][i-1]:
            for j in range(i + 1, len(data) - 1):
                # Check if the next high and low are higher than the current high and low
                if data['high'][j] > data['high'][i] and data['low'][j] > data['low'][i]:
                    # Found an Ascending Channel pattern
                    return True, i, j
    # No Ascending Channel pattern found
    return False, None, None

def detect_descending_channel(data):
    # Look for a Descending Channel pattern in the data
    for i in range(1, len(data) - 1):
        # Check if the current high and low are lower than the previous high and low
        if data['high'][i] < data['high'][i-1] and data['low'][i] < data['low'][i-1]:
            for j in range(i + 1, len(data) - 1):
                # Check if the next high and low are lower than the current high and low
                if data['high'][j] < data['high'][i] and data['low'][j] < data['low'][i]:
                    # Found a Descending Channel pattern
                    return True, i, j
    # No Descending Channel pattern found
    return False, None, None

def detect_horizontal_channel(data):
    # Look for a Horizontal Channel pattern in the data
    for i in range(1, len(data) - 1):
        # Check if the current high and low are within a certain range of the previous high and low
        if abs(data['high'][i] - data['high'][i-1]) <= (data['high'][i] * 0.01) and abs(data['low'][i] - data['low'][i-1]) <= (data['low'][i] * 0.01):
            for j in range(i + 1, len(data) - 1):
                # Check if the next high and low are within a certain range of the current high and low
                if abs(data['high'][j] - data['high'][i]) <= (data['high'][j] * 0.01) and abs(data['low'][j] - data['low'][i]) <= (data['low'][j] * 0.01):
                    # Found a Horizontal Channel pattern
                    return True, i, j
    # No Horizontal Channel pattern found
    return False, None, None

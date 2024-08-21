def detect_rising_wedge(data):
    # Look for a Rising Wedge pattern in the data
    for i in range(1, len(data) - 1):
        # Check if the current high is lower than the previous high
        # and the current low is higher than the previous low
        if data['high'][i] < data['high'][i-1] and data['low'][i] > data['low'][i-1]:
            for j in range(i + 1, len(data) - 1):
                # Check if the next high is lower than the current high
                # and the next low is higher than the current low
                if data['high'][j] < data['high'][i] and data['low'][j] > data['low'][i]:
                    # Found a Rising Wedge pattern
                    return True, i, j
    # No Rising Wedge pattern found
    return False, None, None

def detect_falling_wedge(data):
    # Look for a Falling Wedge pattern in the data
    for i in range(1, len(data) - 1):
        # Check if the current high is higher than the previous high
        # and the current low is lower than the previous low
        if data['high'][i] > data['high'][i-1] and data['low'][i] < data['low'][i-1]:
            for j in range(i + 1, len(data) - 1):
                # Check if the next high is higher than the current high
                # and the next low is lower than the current low
                if data['high'][j] > data['high'][i] and data['low'][j] < data['low'][i]:
                    # Found a Falling Wedge pattern
                    return True, i, j
    # No Falling Wedge pattern found
    return False, None, None

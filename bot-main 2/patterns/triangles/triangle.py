def detect_ascending_triangle(data):
    # Look for an Ascending Triangle pattern in the data
    for i in range(1, len(data) - 1):
        # Check if the current high is higher than the previous high
        # and the current low is higher or equal to the previous low
        if data['high'][i] > data['high'][i-1] and data['low'][i] >= data['low'][i-1]:
            for j in range(i + 1, len(data) - 1):
                # Check if the next high is equal to the current high
                # and the next low is higher or equal to the current low
                if data['high'][j] == data['high'][i] and data['low'][j] >= data['low'][i]:
                    # Found an Ascending Triangle pattern
                    return True, i, j
    # No Ascending Triangle pattern found
    return False, None, None

def detect_descending_triangle(data):
    # Look for a Descending Triangle pattern in the data
    for i in range(1, len(data) - 1):
        # Check if the current low is lower than the previous low
        # and the current high is lower or equal to the previous high
        if data['low'][i] < data['low'][i-1] and data['high'][i] <= data['high'][i-1]:
            for j in range(i + 1, len(data) - 1):
                # Check if the next low is equal to the current low
                # and the next high is lower or equal to the current high
                if data['low'][j] == data['low'][i] and data['high'][j] <= data['high'][i]:
                    # Found a Descending Triangle pattern
                    return True, i, j
    # No Descending Triangle pattern found
    return False, None, None

def detect_symmetrical_triangle(data):
    # Look for a Symmetrical Triangle pattern in the data
    for i in range(1, len(data) - 1):
        # Check if the current high is higher than the previous high
        # and the current low is lower than the previous low
        if data['high'][i] > data['high'][i-1] and data['low'][i] < data['low'][i-1]:
            for j in range(i + 1, len(data) - 1):
                # Check if the next high is lower than the current high
                # and the next low is higher than the current low
                if data['high'][j] < data['high'][i] and data['low'][j] > data['low'][i]:
                    # Found a Symmetrical Triangle pattern
                    return True, i, j
    # No Symmetrical Triangle pattern found
    return False, None, None

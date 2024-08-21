# Function to detect a potential Head and Shoulders pattern
def detect_head_and_shoulders(data):
    # List to store potential shoulder points
    shoulders = []
    # Loop through the data points
    for i in range(1, len(data) - 1):
        # Check if the current point is higher than the points before and after (potential shoulder or head)
        if data['high'][i] > data['high'][i-1] and data['high'][i] > data['high'][i+1]:
            shoulders.append((i, data['high'][i]))
    # If we have at least 3 potential shoulders
    if len(shoulders) >= 3:
        # Identify left shoulder, head, and right shoulder
        left_shoulder, head, right_shoulder = shoulders[-3], shoulders[-2], shoulders[-1]
        # Check if the head is higher than both shoulders
        if left_shoulder[1] < head[1] and right_shoulder[1] < head[1]:
            return True, left_shoulder, head, right_shoulder
    # If pattern is not found, return False and None
    return False, None, None, None

# Function to detect a potential Inverse Head and Shoulders pattern
def detect_inverse_head_and_shoulders(data):
    # List to store potential shoulder points
    shoulders = []
    # Loop through the data points
    for i in range(1, len(data) - 1):
        # Check if the current point is lower than the points before and after (potential shoulder or head)
        if data['low'][i] < data['low'][i-1] and data['low'][i] < data['low'][i+1]:
            shoulders.append((i, data['low'][i]))
    # If we have at least 3 potential shoulders
    if len(shoulders) >= 3:
        # Identify left shoulder, head, and right shoulder
        left_shoulder, head, right_shoulder = shoulders[-3], shoulders[-2], shoulders[-1]
        # Check if the head is lower than both shoulders
        if left_shoulder[1] > head[1] and right_shoulder[1] > head[1]:
            return True, left_shoulder, head, right_shoulder
    # If pattern is not found, return False and None
    return False, None, None, None

# Function to detect an early aggressive entry point based on shoulders
def detect_early_aggressive_entry(data, pattern_type, left_shoulder, right_shoulder):
    # For Head and Shoulders pattern
    if pattern_type == "head_and_shoulders":
        # Entry level is the lowest point of the left shoulder
        entry_level = data['low'][left_shoulder[0]]
        # Loop through the points between the shoulders to find an early entry
        for i in range(left_shoulder[0] + 1, right_shoulder[0]):
            if data['low'][i] <= entry_level:
                return True, i
    # For Inverse Head and Shoulders pattern
    elif pattern_type == "inverse_head_and_shoulders":
        # Entry level is the highest point of the left shoulder
        entry_level = data['high'][left_shoulder[0]]
        # Loop through the points between the shoulders to find an early entry
        for i in range(left_shoulder[0] + 1, right_shoulder[0]):
            if data['high'][i] >= entry_level:
                return True, i
    # If no early entry is found, return False and None
    return False, None
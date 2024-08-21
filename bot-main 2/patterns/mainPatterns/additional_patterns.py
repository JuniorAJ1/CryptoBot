# Additional Pattern Functions
# ----------------------------

# Function to detect if the neckline is broken in a double or triple top/bottom pattern
def detect_neckline_break(data, pattern, level):
    if pattern in ["double_top", "triple_top"]:
        # Check from the last data point to the first
        for i in range(len(data)-1, 0, -1):
            # If the price goes below the neckline level, return True and the index
            if data['low'][i] < level:
                return True, i
    elif pattern in ["double_bottom", "triple_bottom"]:
        # Check from the last data point to the first
        for i in range(len(data)-1, 0, -1):
            # If the price goes above the neckline level, return True and the index
            if data['high'][i] > level:
                return True, i
    # If no break is found, return False and None
    return False, None

# Function to detect if there is a pullback after a neckline break
def detect_pullback(data, break_index, pattern):
    if pattern in ["double_top", "triple_top"]:
        # Check if any high price after the break index is higher than the high at the break index
        return any(data['high'][i] >= data['high'][break_index] for i in range(break_index, len(data)))
    elif pattern in ["double_bottom", "triple_bottom"]:
        # Check if any low price after the break index is lower than the low at the break index
        return any(data['low'][i] <= data['low'][break_index] for i in range(break_index, len(data)))
    # If no pullback is detected, return False
    return False

# Function to evaluate the strength of a detected pattern
def evaluate_pattern_strength(pattern, data, break_index):
    # Check criteria for pattern strength
    if pattern in ["double_top", "double_bottom", "triple_top", "triple_bottom"]:
        # Check if there is a significant volume spike at the break index
        significant_volume = data['volume'][break_index] > data['volume'].mean() * 1.5
        return significant_volume
    # If pattern is not one of the specified types, return False
    return False

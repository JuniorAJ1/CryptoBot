# Double Pattern Recognition Section
# ---------------------------

# Double Top Pattern
def detect_double_top(data):
    # Find all the high points in the data
    tops = [
        (i, data['high'][i])
        for i in range(1, len(data)-1)
        if data['high'][i] > data['high'][i-1] and data['high'][i] > data['high'][i+1]
    ]
    
    # Check if there are at least two high points and if they are almost the same height
    if len(tops) >= 2 and abs(tops[-1][1] - tops[-2][1]) / tops[-2][1] < 0.01:
        return True, tops[-2], tops[-1]
    else:
        return False, None, None

def detect_double_bottom(data):
    # Find all the low points in the data
    bottoms = [
        (i, data['low'][i])
        for i in range(1, len(data)-1)
        if data['low'][i] < data['low'][i-1] and data['low'][i] < data['low'][i+1]
    ]
    
    # Check if there are at least two low points and if they are almost the same depth
    if len(bottoms) >= 2 and abs(bottoms[-1][1] - bottoms[-2][1]) / bottoms[-2][1] < 0.01:
        return True, bottoms[-2], bottoms[-1]
    else:
        return False, None, None

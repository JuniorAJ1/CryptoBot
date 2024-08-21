def detect_triple_top(data):
    # Find all the high points in the data
    tops = [
        (i, data['high'][i]) 
        for i in range(1, len(data)-1) 
        if data['high'][i] > data['high'][i-1] and data['high'][i] > data['high'][i+1]
    ]
    
    # Check if there are at least three high points and if they are almost the same height
    if len(tops) >= 3 and abs(tops[-1][1] - tops[-2][1]) / tops[-2][1] < 0.01 and abs(tops[-2][1] - tops[-3][1]) / tops[-3][1] < 0.01:
        return True, tops[-3], tops[-2], tops[-1]
    else:
        return False, None, None, None

def detect_triple_bottom(data):
    # Find all the low points in the data
    bottoms = [
        (i, data['low'][i]) 
        for i in range(1, len(data)-1) 
        if data['low'][i] < data['low'][i-1] and data['low'][i] < data['low'][i+1]
    ]
    
    # Check if there are at least three low points and if they are almost the same depth
    if len(bottoms) >= 3 and abs(bottoms[-1][1] - bottoms[-2][1]) / bottoms[-2][1] < 0.01 and abs(bottoms[-2][1] - bottoms[-3][1]) / bottoms[-3][1] < 0.01:
        return True, bottoms[-3], bottoms[-2], bottoms[-1]
    else:
        return False, None, None, None

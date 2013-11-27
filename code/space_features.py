def features(bar_info, cur_bounds, next_bounds):
    """Takes the horizontal bar information, the bounds of previous(A),
    current (B) and next(C) symbol, and label of the previous symbol 
    computes the features."""
    """
    TO DO: adjust centers according to previous symbols and the symbol type 
    
    if prev_label in [3, 4]: #if subscript or superscript modify vertical bounds 
    #so reflects the 
                            # previous symbol
        cur_bounds[3] = prev_bounds[3]
        cur_bounds[1] = prev_bounds[1]
    
    if prev_label == 0:
        cur_bounds[3] += prev_bounds[3]
        cur_bounds[1] += prev_bounds[1]
        cur_bounds[3] /= 2 
        cur_bounds[1] /= 2
    """
    ver_center_B = 0.5*(cur_bounds[3]+cur_bounds[1]) 
    ver_center_C = 0.5*(next_bounds[3]+next_bounds[1]) 
    hor_center_B = 0.5*(cur_bounds[2]+cur_bounds[0]) 
    hor_center_C = 0.5*(next_bounds[2]+next_bounds[0]) 
        
    hB = cur_bounds[3] - cur_bounds[1]
    hC = next_bounds[3] - next_bounds[1]
    
    
    H = hC/hB
    D = 0.5*(ver_center_B - ver_center_C)
    dhC = 0.5*(hor_center_B - hor_center_C)
    
    dx = (next_bounds[0] - cur_bounds[2])/hB
    dx1 = (next_bounds[0] - cur_bounds[0])/hB
    dx2 = (next_bounds[2] - cur_bounds[2])/hB

    dy = (next_bounds[3] - cur_bounds[1])/hB
    dy1 = (next_bounds[1] - cur_bounds[1])/hB
    dy2 = (next_bounds[3] - cur_bounds[3])/hB
    
    # bar_info[0] list of widths of bars [x1, x2], 
    # bar_info[1] list of y positions of bars
    bar_up = 0
    bar_down = 0
    
    for i, xbar in enumerate(bar_info[0]):
        if cur_bounds[2] < xbar[1] and cur_bounds[0] > xbar[0]:
            if bar_info[1][i] > ver_center_B:
                bar_up = 1
            else:
                bar_down = 1
        
    features = [H, D, dhC, dx, dx1, dx2, dy, dy1, dy2, bar_up, bar_down]
    return features
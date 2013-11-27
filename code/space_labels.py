import bisect

def loop_ML(mathML, label, list_sym_label):
    """
    Takes in the mathml object and a list of symbols, and outputs spatial labels 
    for each symbol. The labels are list of nested spatial relations, i.e. for 
    values 0, 0.1, -1, 1, 0.5, -0.5, 2, -2 denoting base, square root, subscript, 
    superscript, numerator, denominator, over, and under respectively, we can have 
    for x in $\frac{a+b}{\frac{2^x}{3+6}}$ we would have an output 
    ['x', [-0.5, 0.5, 1]], for y in $a^{\frac{1}{\frac{b_y}{z+w}}}$ the output 
    would be ['y', [1, -0.5, 0.5, -1]], for z in $\sqrt{b^{z} - 4 a c}$ the output
    would be ['z', [2, 1]].
    """
    
    if mathML == None:
        print 'list_sym_label', list_sym_label
        
    if mathML.findall('*') == []:
        if label == []: 
            label.append(0)
        list_sym_label.append([mathML.text, label])
        label = []
              
    else:
                
            if mathML.tag == '{http://www.w3.org/1998/Math/MathML}mfrac':
                
                a = label + [0]
                list_sym_label.append(['-', a])               
                a = label+ [0.5]
                b = label+ [-0.5]
                loop_ML(mathML[0], a, list_sym_label)
                loop_ML(mathML[1], b, list_sym_label)
            
            elif mathML.tag == '{http://www.w3.org/1998/Math/MathML}msubsup':
                a = label + [0]
                b = label + [-1]
                c = label +[1]
                loop_ML(mathML[0], a, list_sym_label)
                loop_ML(mathML[1], b, list_sym_label)
                loop_ML(mathML[2], c, list_sym_label)
    
            elif mathML.tag == '{http://www.w3.org/1998/Math/MathML}msup':
                a = label+ [0]
                b = label+ [1]
                loop_ML(mathML[0], a, list_sym_label)
                loop_ML(mathML[1], b, list_sym_label)
                 
            elif mathML.tag == '{http://www.w3.org/1998/Math/MathML}msub':
                a = label+ [0]
                b = label+ [-1]
                loop_ML(mathML[0], a, list_sym_label)
                loop_ML(mathML[1], b, list_sym_label)
                
            elif mathML.tag == '{http://www.w3.org/1998/Math/MathML}msqrt':
                a = label + [0]
                list_sym_label.append(['\\sqrt', a])
                b = label+ [0.1]
                for child in mathML:
                    loop_ML(child, b, list_sym_label)
                      
            elif mathML.tag == '{http://www.w3.org/1998/Math/MathML}munderover':
                a = label + [0]
                b = label + [-2]
                c = label +[2]
                loop_ML(mathML[0], a, list_sym_label)
                loop_ML(mathML[1], b, list_sym_label)
                loop_ML(mathML[2], c, list_sym_label)
            
            elif mathML.tag == '{http://www.w3.org/1998/Math/MathML}mover':
                a = label+ [0]
                b = label+ [2]
                loop_ML(mathML[0], a, list_sym_label)
                loop_ML(mathML[1], b, list_sym_label)
                 
            elif mathML.tag == '{http://www.w3.org/1998/Math/MathML}munder':
                a = label+ [0]
                b = label+ [-2]
                loop_ML(mathML[0], a, list_sym_label)
                loop_ML(mathML[1], b, list_sym_label)
    
                               
            else:
                for child in mathML:
                    loop_ML(child, label, list_sym_label)
    
    return list_sym_label

def space_relations(list_sym_label):
    """Takes nested positions information from loop_ML() and converts into nearest
    neighbor relation-class. Returns list_space_relations, where 
    list_space_relations[i] = [symbol, label]. Labels are integers
    denoting different classes of spatial relations."""
    
    list_space_relations = []
    
    horizontal = 0
    vertical_up = 1 
    vertical_down = 2 
    superscript = 3
    subscript = 4
    inside = 5
    horizontal_bar = 6
    end = 7
    label = 1000
                      
    for i in range(len(list_sym_label)):
        ele0 = list_sym_label[i]
        symbol0 = ele0[0]
        label0 = ele0[1]
                    
        if i != len(list_sym_label)-1:
            ele1 = list_sym_label[i+1]
            symbol1 = ele1[0]
            label1 = ele1[1]
                                  
            if len(label0) == len(label1): 
                index0 = -1
                index1 = -1
            
            elif len(label0) < len(label1):
                index0 = -1
                index1 = len(label0)-1
            
            elif len(label0) > len(label1):
                index0 = len(label1)-1
                index1 = -1
                
            if (label0[index0] < 2 and label1[index1] == 2) or \
               (label0[index0] != 0.5 and label1[index1] == 0.5) or \
               (label0[index0] == -1 and label1[index1] == 1):
                label = vertical_up
                
            elif (label0[index0] != -2 and label1[index1] == -2) or \
                 (label0[index0] != -0.5 and label1[index1] == -0.5) or \
                 (label0[index0] == 1 and label1[index1] == -1):
                label = vertical_down
                            
            elif (label0[index0] == 0 and label1[index1] == 1) or \
                 (label0[index0] < 0 and label1[index1] == 0):
                label = superscript
                            
            elif (label0[index0] == 0 and label1[index1] == -1) or \
                 (label0[index0] >= 1 and label1[index1] == 0):
                label = subscript
                
            elif label0[index0] == label1[index1]:
                if len(label0) > len(label1):
                    sub = [i <= -0.5 for i in label0[len(label1):]]
                    sup = [i >= 0.5 for i in label0[len(label1):]]                   
                    if True in sub:
                        if True in sup:
                            if sub.index(True) < sup.index(True):
                                label = superscript
                            else:
                                label = subscript
                        else:
                            label = superscript
                    elif True in sup:
                        label = subscript
                    else:
                        label = horizontal
                elif len(label0) < len(label1):
                    sub = [i <= -0.5 for i in label1[len(label0):]]
                    sup = [i >= 0.5 for i in label1[len(label0):]]                   
                    
                    if True in sub:
                        if True in sup:
                            if sub.index(True) < sup.index(True):
                                label = subscript
                            else:
                                label = superscript
                        else:
                            label = subscript
                    elif True in sup:
                        label = superscript
                    else:
                        label = horizontal
                else:
                    label = horizontal 
            
            if symbol0 == '-' and label0[-1] == 0 and \
               label1[len(label0) - 1] == 0.5:
                label = horizontal_bar
                                                                                        
            elif label0[-1] != label1[-1] and label1[-1] == 0.1:
                label = inside
            
            list_space_relations.append([symbol0, label])
                    
        else:
            list_space_relations.append([symbol0, end])
        
        label = 1000
        
    return list_space_relations


import re

class treeNode:
    def __init__(self,val,s):
        self.val = val
        self.s = s
        self.left=None
        self.right=None

def buildTree(cur,lines):
    if len(lines)==1:
        _s = lines[0]
        val = _s.strip().split(':')[0]
        s = _s.strip().split(':')[1].split(',')[0]
        return treeNode(int(val),s)
    mark = []
    for i,line in enumerate(lines):
        if re.match('\t{%d}\d'%cur,line):
            mark.append(i)
    _s = lines[0]
    val = _s.strip().split(':')[0]
    __s = _s.strip().split(':[')[1].split(']')[0]
    t = treeNode(int(val),__s)
    t.left = buildTree(cur+1,lines[mark[0]:mark[1]])
    t.right= buildTree(cur+1,lines[mark[1]:])
    return t

def get_tree(it):
    tree = []
    while True:
        line = next(it,'end')
        if re.search('booster',line):
            if tree:
                yield tree
                tree=  []
        elif line == 'end':
            yield tree
            break
        else:
            tree.append(line)
            
def get_path(a,leaf):
    depth = -1
    for i in range(1,len(a)+1):
        line = a[-i]
        if depth == -1:
            ser = re.search('%d:'%leaf,line)
            if ser:
                depth = ser.span()[0]-1
                yield line[:-1]
        else:
            if re.match('\t{%d}\d'%depth,line):
                depth -= 1
                yield line[:-1]
                
def get_leaf_str(s):
    _s = re.search('(\d*:leaf=.*),',s).groups()[0]
    return _s

def get_parent_str(s):
    _s =  re.search('([\d]*:\[.*\])',s).groups()[0]
    return _s 

def get_pp_path(tree,leaf):
    pp_path = []
    for line in get_path(tree,leaf):
        if re.search(':leaf=',line):
            pp_path.append(get_leaf_str(line))
        else:
            pp_path.append(get_parent_str(line))
    return ' => '.join(pp_path[::-1])

def get_leaf_val(s):
    return float(s.split(':leaf=')[1])

def get_row_interpret(model,y_prd,y_prd_leaf,ins):
    prd = y_prd[ins]
    leaf_lst = y_prd_leaf[ins]
    leaf_vals = []
    it = open(model)
    for i,tree in enumerate(get_tree(it)):
        pp_path = get_pp_path(tree,leaf_lst[i])
        leaf_vals.append(get_leaf_val(pp_path))
        print 'booster[%d]: %s'%(i,pp_path)
        print '-'*10
    print "="*20
    print "ins:",ins
    print "prediction:",prd
    print "prediction leaves:",leaf_lst
    print 'prediction leaves value:',leaf_vals
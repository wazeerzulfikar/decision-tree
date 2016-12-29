from math import log

def divideSet(rows,column,value):
    split_function = None
    if isinstance(value,int) or isinstance(value,float):
        split_function = lambda row: row[column]>=value
    else:
        split_function = lambda row: row[column]==value

    l1 = [row for row in rows if split_function(row)]
    l2 = [row for row in rows if not split_function(row)]
    return [l1,l2]

def valueCounts(rows):
    result = {}
    for row in rows:
        col = len(row)-1
        r = row[col]
        if r in result.keys():
            result[r] += 1
        else:
            result[r] = 1
    return result


def entropy(rows):
    result = valueCounts(rows)
    total = len(rows)
    log2 = lambda x:log(x)/log(2)
    ent = 0
    for key in result.keys():
        p = float(result[key])/total
        if p!=0:
            ent -= p*log2(p)
    return ent

class decisionNode:

    def __init__ (self, col=-1,value=None, tb=None, fb=None, results=None):
        self.value = value
        self.tb = tb
        self.fb = fb
        self.results = results
        self.col = col

def buildTree(rows,scoref = entropy):

    if len(rows) == 0:
        return decisionNode()

    parent_entropy = scoref(rows)
    best_gain = 0.0
    best_value = None
    best_rows = None
    col_count = len(rows[0])-1
    best_params = {}

    for col in range(col_count):

        values = []
        total_child_entropy = 0.0

        for row in rows:
            if row[col] not in values:
                values.append(row[col])

        for value in values:
            new_rows = divideSet(rows,col,value)
            l_child_entropy = scoref(new_rows[0])
            r_child_entropy = scoref(new_rows[1])
            weighted_av_entropy = (len(new_rows[0])*l_child_entropy + len(new_rows[1])*r_child_entropy)/len(rows)
            gain = parent_entropy - weighted_av_entropy


            if gain>best_gain and len(new_rows[0])>0 and len(new_rows[1])>0:
                best_params['column'] = col
                best_params['value'] = value
                best_gain = gain
                best_rows = (new_rows[0],new_rows[1])


    if best_gain > 0.0:
        true_branch = buildTree(best_rows[0])
        false_branch = buildTree(best_rows[1])
        return decisionNode(col=best_params['column'],value=best_params['value'],tb=true_branch,fb=false_branch)

    else:
        return decisionNode(results=valueCounts(rows))



def classify(observation,tree):
    if tree.results != None:
        return tree.results

    else:
        val = observation[tree.col]
        branch = None
        if isinstance(val,int) or isinstance(val,float):
            if val>=tree.value:
                branch = tree.tb
            else:
                branch = tree.fb

        else:
            if val == tree.value:
                branch = tree.tb
            else:
                branch = tree.fb

    return classify(observation,branch)

def printGuess(results):
    total = sum(results.values())
    for result in results.keys():
        print result +' with probability = %lf' %(results[result]/float(total))



data = [['slashdot','USA','yes',18,'None'],
        ['google','France','yes',23,'Premium'],
        ['digg','USA','yes',24,'Basic'],
        ['kiwitobes','France','yes',23,'Basic'],
        ['google','UK','no',21,'Premium'],
        ['(direct)','New Zealand','no',12,'None'],
        ['(direct)','UK','no',21,'Basic'],
        ['google','USA','no',24,'Premium'],
        ['slashdot','France','yes',19,'None'],
        ['digg','USA','no',18,'None'],
        ['google','UK','no',18,'None'],
        ['kiwitobes','UK','no',19,'None'],
        ['digg','New Zealand','yes',12,'Basic'],
        ['slashdot','UK','no',21,'None'],
        ['google','UK','yes',18,'Basic'],
        ['kiwitobes','France','yes',19,'Basic']]
tree = buildTree(data)
print classify(['(direct)','USA','yes',5],tree)
printGuess (classify(['(direct)','USA','yes',5],tree))
# print entropy(data)
# set1,set2=divideSet(data,3,20)
# print entropy(set1), entropy(set2)
# print valueCounts(data)
# print divideSet(data,2,'yes')

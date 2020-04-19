def calculate_intersection(set1, set2):
    set1Vals = []
    intersection = []
    for i in set1:
        set1Vals.append(i)
    for i in set2:
        if i in set1Vals:
            if i not in intersection:
                intersection.append(i)
    return len(intersection)

def jaccard_distance(set1, set2):
    set1 = list(set1)
    set2 = list(set2)
    intersection = calculate_intersection(set1, set2)
    union = (len(set1) + len(set2)) - intersection
    return intersection // union 
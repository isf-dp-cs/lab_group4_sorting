# helper functions for finding group diversity

import random

def diversity_score(group):
    TRAITS = ['science1', 'science2', 'science3']
    score = 0
    # Compare every student to every other student in the group
    for i in range(len(group)):
        student_1 = group[i]
        
        # Start the second loop from the next student to avoid double-counting
        for j in range(i + 1, len(group)):
            student_2 = group[j]
            
            # Check every trait for a match
            for k in range(len(TRAITS)):
                trait_name = TRAITS[k]
                
                val_1 = getattr(student_1, trait_name)
                val_2 = getattr(student_2, trait_name)
                
                # Only compare if the values are not None or empty strings
                if val_1 and val_2:
                    if val_1 == val_2:
                        score -= 1
                        
    return score



def maybe_swap(group_1, group_2):
    """Based on Ms. Genzlinger's version with help of Gemini """
    old_sum = diversity_score(group_1) + diversity_score(group_2)
    
    for i in range(len(group_1)):
        for j in range(len(group_2)):
            # 1. Perform the swap using Python's "a, b = b, a" trick
            group_1[i], group_2[j] = group_2[j], group_1[i]
            
            new_sum = diversity_score(group_1) + diversity_score(group_2)
            
            # 2. If it improved, keep it and stop
            if new_sum > old_sum:
                return True
            
            # 3. If it DID NOT improve, swap them back exactly where they were
            group_1[i], group_2[j] = group_2[j], group_1[i]
            
    return False


def random_assignment(students, num_groups):
    random.shuffle(students)
    groups = [[] for _ in range(num_groups)]
    for i in range(len(students)):
        groups[i % num_groups].append(students[i])
    return groups

def assign_to_groups(students, num_groups):
    """Written by Ms. Genzlinger"""

    groups = random_assignment(students, num_groups)
    while True:
        has_swapped = False
        for i in range(len(groups)):
            group_1 = groups[i]
            for j in range(i + 1, len(groups)):
                group_2 = groups[j]
                if maybe_swap(group_1, group_2):
                    has_swapped = True
        if not has_swapped:
            return groups
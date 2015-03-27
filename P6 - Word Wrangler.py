
"""
Word Wrangler

"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided


WORDFILE = "assets_scrabble_words3.txt"

codeskulptor.set_timeout(40)

# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    found = []
    keep = []
    for dummy in list1:
        if dummy not in found:
            found.append(dummy)
            keep.append(dummy)
    return keep


def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """    
    matches = []
    idx1, idx2 = 0, 0
    len1, len2 = len(list1), len(list2)
    while idx1 < len1 and idx2 < len2:
        val1, val2 = list1[idx1], list2[idx2]
        if val1 < val2:
            idx1 += 1
        elif val1 > val2:
            idx2 += 1
        else:
            matches.append(val1)
            idx1 += 1
            idx2 += 1
    return matches
    
    
# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 or list2.

    This function can be iterative.
    """
    copy1, copy2 = list(list1), list(list2)
    result = list()
    while len(copy1) > 0 and len(copy2) > 0:        
        if copy1[0] <= copy2[0]:
            result.append(copy1.pop(0))            
        else:
            result.append(copy2.pop(0))            
    # len(list1) != len(list2)      
    if len(copy1) == 0:
        result.extend(copy2)
    result.extend(copy1)          
    return result

                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """  
    if len(list1) <= 1:     # base case: list with 0 or 1 element is by definition sorted
        return list1
    else:                   # recursive case: assume merge_sort will work
        left = merge_sort(list1[:len(list1)/2])
        right = merge_sort(list1[len(list1)/2:]) 
        return merge(left, right)


# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if word == '':
        return ['']
    else:
        first, rest = word[0], word[1:]
        rest_strings = gen_all_strings(rest)
        temp = list()
        for dummy_str in rest_strings:
            for dummy_idx in range(len(dummy_str)+1):
                temp.append(dummy_str[:dummy_idx] + first + 
                            dummy_str[dummy_idx:])        
        return rest_strings + temp
    

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    online_file = urllib2.urlopen(url)
    return [word[:-1] for word in online_file]


def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)


run()

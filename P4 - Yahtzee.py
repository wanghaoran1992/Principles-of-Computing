import codeskulptor
codeskulptor.set_timeout(20)


def gen_all_sequences(outcomes, length):
    '''
    iterative function that enumerates the set of all sequences of outcomes of given length;
    original code from the lecture, do not modify
    '''
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    '''
    compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card

    hand (die values in a tuple): full yahtzee hand

    returns an integer score
    '''
    # empty hand returns 0, naturally
    if not hand:
        return 0
    
    maximum_score = []
    for item in hand:
        # value is determined by its frequency and denomination
        maximum_score.append(hand.count(item) * item)
    return max(maximum_score)


def expected_value(held_dice, num_die_sides, num_free_dice):
    '''
    compute the expected value of the held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides

    held_dice (a tuple): dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    returns a floating point expected value
    '''
    
##    try:
##        assert len(held_dice) + num_free_dice == 5
##        assert num_die_sides == 6
##    except:
##        print 'Standard Yahtzee game shall use precisely five dice (each with six sides)!'

    scores = []
    die_sides = [die for die in range(1, num_die_sides + 1)]
    possible_sequence = gen_all_sequences(die_sides, num_free_dice)

    # scoring sum of held dice with each generated possibility
    for item in possible_sequence:
        scores.append(score(held_dice + item))
    
    return float(sum(scores)) / len(scores)

    
def gen_all_holds(hand):
    '''
    generate all possible choices of dice from hand to hold

    hand (a tuple): full yahtzee hand

    returns a set of tuples, where each tuple is dice to hold
    '''
    # just generate a power set from 'hand' (without following recipe with itertools)
    from_hand = [()]
    for item in hand:
        for subset in from_hand:
            from_hand = from_hand + [tuple(subset) + (item, )]
           
    return set(from_hand)
            
    
def strategy(hand, num_die_sides):
    '''
    compute the hold that maximizes the expected value when the discarded dice are rolled

    hand (a tuple): full yahtzee hand
    num_die_sides: number of sides on each die

    returns a tuple (where the first element is the expected score,
    the second element is a tuple of the dice to hold)
    '''
    result = (0.0, ())
    current_value = float('-inf')
    
    for item in gen_all_holds(hand):
        value = expected_value(item, num_die_sides, len(hand) - len(item))
        if value > current_value:
            current_value = value
            result = (current_value, item)
    
    return result


def run_example():
    '''
    compute the dice to hold and expected score for an example hand
    '''
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print 'Best strategy for hand', hand, 'is to hold', hold, 'with expected score', hand_score
    
    
run_example()
                                       
    
    
    




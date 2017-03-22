from re import sub as re_sub
from nospoil.constants import MAX_PLAYOFF_ROUNDS


def slugify(string):
    return re_sub(r'[^\w]+', '-', string.lower())


def get_match_positions(rounds, double=False):
    """
    Returns sorted list of positions for playoff.
    Rounds - number of rounds, double - if true, means double elimination.

    Position - is a string for match in playoff, whitch determines if it is:
    final (position '0-1'), first semifinal ('1-1'), second semi ('1-2'),
    first quarterfinal ('2-1'), second quarterfinal ('2-2') and so on...
    If playoff is double elimination, grand final is '0-0',
    and loosers matches are started with 'l'. Loosers final - 'l0-1'
    """
    possible_rounds = range(2, MAX_PLAYOFF_ROUNDS + 1) 
    if rounds not in possible_rounds:
        raise ValueError('Rounds should be in {}'.format(possible_rounds))
    
    result = ['0-0'] if double else []  # '0-0' is grand final
    for rnd in range(rounds):  # loop for winners matches
        template = '{}-{}' if rnd < 4 else '{}-{:02}'
        result.extend(template.format(rnd, i) for i in range(1, 2**rnd+1))
    if double:  # loop for loosers matches
        lr = 0
        for rnd in range(rounds-1):
            result.extend('l{}-{}'.format(lr, i) for i in range(1, 2**rnd+1))
            result.extend('l{}-{}'.format(lr+1, i) for i in range(1, 2**rnd+1))
            lr += 2
    # note: result is already sorted
    return result


def get_grid(matches, rounds_number, double):
    """
    Grid is playoff matches grouped by semi/quarter/one-eights for nice output.
    Matches could be just list of position strings or some objects,
    but they should be sorted same as in get_match_positions function,
    (and should not be a queryset object, because a lot of slicing here)
    result should be like this: 
    {
      'winners': [
        ...
        [first quarterfinal, second quarter, 3rd, 4th]
        [first semifinal, second semifinal]
        [final match],
      ],
      'loosers': [...],  // same as winners if playoff is double eliminated
      'final': grand final match  // if double
    }

    """
    result = {'final': matches[0]} if double else {}
    i = 1 if double else 0
    rounds = []
    for rnd in range(rounds_number):  # matches are sorted, winners (0-1, 1-1)
        j = i + 2 ** rnd              # goes rigth after grand final (0-0)
        rounds.append(matches[i:j])
        i = j;
    result['winners'] = rounds[::-1]  # reversed - final is last
    if not double:
        return result

    rounds, total_looser_rounds = [], 2*(rounds_number-1)
    for rnd in range(total_looser_rounds):  # same for loosers
        j = i + 2 ** (rnd//2)
        rounds.append(matches[i:j])
        i = j;
    result['loosers'] = rounds[::-1]
    return result

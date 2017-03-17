from re import sub as re_sub
from nospoil.constants import MAX_PLAYOFF_ROUNDS


def slugify(string):
    return re_sub(r'[^\w]+', '-', string.lower())


def get_match_positions(rounds, double=False):
    possible_rounds = range(2, MAX_PLAYOFF_ROUNDS + 1) 
    if rounds not in possible_rounds:
        raise ValueError('Rounds should be in {}'.format(possible_rounds))
    
    result = ['0-0'] if double else []  # '0-0' is grand final
    for rnd in range(rounds):  # '0-1' - final; '1-1', '1-2' - semifinals ...
        template = '{}-{}' if rnd < 4 else '{}-{:02}'
        result.extend(template.format(rnd, i) for i in range(1, 2**rnd+1))
    if double:  # 'l0-1' - loosers final ...
        lr = 0
        for rnd in range(rounds-1):
            result.extend('l{}-{}'.format(lr, i) for i in range(1, 2**rnd+1))
            result.extend('l{}-{}'.format(lr+1, i) for i in range(1, 2**rnd+1))
            lr += 2
    return result



def get_playoff_grid(playoff):
    values = ('position', 'side_a', 'side_b', 'winner_a', 'youtube_id')
    matches = list(playoff.matches.order_by('position').values(*values))
    return _get_grid(matches, playoff.rounds, playoff.double)


def get_empty_grid():
    rounds, double = MAX_PLAYOFF_ROUNDS, True
    positions = get_match_positions(rounds, double)
    empty = {'side_a': '', 'side_b': '', 'winner_a': None, 'youtube_id': ''}
    matches = [dict(position=p, **empty) for p in positions]
    return _get_grid(matches, rounds, double)


def _get_grid(matches, rounds_number, double):
    result = {'final': matches[0]} if double else {}
    i = 1 if double else 0
    rounds = []
    for rnd in range(rounds_number):
        j = i + 2 ** rnd
        rounds.append(matches[i:j])
        i = j;
    result['winners'] = rounds[::-1]
    if not double:
        return result

    rounds, total_looser_rounds = [], 2*(rounds_number-1)
    for rnd in range(total_looser_rounds):
        j = i + 2 ** (rnd//2)
        rounds.append(matches[i:j])
        i = j;
    result['loosers'] = rounds[::-1]
    return result

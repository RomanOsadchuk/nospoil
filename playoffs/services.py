from django.db.models import F
from bulk_update.helper import bulk_update
from nospoil.constants import MAX_PLAYOFF_ROUNDS, HEADER_DROPDOWN_SIZE
from .models import Playoff, Match


def inc_playoff_views(playoff):
    Playoff.objects.filter(pk=playoff.pk).update(views=F('views')+1)


def update_last_viewed(session, new_playoff):
    _update_session('last_viewed', session, new_playoff)


def update_last_edited(session, new_playoff):
    _update_session('last_edited', session, new_playoff)


def _update_session(key, session, new_playoff):
    old_list = session.get(key, [])
    for i, item in enumerate(old_list):
        if item['pk'] == new_playoff.pk:
            new_list = [old_list[i]] + old_list[:i] + old_list[i+1:]
            session[key] = new_list
            return
    new_item = {'pk': new_playoff.pk,
                'title': new_playoff.title,
                'slug': new_playoff.slug}
    new_list = [new_item] + old_list[:HEADER_DROPDOWN_SIZE-1]
    session[key] = new_list


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
    matches = list(Match.objects.filter(playoff=playoff).order_by('position'))
    return _get_grid(matches, playoff.rounds, playoff.double)


def get_edit_grid(post_data, playoff=None):
    if playoff:  # update view case
        rounds, double = playoff.rounds, playoff.double
    else:        # create view case
        rounds, double = MAX_PLAYOFF_ROUNDS, True
    positions = get_match_positions(rounds, double)
    matches = [Match(position=p) for p in positions]
    _attach_data_to_matches(matches, post_data)
    return _get_grid(matches, rounds, double)


def save_matches(post_data, playoff):
    positions = get_match_positions(playoff.rounds, playoff.double)
    matches = [Match(position=p, playoff=playoff) for p in positions]
    _attach_data_to_matches(matches, post_data)
    Match.objects.bulk_create(matches)


def update_matches(post_data, playoff):
    matches = list(Match.objects.filter(playoff=playoff).order_by('position'))
    _attach_data_to_matches(matches, post_data)
    fields = ['side_a', 'side_b', 'winner_a', 'youtube_id']
    bulk_update(matches, update_fields=fields)


def _attach_data_to_matches(matches, post_data):
    winner_a_dict = {'True': True, 'False': False}
    for match in matches:
        pos = match.position
        winner_a_key = post_data.get('winner-a-' + pos)
        match.winner_a = winner_a_dict.get(winner_a_key)
        match.side_a = post_data.get('side-a-' + pos, '')[:32]
        match.side_b = post_data.get('side-b-' + pos, '')[:32]
        match.youtube_id = post_data.get('youtube-id-' + pos, '')[:32]


def create_matches_2(playoff, matches_data):
    positions = get_match_positions(playoff.rounds, playoff.double)
    matches = [Match(position=p, playoff=playoff) for p in positions]
    _attach_data_to_matches_2(matches, matches_data)
    Match.objects.bulk_create(matches)


def update_matches_2(playoff, matches_data):
    matches = list(playoff.matches.order_by('position'))
    _attach_data_to_matches_2(matches, matches_data)
    fields = ['side_a', 'side_b', 'winner_a', 'youtube_id']
    bulk_update(matches, update_fields=fields)


def _attach_data_to_matches_2(matches, matches_data):
    if not isinstance(matches_data, dict):
        return
    for match in matches:
        data_bit = matches_data.get(match.position, {})
        match.side_a = data_bit.get('sideA', '')[:32]
        match.side_b = data_bit.get('sideB', '')[:32]
        match.winner_a = data_bit.get('winnerA')
        match.youtube_id = data_bit.get('youtubeId-', '')[:32]


LONG_NAMES = ['Final', 'SemiFinals', 'QuarterFinals']
SHORT_NAMES = ['F', 'SF', 'QF']

def _get_grid(matches, rounds_number, double):
    result = {'grand_final': matches[0]} if double else {}
    i = 1 if double else 0
    rounds = []
    for rnd in range(rounds_number):
        j = i + 2 ** rnd
        idx = rounds_number - rnd
        rounds.append({
            'one_based_idx': idx,
            'short_name': SHORT_NAMES[rnd] if rnd<3 else str(idx),
            'long_name': LONG_NAMES[rnd] if rnd<3 else 'Round {}'.format(idx),
            'matches': matches[i:j],
        })
        i = j;
    result['winners'] = rounds[::-1]
    if not double:
        return result

    rounds, total_looser_rounds = [], 2*(rounds_number-1)
    for rnd in range(total_looser_rounds):
        j = i + 2 ** (rnd//2)
        idx = total_looser_rounds - rnd
        rounds.append({
            'one_based_idx': idx,
            'short_name': SHORT_NAMES[rnd] if rnd<1 else str(idx),
            'long_name': LONG_NAMES[rnd] if rnd<1 else 'Round {}'.format(idx),
            'matches': matches[i:j],
        })
        i = j;
    result['loosers'] = rounds[::-1]
    return result

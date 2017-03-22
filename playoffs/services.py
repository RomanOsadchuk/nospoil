from django.db.models import F
from bulk_update.helper import bulk_update
from nospoil.constants import HEADER_DROPDOWN_SIZE, MAX_PLAYOFF_ROUNDS

from .helpers import get_grid, get_match_positions
from .models import Playoff, Match


def get_empty_grid():
    rounds, double = MAX_PLAYOFF_ROUNDS, True
    positions = get_match_positions(rounds, double)
    empty = {'side_a': '', 'side_b': '', 'winner_a': None, 'youtube_id': ''}
    matches = [dict(position=p, **empty) for p in positions]
    return get_grid(matches, rounds, double)


# ==== match services ==== #

def create_matches(playoff, matches_data):
    """Creating all matches for playoff depending on rounds number and elim.
    And attaching data which is provided"""
    positions = get_match_positions(playoff.rounds, playoff.double)
    matches = [Match(position=p, playoff=playoff) for p in positions]
    _attach_data_to_matches(matches, matches_data)
    Match.objects.bulk_create(matches)


def update_matches(playoff, matches_data):
    matches = list(playoff.matches.order_by('position'))
    _attach_data_to_matches(matches, matches_data)
    fields = ['side_a', 'side_b', 'winner_a', 'youtube_id']
    bulk_update(matches, update_fields=fields)


def _attach_data_to_matches(matches, matches_data):
    """Safe attaching should not rise anything"""
    if not isinstance(matches_data, dict):
        return
    safe_null_bool = lambda x: x is True or (False if x is False else None)
    for match in matches:
        data_bit = matches_data.get(match.position, {})
        if data_bit and isinstance(data_bit, dict):
            match.side_a = unicode(data_bit.get('side_a', ''))[:32]
            match.side_b = unicode(data_bit.get('side_b', ''))[:32]
            match.winner_a = safe_null_bool(data_bit.get('winner_a'))
            match.youtube_id = unicode(data_bit.get('youtube_id', ''))[:32]


# ==== template views services ==== #


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

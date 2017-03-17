from django.db.models import F
from bulk_update.helper import bulk_update
from nospoil.constants import HEADER_DROPDOWN_SIZE
from .helpers import get_match_positions
from .models import Playoff, Match


def inc_playoff_views(playoff):
    Playoff.objects.filter(pk=playoff.pk).update(views=F('views')+1)


# ==== match services ==== #

def create_matches(playoff, matches_data):
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
    make_null_bool = lambda x: {True: True, False: False}.get(x)
    if not isinstance(matches_data, dict):
        return
    for match in matches:
        data_bit = matches_data.get(match.position, {})
        if data_bit and isinstance(data_bit, dict):
            match.side_a = str(data_bit.get('side_a', ''))[:32]
            match.side_b = str(data_bit.get('side_b', ''))[:32]
            match.winner_a = make_null_bool(data_bit.get('winner_a'))
            match.youtube_id = str(data_bit.get('youtube_id', ''))[:32]


# ==== 

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


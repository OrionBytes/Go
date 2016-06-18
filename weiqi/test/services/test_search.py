# weiqi.gs
# Copyright (C) 2016 Michael Bitzi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from weiqi.services import SearchService
from weiqi.test.factories import UserFactory, GameFactory


def test_no_results(db, socket):
    svc = SearchService(db, socket)
    data = svc.execute('all', {'query': 'test'})

    users = data.get('users')
    assert users.get('page') == 1
    assert users.get('total_pages') == 1
    assert users.get('total_results') == 0

    games = data.get('users')
    assert games.get('page') == 1
    assert games.get('total_pages') == 1
    assert games.get('total_results') == 0


def test_users_display_name(db, socket):
    user = UserFactory(display='TestUser')
    other = UserFactory(display='ATestUser2')
    UserFactory(display='SomeoneElse')

    svc = SearchService(db, socket)
    data = svc.execute('users', {'query': 'testuser'})

    assert data.get('page') == 1
    assert data.get('total_pages') == 1
    assert data.get('total_results') == 2

    assert len(data['results']) == 2
    assert data['results'][0]['id'] == other.id
    assert data['results'][0]['display'] == other.display
    assert data['results'][1]['id'] == user.id
    assert data['results'][1]['display'] == user.display


def test_new_users(db, socket):
    user = UserFactory(display='test', last_activity_at=None)

    svc = SearchService(db, socket)
    data = svc.execute('users', {'query': 'test'})

    assert len(data['results']) == 1
    assert data['results'][0]['id'] == user.id


def test_games_display_names(db, socket):
    black = GameFactory(black_display='TestUser')
    white = GameFactory(white_display='ATestUser2')
    demo = GameFactory(demo_owner_display='BTestUser3')
    GameFactory(black_display='nomatch', white_display='nomatch', demo_owner_display='nomatch')

    svc = SearchService(db, socket)
    data = svc.execute('games', {'query': 'testuser'})

    assert data.get('page') == 1
    assert data.get('total_pages') == 1
    assert data.get('total_results') == 3

    assert len(data['results']) == 3
    assert data['results'][0]['id'] == demo.id
    assert data['results'][1]['id'] == white.id
    assert data['results'][2]['id'] == black.id

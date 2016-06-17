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

from weiqi.models import User, Game
from weiqi.services import BaseService


class UserService(BaseService):
    __service_name__ = 'users'

    def publish_status(self):
        if not self.user:
            return

        self.socket.publish('user_status', {
            'id': self.user.id,
            'rating': self.user.rating,
            'is_online': self.user.is_online,
            'wins': Game.count_wins(self.db, self.user)
        })

    @BaseService.register
    def email_exists(self, email):
        return self.db.query(User).filter_by(email=email).count() > 0

    @BaseService.register
    def profile(self, user_id):
        user = self.db.query(User).get(user_id)
        if not user:
            return {}

        return {
            'id': user_id,
            'created_at': user.created_at.isoformat(),
            'last_activity_at': user.last_activity_at.isoformat() if user.last_activity_at else None,
            'is_online': user.is_online,
            'rating': user.rating,
            'display': user.display,
            'info_text_html': user.info_text_html,
        }

    @BaseService.register
    def games(self, user_id):
        user = self.db.query(User).get(user_id)
        if not user:
            return []

        return [g.to_frontend() for g in user.games(self.db)]

    @BaseService.register
    def autocomplete(self, query):
        users = self.db.query(User).filter(User.display.ilike('%%{}%%'.format(query)))
        return [u.to_frontend() for u in users]

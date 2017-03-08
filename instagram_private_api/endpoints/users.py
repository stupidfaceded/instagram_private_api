import warnings

from ..compatpatch import ClientCompatPatch


class UsersEndpointsMixin(object):

    def user_info(self, user_id):
        """
        Get user info for a specified user id

        :param user_id:
        :return:
        """
        res = self._call_api('users/%(user_id)s/info/' % {'user_id': user_id})
        if self.auto_patch:
            ClientCompatPatch.user(res['user'], drop_incompat_keys=self.drop_incompat_keys)
        return res

    def username_info(self, user_name):
        """
        Get user info for a specified user name
        :param user_name:
        :return:
        """
        res = self._call_api('users/%(user_name)s/usernameinfo/' % {'user_name': user_name})
        if self.auto_patch:
            ClientCompatPatch.user(res['user'], drop_incompat_keys=self.drop_incompat_keys)
        return res

    def user_detail_info(self, user_id, **kwargs):
        """
        EXPERIMENTAL ENDPOINT, INADVISABLE TO USE.
        Get user detailed info

        :param user_id:
        :param kwargs:
            - **max_id**: For pagination
            - **min_timestamp**: For pagination
        :return:
        """
        warnings.warn('This endpoint is experimental. Do not use.', UserWarning)

        endpoint = 'users/%(user_id)s/full_detail_info/' % {'user_id': user_id}
        res = self._call_api(endpoint, query=kwargs)
        if self.auto_patch:
            ClientCompatPatch.user(res['user_detail']['user'], drop_incompat_keys=self.drop_incompat_keys)
            [ClientCompatPatch.media(m, drop_incompat_keys=self.drop_incompat_keys)
             for m in res.get('feed', {}).get('items', [])]
            [ClientCompatPatch.media(m, drop_incompat_keys=self.drop_incompat_keys)
             for m in res.get('reel_feed', {}).get('items', [])]
            [ClientCompatPatch.media(m, drop_incompat_keys=self.drop_incompat_keys)
             for m in res.get('user_story', {}).get('reel', {}).get('items', [])]
        return res

    def user_map(self, user_id):
        """
        Get a list of geo-tagged media from a user

        :param user_id: User id
        :return:
        """
        endpoint = 'maps/user/%(user_id)s/' % {'user_id': user_id}
        return self._call_api(endpoint)

    def search_users(self, query, **kwargs):
        """
        Search users

        :param query: Search string
        :param kwargs:
            - **max_id**: For pagination
        :return:
        """
        query_params = {
            'rank_token': self.rank_token,
            'ig_sig_key_version': self.key_version,
            'is_typeahead': 'true',
            'query': query
        }
        if kwargs:
            query_params.update(kwargs)
        res = self._call_api('users/search/', query=query_params)
        if self.auto_patch:
            [ClientCompatPatch.list_user(u, drop_incompat_keys=self.drop_incompat_keys)
             for u in res.get('users', [])]
        return res

import time
from typing import Optional
from vk_api import VkApi
from vk_api.vk_api import VkApiMethod
from loggers import community_parser_logger
from main_api.loggers import community_parser_logger

from vkbottle import API


class AsyncCommunityParser:

    def __init__(self, vk_api: API) -> None:
        self.vk_api = vk_api

    async def get_all_community_participants(
        self, 
        community_screenname: str, 
        fields: list[str],
        filter_by_can_add_to_friend: bool = True
    ) -> Optional[list[dict]]:
        community_parser_logger.info(
            f'starting get all members of "{community_screenname}"'
        )
        try:
            is_in_group_now: int = await self.vk_api.groups.get_members(group_id=community_screenname)
            is_in_group_now = is_in_group_now.count
        except Exception:
            is_in_group_now = 'UNKNOWN'

        _all: list[dict] = []
        offset = 0
        try:
            while True:
                offsetted_members = await self.get_thousand_with_offset(
                    community_screenname=community_screenname,
                    offset=offset,
                    fields=fields,
                    filter_by_can_add_to_friend=filter_by_can_add_to_friend
                )
                if not offsetted_members:
                    break
                _all.extend(offsetted_members)
                offset+=1000
                community_parser_logger.info(
                    f'{community_screenname} parsing: '
                    f'passed {offset}/{is_in_group_now}, '
                    f'{len(offsetted_members) if offsetted_members else 0} added in common list'
                )
                time.sleep(1)
        except Exception as e:
            community_parser_logger.error(
                f'Error in getting all users from community(group)="{community_screenname}" '
                f'on offset={offset}. '
                f'The funtions return all that received at the moment...'
                f'({type(e)}: {str(e)})'
            )
        return _all

    async def get_thousand_with_offset(
            self,
            community_screenname: str,
            offset: int,
            fields: list[str],
            filter_by_can_add_to_friend: bool = True
        ) -> list[dict]:

        if not fields:
            fields = ['screen_name']

        community_parser_logger.info(
            f'start parsing community members of {community_screenname} '
            f'with offset >>> {offset}'
        )

        res = await self.vk_api.groups.get_members(
            group_id=community_screenname,
            offset=offset,
            fields=fields
        )
        res = res.items

        items_to_return = []
        for item in res:
            item_dict = item.dict() 
            filtered_dict = {key: value for key, value in item_dict.items() if value is not None}
            items_to_return.append(filtered_dict)

        if filter_by_can_add_to_friend:
            filtered = []
            for item in items_to_return:
                if 'can_send_friend_request' in item.keys():
                    if item['can_send_friend_request']:
                        filtered.append(item)
            community_parser_logger.info(
                f'{community_screenname} getting offset, received and filtered '
                f'by posibility of adding to friend >>> {len(res)} clients'
            )
            return filtered

        community_parser_logger.info(
            f'{community_screenname} getting offset, received >>> {len(res)} clients'
        )

        return items_to_return







class CommunityParser:

    def __init__(self, vk_api: VkApiMethod) -> None:
        self.vk_api = vk_api

    def get_all_community_participants(
        self, 
        community_screenname: str, 
        fields: list[str],
        filter_by_can_add_to_friend: bool = True
    ) -> Optional[list[dict]]:
        community_parser_logger.info(
            f'starting get all members of "{community_screenname}"'
        )
        try:
            is_in_group_now: int = self.vk_api.groups.getMembers(group_id=community_screenname).get('count')
        except Exception:
            is_in_group_now = 'UNKNOWN'

        _all: list[dict] = []
        offset = 0
        try:
            while True:
                offsetted_members = self.get_thousand_with_offset(
                    community_screenname=community_screenname,
                    offset=offset,
                    fields=fields,
                    filter_by_can_add_to_friend=filter_by_can_add_to_friend
                )
                if not offsetted_members:
                    break
                _all.extend(offsetted_members)
                offset+=1000
                community_parser_logger.info(
                    f'{community_screenname} parsing: '
                    f'passed {offset}/{is_in_group_now}, '
                    f'{len(offsetted_members) if offsetted_members else 0} added in common list'
                )
                time.sleep(1)
        except Exception as e:
            community_parser_logger.error(
                f'Error in getting all users from community(group)="{community_screenname}" '
                f'on offset={offset}. '
                f'The funtions return all that received at the moment...'
                f'({type(e)}: {str(e)})'
            )
        return _all

    def get_thousand_with_offset(
            self,
            community_screenname: str,
            offset: int,
            fields: list[str],
            filter_by_can_add_to_friend: bool = True
        ) -> list[dict]:
        '''
        returns list of dict items, which contain data about users: id, screen_name, first_name, can_access_closed, is_closed.
        If offset is too big (more than number of participants), it returns empty list []
        '''
        if not fields:
            fields = ['screen_name']

        community_parser_logger.info(
            f'start parsing community members of {community_screenname} '
            f'with offset >>> {offset}'
        )

        res = self.vk_api.groups.getMembers(
            group_id=community_screenname,
            offset=offset,
            fields=fields
        ).get('items')

        if filter_by_can_add_to_friend:
            filtered = []
            for item in res:
                if 'can_send_friend_request' in item.keys():
                    if item['can_send_friend_request']:
                        filtered.append(item)
            community_parser_logger.info(
                f'{community_screenname} getting offset, received and filtered '
                f'by posibility of adding to friend >>> {len(res)} clients'
            )
            return filtered

        community_parser_logger.info(
            f'{community_screenname} getting offset, received >>> {len(res)} clients'
        )

        return res
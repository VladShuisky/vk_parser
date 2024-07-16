import json
import time
import traceback
from vk_api import VkApi
from vk_api.exceptions import ApiError

from main_api.service.vk_parsing.community_parser import CommunityParser
from old_friendly_users_getter import SearchFriendlyUSers
from main_api.service.export.saver_for_promo import SaverForPromoCsvImport
from settings import DEFAULT_FIELDS_TO_NEED, TOKEN
from loggers import script_parsing_logger

api = VkApi(token=TOKEN).get_api()

group_names = [
 'tyt_novosti',
 'leprazo',
 'vkgames',
 'bak',
 'smechno_do_boli',
 'overhear',
 'ulibnullo',
 'megaotriv',
 'great.food',
 'science_technology',
 'comedyclubru',
 'zerofat',
 'hmideas',
 'cocacola',
 'foodrumedia',
 'zloyzayacgif'
 ]

for group_name in group_names:
    try:
        while True:
            try:
                data = CommunityParser(
                    vk_api=api
                    ).get_thousand_with_offset(
                        group_name,
                        offset=0, fields=DEFAULT_FIELDS_TO_NEED
                    )
                script_parsing_logger.info(
                    f'community_data for {group_name} received'
                )
                break
            except Exception as e:
                if isinstance(e, ApiError):
                    if e.code == 15: # hidden members of community
                        data = 'raise exc'
                    break

                else:
                    script_parsing_logger.error(f'errror >>> {type(e)} : {str(e)}')
                    traceback.print_exc()
                    script_parsing_logger.info('sleeping 300 seconds')
                    time.sleep(300)

        if data == 'raise exc':
            continue

        try:
            script_parsing_logger.info(f'{group_name}: try to filter by SearchFriendlyUsers class')
            thousanders_filtering_ids: list[int] = SearchFriendlyUSers(api, 1000, [x['id'] for x in data], 100).start()
            ids_as_list = list(thousanders_filtering_ids.queue)
            script_parsing_logger.info(f'{group_name}: {len(ids_as_list)} id"s filtered!')
        except Exception as e:
            script_parsing_logger.error('smth goes wrong in script in filtering by friendly users, saving data in json')
            traceback.print_exc()

            with open(f'{group_name}_backup.json', 'w') as jsonfile:
                json.dump(data, jsonfile, ensure_ascii=False)
            continue

        filtered_data = [item for item in data if item['id'] in ids_as_list]
        script_parsing_logger.info(f'{group_name}: data filtered! now {len(filtered_data)} in items list!')
        if filtered_data:
            try:
                saver = SaverForPromoCsvImport()
                saver.save_to_csv(filtered_data, group_name, ',')
            except Exception as e:
                script_parsing_logger.error(f'smth goes wrong with csv saving: {type(e)}: {str(e)}')
    except Exception as e:
        script_parsing_logger.error(f'BIG ERROR {type(e)}: {str(e)}')
        continue
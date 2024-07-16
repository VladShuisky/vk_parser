import json
import traceback
from vk_api import VkApi

from main_api.service.vk_parsing.community_parser import CommunityParser
from old_friendly_users_getter import SearchFriendlyUSers
from main_api.service.export.saver_for_promo import SaverForPromoCsvImport
from settings import DEFAULT_FIELDS_TO_NEED, TOKEN

api = VkApi(token=TOKEN).get_api()

group_names = ['kinomania', 'smeyaka', 'fuck_humor', 'ifun']

for group_name in group_names:
    data = CommunityParser(
        vk_api=api
        ).get_thousand_with_offset(
            group_name, 
            offset=0, fields=DEFAULT_FIELDS_TO_NEED
        )

    try:
        thousanders_filtering_ids: list[int] = SearchFriendlyUSers(api, 1000, [x['id'] for x in data], 100).start()
        ids_as_list = list(thousanders_filtering_ids.queue)
    except Exception as e:
        print('smth goes wrong in script in filtering by friendly users, saving data in json')
        traceback.print_exc()

        with open(f'{group_name}_backup.json', 'w') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False)
        continue


    filtered_data = [item for item in data if item['id'] in ids_as_list]
    if filtered_data:
        try:
            saver = SaverForPromoCsvImport()
            saver.save_to_csv(filtered_data, group_name, ',')
        except Exception as e:
            print(f'smth goes wrong with csv saving: {type(e)}: {str(e)}')
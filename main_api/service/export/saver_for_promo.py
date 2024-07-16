import csv
from ctypes.wintypes import tagSIZE
from io import StringIO
import json
from loggers import csv_file_write_logger as logger

class SaverForPromoCsvImport:

    def __init__(self) -> None:
        pass

    def make_a_row_for_csv_writing(
            self, 
            item: dict,
        ) -> list:
        row = []
        row.append(item.get('id')) #0
        row.append('https://vk.com/' + item.get('screen_name')) #1
        row.append('3') #3
        row.append('для_количества') #4
        row.append('ДЛЯ_КОЛИЧЕСТВА') #5

        json_dict: str = json.dumps(item, ensure_ascii=False)
        row.append(json_dict)

        return row

    def save_to_csv(
            self, 
            items_to_save: list[dict],
            new_file_name: str,
            separator: str = ','
        ):
        '''saves csv file in current catalogue'''
        logger.info(f'start save csv file "{new_file_name}.csv"')
        with open(f'{new_file_name}.csv', 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=separator)


            logger.info(f'{new_file_name}.csv -> add header with column names to file')
            self.add_header_with_column_names(writer)
            logger.info(f'{new_file_name}.csv header with column names >>> created')

            for item in items_to_save:
                prepared_row = self.make_a_row_for_csv_writing(item=item)
                writer.writerow(prepared_row)
            logger.info(f'{new_file_name}.csv >>> rows created!')


    def add_header_with_column_names(self, csvfilewriter):
        csvfilewriter.writerow(
            ['vk_id','vk_profile_url','friending_priority','tags','comment','json_data_dict']
        )

class StringIOSaverForPromoCsv(SaverForPromoCsvImport):

    def make_a_item_dict_for_csv_writing(self, item: dict, tags: list, comment: str):
        formatted_item: dict = {}
        formatted_item['vk_id'] = item['id']
        formatted_item['vk_profile_url'] = 'https://vk.com/' + item.get('screen_name')
        formatted_item['tags'] = ','.join(tags) if isinstance(tags, list) else tags
        formatted_item['comment'] = comment
        formatted_item['json_data_dict'] = json.dumps(item, ensure_ascii=False)
        
        return formatted_item

    def save_to_csv(self, items_to_save: list[dict], tags, comment, separator: str = ','):
        output = StringIO()

        data: list[dict] = [
            self.make_a_item_dict_for_csv_writing(item, tags=tags, comment=comment) for item in items_to_save
        ]

        csv_writer = csv.DictWriter(
            output, 
            fieldnames=['vk_id', 'vk_profile_url', 'tags', 'comment', 'json_data_dict'],
            delimiter=separator
        )
        csv_writer.writeheader()
        csv_writer.writerows(data)

        return output.getvalue()

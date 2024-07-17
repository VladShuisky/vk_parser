from typing import List, Optional

from fastapi import HTTPException
from sqlmodel import and_, select
from vk_api import VkApi
from vkbottle import API

from main_api.parsingsources.models.parsingresourceapicredentials import ParsingAccountApiCredentials
from main_api.parsingtasks.crud import task_crud, taskprops_crud, taskresults_crud
from main_api.parsingtasks.models.task import Task
from main_api.parsingtasks.models.taskprops import TaskProps
from main_api.parsingtasks.models.taskresults import TaskResults
from main_api.service.vk_parsing.async_community_parser import AsyncCommunityParser
from main_api.loggers import get_groups_users_logger as logger

async def get_groups_users(
        db,
        parsing_task_name: str,
        groups_screennames: List[str],
        fields: List[str]
):
    '''
    single vk parsing via 1 api account, sync parsing groups one by one
    :param parsing_task_name str - unique name of parsing task, try to come up with a memorable task name
    :param group_screennames - list of screennames, which need to parse (https://vk.com/vkgroup, "vkgroup" is screenname)
    :param fields str - list of fields, which need to get from vk api about vk accounts, more details "https://dev.vk.com/ru/reference/objects/user"
    '''
    logger.info('start vk parsing task!')
    logger.info('creating task...')

    task: Task = await task_crud.create(
        db, obj_in={
            'unique_name': parsing_task_name,
            'start_datetime': None,
            'finish_datetime': None
        }
    )
    task_id = task.id

    logger.info(f'task id >>> {task_id}')

    task_props: TaskProps = await taskprops_crud.create(db, obj_in={'task_id': task_id})

    task_props.body = {
        'parsing_task_name': parsing_task_name,
        'group_screennames': groups_screennames,
        'fields': fields
    }

    task_results: TaskResults = await taskresults_crud.create(db, obj_in={'task_id': task_id})

    stmt = select(
        ParsingAccountApiCredentials).where(
            and_(
                ParsingAccountApiCredentials.active == True,
                ParsingAccountApiCredentials.engaged == False
            )
        )

    creds_item_res = await db.execute(stmt)
    creds_item = creds_item_res.scalars().first()

    logger.info(creds_item)

    access_token = creds_item.access_token

    if not creds_item:
        raise HTTPException(404, detail='no free vk account!')

    logger.info(f'task with id {task_id}: account for api received from api >>> {creds_item}')
    
    creds_item.engaged = True
    db.add(creds_item)
    db.add(task_props)
    await db.commit()

    logger.info(f'task with id >> {task_id}: account engaged, task_props updated, and saved in db')

    # vkapi = VkApi(token=access_token).get_api()
    vkapi = API(token=access_token)

    logger.info(f'task with id >> {task_id}, api received')

    result = {
        'result': [],
        'succesfull_groups': [],
        'error_groups': [],
        'groups_with_empty_results': [],
        'errors': [] 
    }

    logger.info(f'task id >> {task_id}: start parsing...')

    for group_name in groups_screennames:
        parser = AsyncCommunityParser(vk_api=vkapi)
        try:
            group_res = await parser.get_all_community_participants(
                community_screenname=group_name,
                fields=fields,
                filter_by_can_add_to_friend=False
            )
            if group_res:
                group_res_ids = [item['id'] for item in result['result']]
                for item in group_res:
                    if item['id'] not in group_res_ids:
                        result['result'].append(item)
                result['succesfull_groups'].append(group_name)
            else:
                result['groups_with_empty_results'].append(group_name)
        except Exception as e:
            result['error_groups'].append(group_name)
            result['errors'].append(
                f'{group_name}: {type(e)}: {str(e)}'
            )

    task_results.body = result

    creds_item.engaged = False

    db.add(task_results)
    db.add(creds_item)

    await db.commit()

    logger.info(f'task_id >> {task_id}: task results and creds item updated and saved in db...')

    logger.info(
        f'parsing task with id={task_id} ended!'
    )





import json
from vk_api import VkApi
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from vkbottle import API
from main_api.service.vk_parsing.community_parser import CommunityParser
from main_api.service.vk_parsing.get_groups_users import get_groups_users
from main_api.service.export.saver_for_promo import SaverForPromoCsvImport
from old_friendly_users_getter import SearchFriendlyUSers
from main_api.parsingsources.models import ParsingAccountApiCredentials, ParsingResourceApi
from main_api.parsingtasks.models import Task, TaskProps, TaskResults
from main_api.db.db import AsyncSession, engine
from sqlmodel import select

from main_api.parsingtasks.crud import task_crud, taskresults_crud, taskprops_crud


async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

myvkapi = VkApi(token='vk1.a.oBd8lC3Zc0JYDxrgZOKEiKmnu5LeuDGu6MrO_JSmvu9w5mmkTsSophfP4kiScKzuXIMHIZziZwAnn2LoYaXK6iWDESW-ZsgWnLRaFktapvYzNJlnMpZzKffIppAPlSZFvmuH0H2xukRZxw7rU0hkRkVZDCOXD8vIUAfuqSMRQvc1qI9OiGqpUOXdWWMchtDQBhPX8z2OXisKg57PhNq7Jw').get_api()

myvkbottleapi = API(token='vk1.a.oBd8lC3Zc0JYDxrgZOKEiKmnu5LeuDGu6MrO_JSmvu9w5mmkTsSophfP4kiScKzuXIMHIZziZwAnn2LoYaXK6iWDESW-ZsgWnLRaFktapvYzNJlnMpZzKffIppAPlSZFvmuH0H2xukRZxw7rU0hkRkVZDCOXD8vIUAfuqSMRQvc1qI9OiGqpUOXdWWMchtDQBhPX8z2OXisKg57PhNq7Jw')
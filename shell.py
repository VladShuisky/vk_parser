
import json
from vk_api import VkApi
from community_parser import CommunityParser
from saver_for_promo import SaverForPromoCsvImport
from old_friendly_users_getter import SearchFriendlyUSers

myvkapi = VkApi(token='vk1.a.oBd8lC3Zc0JYDxrgZOKEiKmnu5LeuDGu6MrO_JSmvu9w5mmkTsSophfP4kiScKzuXIMHIZziZwAnn2LoYaXK6iWDESW-ZsgWnLRaFktapvYzNJlnMpZzKffIppAPlSZFvmuH0H2xukRZxw7rU0hkRkVZDCOXD8vIUAfuqSMRQvc1qI9OiGqpUOXdWWMchtDQBhPX8z2OXisKg57PhNq7Jw').get_api()
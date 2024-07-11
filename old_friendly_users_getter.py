from queue import Queue
import threading
from vk_api.vk_api import VkApiMethod
from vk_api import VkApiError
from threading import Thread

class SearchFriendlyUSers:
    def __init__(self, account_api, min_friends_need: int = 0, users_list: list = [], threads_number: int = 1) -> None:
        self.api: VkApiMethod = account_api
        self.min_friends_need = min_friends_need
        self.users_list = users_list
        self.threads_number = threads_number
        self.threads_queue = Queue()

    def get_users_friends(self, user_id: int):
        all = []
        offset = 0
        while True:
            try:
                current_users = self.api.friends.get(user_id=user_id, offset=offset).get('items')
                all = [*all, *current_users]
                if len(all) != 5000:
                    return all
                offset += 5000
            except VkApiError as e:
                all.append({'error': f'{str(e)}:{type(e)}'})
            finally:
                return all

    def get_thread_for_resolving(self, users_list: list):
        return Thread(target=self.resolve_user_slice, kwargs={'users_list': users_list})

    def resolve_user_slice(self, users_list: list = None) -> list:
        thread_name = threading.currentThread().getName()
        users_list = users_list if users_list else self.users_list
        for user_id in users_list:
            print(f'{thread_name}: resolving {user_id}')
            resolving: tuple = self.resolve_users_friends(user_id), user_id
            if isinstance(resolving[0], int) and resolving[0]>self.min_friends_need:
                self.threads_queue.put(resolving[1])

    def разделить_список(self, исходный_список, размер_подсписка):
        разделенные_списки = []
        for i in range(0, len(исходный_список), размер_подсписка):
            подсписок = исходный_список[i:i+размер_подсписка]
            разделенные_списки.append(подсписок)
        return разделенные_списки

    def start_threads_resolving(self):
        user_slice_size = self.threads_number
        user_slices = self.разделить_список(размер_подсписка=user_slice_size, исходный_список=self.users_list)
        print(len(user_slices))
        resolve_threads: list[Thread] = []
        try:
            for user_slice in user_slices:
                resolve_threads.append(self.get_thread_for_resolving(user_slice))
            for thread in resolve_threads:
                thread.start()

            for thread in resolve_threads:
                thread.join()
        except VkApiError:
            return self.threads_queue
        except KeyboardInterrupt:
            return self.threads_queue

        return self.threads_queue

    def resolve_users_friends(self, user_id: int):
        try:
            return self.api.friends.get(user_id=user_id).get('count')
        except VkApiError as e:
            return {
                f"{type(e)}": f"{str(e)}"
            }

    def start(self):
        try:
            return self.start_threads_resolving()
        except VkApiError:
            print('vk api error, stopping')
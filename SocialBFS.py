import requests
from collections import deque

already_checked_users_ids = []

result = []
destination_target_friends = []

def breadth_search(friends):

    some_set = set()

    while len(friends) > 0:
        first_friend = friends.popleft()
        last_friend = friends.pop() if len(friends) > 0 else None

        already_checked_users_ids.extend([first_friend,last_friend])

        friends_of_first = set(get_friends_from_id(first_friend))
        friends_of_last = set(get_friends_from_id(last_friend))

        s_destination_friends = set(destination_target_friends)

        no_common_friends_from_first = friends_of_first.isdisjoint(s_destination_friends)
        no_common_friends_from_last = friends_of_last.isdisjoint(s_destination_friends)

        if not no_common_friends_from_first:
            graph = dict()
            graph[first_friend] = friends_of_first & s_destination_friends
            result.append(graph)
        else:
            some_set.update(friends_of_first)
        if not no_common_friends_from_last:
            graph = dict()
            graph[last_friend] = friends_of_last & s_destination_friends
            result.append(graph)
        else:
            some_set.update(friends_of_last)
    else:
        #breadth_search(deque(some_set))
        print(result)

def get_friends_from_id(friend_id):
    print(friend_id)
    response = requests.get('https://api.vk.com/method/friends.get?user_id={0}&fields=city'.format(friend_id))
    try:
        dict_repsone = response.json()
        users_response = dict_repsone['response']
        pass
    except Exception as e:
        return []
        pass
    else:
        return [user['user_id'] for user in users_response if user not in already_checked_users_ids]

user_input_source_id = input('Enter source user id: ')
user_input_destination_id = input('Enter destination user id: ')

if user_input_source_id.isdigit() and user_input_destination_id.isdigit():

    source_user_id = int(user_input_source_id)
    destination_user_id = int(user_input_destination_id)

    response = requests.get('https://api.vk.com/method/friends.get?user_id={0}'.format(source_user_id))
    dict_repsone = response.json()
    users_response = dict_repsone['response']

    source_target_friends = [user for user in users_response]
    destination_target_friends = get_friends_from_id(destination_user_id)

    breadth_search(deque(source_target_friends))

else:
    print('One or more of the specified ids is not a numeric value')
    exit(1)

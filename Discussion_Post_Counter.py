from canvas_apps.connect import connect, get_course
from canvas_apps.util.data import json_read
from canvas_apps.ui import get_id_from_file, get_id_from_dict, sift_sort
from canvas_apps.discussions import get_all_entries

## Connect to Canvas
canvas = connect()
course = get_course(canvas)

## Load user and discussion_topic data
users = json_read(f'course_data/{course.id}-users')
discussion_topics = json_read(f'course_data/{course.id}-discussion-topics')

## Get the discussion_topic
topic_id = get_id_from_dict(discussion_topics, 'title')
topic = course.get_discussion_topic(topic_id)
entries = get_all_entries(topic)

# Count posts
post_count = {}
for _, entry in entries.items():
    if entry.user_id not in post_count.keys():
        post_count[entry.user_id] = {'count': 0}
    post_count[entry.user_id]['count'] += 1

# Display results
for user, contents in post_count.items():
    if str(user) in users.keys():
        print(f'{users[str(user)]['sortable_name']}: {contents['count']}')
        contents['sortable_name'] = users[str(user)]['sortable_name']

# Write results to CSV
post_count = sift_sort(post_count, sort_key='sortable_name')

with open(f'{course.id}-{topic.title}.csv', 'w') as file:
    file.write('student_name,post_count\n')
    for _, contents in post_count.items():
        file.write(f'"{contents['sortable_name']}",{contents['count']}\n')
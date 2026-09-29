from canvas_apps.connect import connect, get_course
from canvas_apps.util.data import commas, load_discussions, load_users
from canvas_apps.ui import sift_sort
from canvas_apps.discussions import get_all_entries

## Connect to Canvas
canvas = connect()
course = get_course(canvas)

## Load user and discussion_topic data
users = load_users(course)
discussion_topics = load_discussions(course)

## Prepare for the data
post_counts = {
    user_id: {
        topic_id: 0 for topic_id in discussion_topics
    } for user_id in users
}

for user_id in users:
    post_counts[user_id]['sortable_name'] = users[user_id]['sortable_name']

for topic_id, discussion in discussion_topics.items():
    ## Get the discussion_topic
    print(f'Getting entries for {discussion['title']}')
    topic = course.get_discussion_topic(topic_id)
    entries = get_all_entries(topic)

    # Count posts
    for _, entry in entries.items():
        try:
            post_counts[str(entry.user_id)][topic_id] += 1
        except:
            pass

# Write results to CSV
post_counts = sift_sort(post_counts, sort_key='sortable_name')

with open(f'{course.id}-discussions.csv', 'w') as file:
    file.write(commas(['student_name'] + [ discussion['title'] for _, discussion in discussion_topics.items() ]))
    for _, contents in post_counts.items():
        file.write(commas([contents['sortable_name']] + [ contents[topic_id] for topic_id in discussion_topics ]))
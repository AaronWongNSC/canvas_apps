"""
Code for handling discussion posts
"""

from canvasapi.discussion_topic import DiscussionTopic, DiscussionEntry

def get_all_entries(topic:DiscussionTopic) -> dict:
    """Gets all of the entries (posts) in a discussion topic as a flattened dictionary.

    Parameters
    ----------
    topic : DiscussionTopic
        The discussion topic to extract from.

    Returns
    -------
    dict
        A dictionary of entries whose keys are the entry ID.
    """

    def extract(entry:DiscussionEntry):
        """
        Recursive function to extract all of the entries in a particular discussion tree
        """
        subentries = {entry.id: topic.get_entries([entry.id])[0]}

        try:
            for reply in entry.get_replies():
                subentries = subentries | extract(reply)
        except:
            pass

        return subentries

    entries = {}

    for entry in topic.get_topic_entries():
        entries[entry.id] = topic.get_entries([entry.id])[0]

        entries = entries | extract(entry)
    return entries

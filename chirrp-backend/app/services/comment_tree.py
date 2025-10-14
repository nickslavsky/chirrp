from collections import defaultdict
from typing import List
from app.models.comment import Comment
from app.schemas.comment import CommentResponse

def build_comment_tree(all_comments: List[Comment], top_level_comments: List[Comment]) -> List[CommentResponse]:
    comment_map = {c.id: CommentResponse.from_orm(c) for c in all_comments}
    tree_map = defaultdict(list)
    for comment in all_comments:
        if comment.parent_comment_id:
            tree_map[comment.parent_comment_id].append(comment)
    for parent_id, children in tree_map.items():
        if parent_id in comment_map:
            sorted_children = sorted(children, key=lambda c: c.created_at)
            comment_map[parent_id].children = [comment_map[c.id] for c in sorted_children]
    tree = [comment_map[c.id] for c in sorted(top_level_comments, key=lambda c: c.created_at)]
    return tree
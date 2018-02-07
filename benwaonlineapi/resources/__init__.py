# 1. from packagePy import *

# 2. __all__ = [“module1”, “module2”, module2]

from benwaonlineapi.resources.resources import (
    PostDetail, PostList, PostRelationship,
    TagDetail, TagList, TagRelationship,
    UserDetail, UserList, UserRelationship,
    ImageDetail, ImageList, ImageRelationship,
    PreviewDetail, PreviewList, PreviewRelationship,
    CommentDetail, CommentList, CommentRelationship
)

__all__ = [
    'PostList',
    'PostList',
    'PostRelationship',
    'TagDetail',
    'TagList',
    'TagRelationship',
    'UserDetail',
    'UserList',
    'UserRelationship',
    'PreviewDetail',
    'PreviewList',
    'PreviewRelationship',
    'CommentDetail',
    'CommentList',
    'CommentRelationship'
]

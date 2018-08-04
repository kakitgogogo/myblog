from django import template

from ..models import Comment

register = template.Library()

@register.simple_tag
def parse_comments(comment_queryset, comment=None):
    comments = []

    def parse(superior):
        children = comment_queryset.filter(superior=superior)
        for child in children:
            comments.append(child)
            if superior:
                parse(child)
        
    parse(comment)
    comments.sort(key=lambda comment: comment.created_time, reverse=True)
    return comments

@register.inclusion_tag('comments/tags/comment_item.html')
def display_comment(comment, issuperior=True):
    ident_class = 'outer-comment' if issuperior else 'inner-comment'
    return {
        'ident_class': ident_class,
        'comment': comment
    }
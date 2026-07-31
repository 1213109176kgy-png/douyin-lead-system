from sanic import Blueprint

from application.src.tiktok.views import AwemeDetailView, UserDetailView, AwemeRootCommentView, AwemeSubCommentView, \
    UserPostView, GeneralSearchView, SearchUserView, SearchItemView

routes = {
    'aweme_detail': (AwemeDetailView.as_view(), "获取视频信息"),
    'user_data': (UserDetailView.as_view(), "获取用户详情"),
    'video_comment': (AwemeRootCommentView.as_view(), "获取作品父评论"),
    'video_sub_comment': (AwemeSubCommentView.as_view(), "获取视频二级评论"),
    'user_post': (UserPostView.as_view(), "获取主页发布"),
    'general_search': (GeneralSearchView.as_view(), "综合搜索"),
    'search_user': (SearchUserView.as_view(), "搜索用户"),
    'search_item': (SearchItemView.as_view(), "搜索视频"),

}

TIKTOK_ROUTER = Blueprint('tiktok', url_prefix='tiktok')

for path, (handler, name) in routes.items():
    TIKTOK_ROUTER.add_route(handler, path, name=name)
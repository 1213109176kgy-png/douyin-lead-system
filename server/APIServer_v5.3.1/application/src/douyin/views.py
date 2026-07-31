
from loguru import logger
from sanic import Request
from sanic.views import HTTPMethodView

from application.src.douyin.client.base import RequestValidator
from application.src.douyin.client.core import Client
from core import CustomException, json_success_response
from libs import get_request_data


class AwemeDetailView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=["aweme_id", "share_text"],
            optional_params={"cookie": ""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.aweme_detail(aweme_id=main_id, cookie=validated_data['cookie'],
                                                 )
                return json_success_response(data)
            except Exception as e:
                # logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class MultipleAwemeDetailView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["item_ids"],
            one_of_required_params=[],
            optional_params={}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.multiple_aweme_detail(item_ids=main_id, )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class AwemeDetailV3View(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=["aweme_id", "share_text"],
            optional_params={}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.aweme_detail_v3(aweme_id=main_id, )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class AwemeDetailV4View(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=["aweme_id", "share_text"],
            optional_params={"cookie": ""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.aweme_detail_v4(aweme_id=main_id, cookie=validated_data['cookie'],
                                                    )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class AwemeFansCountView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=["aweme_id", "share_text"],
            optional_params={"cookie": ""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.aweme_new_fans_count(aweme_id=main_id, )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class UserDetailView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=["sec_user_id", "share_text"],
            optional_params={"cookie": ""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.user_detail(sec_user_id=main_id, cookie=validated_data['cookie'],
                                                )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class UserDetailV2View(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=["sec_user_id", "share_text"],
            optional_params={"cookie": ""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.user_detail_v2(sec_user_id=main_id, cookie=validated_data['cookie'],
                                                   )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class UserDetailV3View(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=["sec_user_id", "share_text"],
            optional_params={"cookie": ""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.user_detail_v3(sec_user_id=main_id, )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class UserDetailV4View(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=["sec_user_id", "share_text"],
            optional_params={"cookie": ""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.user_detail_v4(sec_user_id=main_id, )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class UserTagView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=["sec_user_id", "share_text"],
            optional_params={"cookie": ""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.aweme_user_tag(sec_user_id=main_id, )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class UserDetailByUIDView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=["user_id"],
            optional_params={"cookie": ""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.user_detail_by_uid(user_id=main_id, cookie=validated_data['cookie'],
                                                       )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class UserDetailByShortIDView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=["user_id"],
            optional_params={"cookie": ""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.user_detail_by_short_id(user_id=main_id, cookie=validated_data['cookie'],
                                                            )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class UserPostView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=["sec_user_id", "share_text"],
            optional_params={"cookie": "", "max_cursor": "", "count": "3", "filter_type": ""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.user_post(sec_user_id=main_id, cookie=validated_data['cookie'],
                                              max_cursor=validated_data['max_cursor'], count=validated_data['count'],
                                              filter_type=validated_data['filter_type'], )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg



class UserPostV2View(HTTPMethodView):
        async def post(self, request: Request):
            validator = RequestValidator(
                required_params=[],
                one_of_required_params=["sec_user_id", "share_text"],
                optional_params={"max_cursor": "", "count": "12"}
            )

            try:
                validated_data = await validator.validate(request)
            except ValueError as e:
                raise CustomException(message=str(e))
            main_id = validated_data["main_id"]
            retries = 0
            ex_msg = None
            while retries < 5:
                try:
                    client = Client(request)
                    data = await client.user_post_v2(user_id="", sec_user_id=main_id, max_cursor=validated_data['max_cursor'], count=validated_data['count'])
                    return json_success_response(data)
                except Exception as e:
                    logger.error(e)
                    ex_msg = e
                    retries += 1
            raise ex_msg




class UserNewPostView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=["sec_user_id", "share_text"],
            optional_params={"cookie": "", "max_cursor": "", "count": "3"}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.user_new_post(sec_user_id=main_id, cookie=validated_data['cookie'],
                                                  max_cursor=validated_data['max_cursor'],
                                                  count=validated_data['count'],
                                                  )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class UserProductDataView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=["sec_user_id", "share_text"],
            optional_params={"day":"7"}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.user_product_data(sec_uid=main_id, day=validated_data["day"], )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class UserMixView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=["sec_user_id", "share_text"],
            optional_params={"cursor": "", "count": "12"}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.user_mix(sec_user_id=main_id,
                                             cursor=validated_data['cursor'], count=validated_data['count'],
                                             )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class MixInfoView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=["mix_id", "share_text"],
            optional_params={}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.mix_info(mix_id=main_id,
                                             )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class MixAwemeListView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=["mix_id"],
            optional_params={"count": "20", "cursor": ""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.mix_aweme_list(mix_id=main_id, cursor=validated_data['cursor'],
                                                   count=validated_data['count'],
                                                   )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class SearchUserAwemeView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["uid", "keyword"],
            one_of_required_params=[],
            optional_params={"cookie": "", "cursor": "", "count": "10", "search_id": ""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.search_user_aweme(uid=validated_data['uid'], keyword=main_id,
                                                      cookie=validated_data['cookie'],
                                                      search_id=validated_data['search_id'],
                                                      cursor=validated_data['cursor'],
                                                      count=validated_data['count'],
                                                      )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class UserFavView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=["sec_user_id", "share_text"],
            optional_params={"cookie": "", "max_cursor": "", "count": "12"}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.user_fav(sec_user_id=main_id, cookie=validated_data['cookie'],
                                             max_cursor=validated_data['max_cursor'], count=validated_data['count'],
                                             )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class AwemeRootCommentsView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=["aweme_id", "share_text"],
            optional_params={"cursor": "", "count": "10"}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.aweme_root_comments(aweme_id=main_id, count=validated_data['count'],
                                                        cursor=validated_data['cursor'],
                                                        )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class AwemeSubCommentsView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=["comment_id"],
            optional_params={"cursor": "", "count": "10"}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.aweme_sub_comments(comment_id=main_id, count=validated_data['count'],
                                                       cursor=validated_data['cursor'],
                                                       aweme_id=validated_data['aweme_id'],
                                                       )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class UserSeriesView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=["sec_user_id", "share_text"],
            optional_params={"cursor": "", "count": "12"}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.user_series_list(sec_user_id=main_id,
                                                     cursor=validated_data['cursor'], count=validated_data['count'],
                                                     )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class SeriesInfoView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=["series_id", "share_text"],
            optional_params={}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.series_info(series_id=main_id, )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class SeriesAwemeListView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=["series_id"],
            optional_params={"count": "20", "cursor": ""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.series_aweme_list(series_id=main_id, cursor=validated_data['cursor'],
                                                      count=validated_data['count'],
                                                      )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class GeneralSearchV2View(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["keyword"],
            one_of_required_params=[],
            optional_params={"count": "18", "offset": "", "publish_time": "0", "content_type": "0","search_range":"0", "search_id": "",
                             "cookie": "",
                             "filter_duration": "0", "sort_type": "0", "ua":""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.general_search_v2(keyword=main_id, offset=validated_data['offset'],
                                                      search_id=validated_data['search_id'],
                                                      cookie=validated_data.get("cookie") or None,
                                                      filter_duration=validated_data['filter_duration'],
                                                      sort_type=validated_data['sort_type'],
                                                      count=validated_data['count'],
                                                      publish_time=validated_data['publish_time'],
                                                      content_type=validated_data['content_type'],
                                                      search_range=validated_data['search_range'],
                                                      ua=validated_data.get("ua") or None
                                                      )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg



class GeneralSearchV3View(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["keyword"],
            one_of_required_params=[],
            optional_params={"count": "18", "offset": "", "publish_time": "0", "content_type": "0","search_range":"0", "search_id": "",
                             "cookie": "",
                             "filter_duration": "0", "sort_type": "0", "ua":""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.general_search_v3(keyword=main_id, offset=validated_data.get('offset') or "10",
                                                      search_id=validated_data.get('search_id') or "",
                                                      cookie=validated_data.get('cookie') or "",
                                                      filter_duration=validated_data.get('filter_duration') or "",
                                                      sort_type=validated_data.get('sort_type') or "0",
                                                      count=validated_data.get('count') or "10",
                                                      publish_time=validated_data.get('publish_time') or "0",
                                                      content_type=validated_data.get('content_type') or "0",
                                                      search_range=validated_data.get('search_range') or "0",
                                                      ua=validated_data.get("ua") or None
                                                      )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg





class GeneralSearchView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["keyword"],
            one_of_required_params=[],
            optional_params={"count": "18", "offset": "", "publish_time": "0", "content_type": "0", "search_id": "",
                             "cookie": "",
                             "filter_duration": "", "sort_type": "0"}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.general_search(keyword=main_id, offset=validated_data['offset'],
                                                   search_id=validated_data['search_id'],
                                                   cookie=validated_data['cookie'],
                                                   filter_duration=validated_data['filter_duration'],
                                                   sort_type=validated_data['sort_type'],
                                                   count=validated_data['count'],
                                                   publish_time=validated_data['publish_time'],
                                                   content_type=validated_data['content_type'],
                                                   )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg



class GeneralSearchAccountView(HTTPMethodView):
    async def post(self, request: Request):
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.any_account()
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg

class GeneralSearchStreamView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["keyword"],
            one_of_required_params=[],
            optional_params={"count": "18", "offset": "", "publish_time": "0", "content_type": "0", "search_id": "",
                             "cookie": "","search_range":"0",
                             "filter_duration": "", "sort_type": "0"}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        ex_msg = None
        try:
            client = Client(request)
            data = await client.search_stream(keyword=main_id, offset=validated_data.get("offset") or "0",
                                                   search_id=validated_data.get("search_id") or "",
                                                   cookie=validated_data.get("cookie") or None,
                                                   filter_duration=validated_data.get("filter_duration") or "",
                                                   sort_type=validated_data.get("sort_type") or "0",
                                                   count=validated_data.get("count") or "10",
                                                   publish_time=validated_data.get("publish_time") or "0",
                                                   content_type=validated_data['content_type'],search_range=validated_data.get("search_range") or "0")
            return json_success_response(data)
        except Exception as e:
            logger.error(e)
            ex_msg = e
        raise ex_msg



class SearchVideoView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["keyword"],
            one_of_required_params=[],
            optional_params={"count": "18", "offset": "", "publish_time": "0", "search_id": "","search_range":"0", "cookie": "",
                             "filter_duration": "0", "sort_type": "0", 'ua':""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.search_aweme(keyword=main_id, offset=validated_data.get('offset') or "0",
                                                 search_id=validated_data.get('search_id') or "",
                                                 cookie=validated_data.get('cookie') or None,
                                                 filter_duration=validated_data.get('filter_duration') or "",
                                                 sort_type=validated_data.get('sort_type') or "0",
                                                 count=validated_data.get('count') or "10",
                                                 publish_time=validated_data.get('publish_time') or "0",
                                                 search_range=validated_data.get('search_range') or "0",
                                                 ua=validated_data.get("ua") or None
                                                 )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg
class SearchVideoV3View(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["keyword"],
            one_of_required_params=[],
            optional_params={"count": "18", "offset": "", "publish_time": "0", "search_id": "","search_range":"0", "cookie": "",
                             "filter_duration": "0", "sort_type": "0", 'ua':""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.search_aweme_v3(keyword=main_id, offset=validated_data.get('offset') or "0",
                                                 search_id=validated_data.get('search_id') or "",
                                                 cookie=validated_data.get('cookie') or None,
                                                 filter_duration=validated_data.get('filter_duration') or "",
                                                 sort_type=validated_data.get('sort_type') or "0",
                                                 count=validated_data.get('count') or "10",
                                                 publish_time=validated_data.get('publish_time') or "0",
                                                 search_range=validated_data.get('search_range') or "0",
                                                 ua=validated_data.get("ua") or None
                                                 )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg

class SearchVideoV2View(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["keyword"],
            one_of_required_params=[],
            optional_params={"count": "18", "offset": "", "publish_time": "0", "search_id": "", "cookie": "",
                             "filter_duration": "0", "sort_type": "0", "search_d":""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.search_aweme_v2(keyword=main_id, offset=validated_data['offset'],
                                                    search_id=validated_data['search_id'],
                                                    cookie=validated_data['cookie'],
                                                    filter_duration=validated_data['filter_duration'],
                                                    sort_type=validated_data['sort_type'],
                                                    count=validated_data['count'],
                                                    publish_time=validated_data['publish_time'],
                                                    search_d=validated_data.get("search_d") or None,
                                                    )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg





class SearchUserView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["keyword"],
            one_of_required_params=[],
            optional_params={"cursor": ""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.search_user(keyword=main_id, cursor=validated_data['cursor'],
                                                   )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg



class SearchUserV2View(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["keyword"],
            one_of_required_params=[],
            optional_params={"count": "18", "offset": "", "user_type": "0", "search_id": "", "cookie": "",
                             "user_fans": "0", "ua":""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 1:
            try:
                client = Client(request)
                data = await client.search_user_v2(keyword=main_id, offset=validated_data['offset'],
                                                   search_id=validated_data['search_id'],
                                                   cookie=validated_data['cookie'],
                                                   user_type=validated_data['user_type'],
                                                   user_fans=validated_data['user_fans'],
                                                   count=validated_data['count'],
                                                   ua=validated_data.get("ua") or None
                                                   )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class SearchUserV3View(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["keyword"],
            one_of_required_params=[],
            optional_params={"count": "18", "offset": "", "douyin_user_type": "0", "search_id": "", "cookie": "","search_d":"",
                             "douyin_user_fans": "0"}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 1:
            try:
                client = Client(request)
                data = await client.search_user_v3(keyword=main_id, offset=validated_data['offset'],
                                                   search_id=validated_data['search_id'],
                                                   search_d=validated_data['search_d'],
                                                   cookie=validated_data['cookie'],
                                                   douyin_user_type=validated_data['douyin_user_type'],
                                                   douyin_user_fans=validated_data['douyin_user_fans'],
                                                   count=validated_data['count']
                                                   )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg



class SearchMusicView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["keyword"],
            one_of_required_params=[],
            optional_params={"count": "18", "cursor": "", "cookie": "", "search_id":"", "search_session_id":""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.search_music(keyword=main_id, cursor=validated_data['cursor'],
                                                 count=validated_data['count'],
                                                 search_id=validated_data['search_id'] or None,
                                                 )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class MusicInfoView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["music_id"],
            one_of_required_params=[],
            optional_params={"cookie": ""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.music_info(music_id=main_id,
                                               cookie=validated_data['cookie'],
                                               )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class MusicAwemeListView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["music_id"],
            one_of_required_params=[],
            optional_params={"cookie": "", 'count': "10", "cursor": ""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.music_aweme(music_id=main_id,
                                                count=validated_data['count'],
                                                cursor=validated_data['cursor'],
                                                cookie=validated_data['cookie'],
                                                )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class SearchHashtagView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["keyword"],
            one_of_required_params=[],
            optional_params={"count": 10, "page": 1}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.search_hash_tag(keyword=main_id, page=validated_data.get('page') or 1,
                                                    count=validated_data.get('count') or 10
                                                    )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class SearchHashtagV2View(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["keyword"],
            one_of_required_params=[],
            optional_params={"count": "18", "cursor": "", "search_id":""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.search_challenge(keyword=main_id, cursor=validated_data['cursor'],
                                                     count=validated_data['count'], search_id=validated_data['search_id']
                                                     )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class HashTagInfoView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["keyword"],
            one_of_required_params=[],
            optional_params={"cookie": ""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.hash_tag_info(keyword=main_id,
                                                  cookie=validated_data['cookie'],
                                                  )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class HashTagAwemeListView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["ch_id"],
            one_of_required_params=[],
            optional_params={"cookie": "", 'count': "10", "cursor": "", "sort_type": ""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.hash_tag_aweme(ch_id=main_id,
                                                   count=validated_data['count'],
                                                   cursor=validated_data['cursor'],
                                                   sort_type=validated_data['sort_type'],
                                                   cookie=validated_data['cookie'],
                                                   )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class HashTagAwemeListV2View(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["keyword"],
            one_of_required_params=[],
            optional_params={"cookie": "", 'count': "10", "cursor": "", "sort_type": ""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.hash_tag_aweme_v2(keyword=main_id,
                                                      count=validated_data['count'],
                                                      cursor=validated_data['cursor'],
                                                      sort_type=validated_data['sort_type'],
                                                      cookie=validated_data['cookie'],
                                                      )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class SearchLiveUserView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["keyword"],
            one_of_required_params=[],
            optional_params={"count": "18", "cursor": "", "search_id":"", "cookie": ""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.search_live_user(keyword=main_id, offset=validated_data['cursor'],
                                                     search_id=validated_data['search_id'],
                                                     count=validated_data['count'],
                                                     cookie=validated_data['cookie'],
                                                     )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class SearchLiveUserV2View(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["keyword"],
            one_of_required_params=[],
            optional_params={"count": "18", "cursor": "", "search_id":"","search_session_id":"", "cookie": ""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.search_live_user_v2(keyword=main_id, cursor=validated_data['cursor'],
                                                     search_id=validated_data['search_id'],
                                                     search_session_id=validated_data['search_session_id'],
                                                     count=validated_data['count'],
                                                     cookie=validated_data['cookie'],
                                                     )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class LiveRoomInfoByRidView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=['web_rid', 'share_text'],
            optional_params={"cookie": ""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.live_room_info(web_rid=main_id,
                                                   cookie=validated_data['cookie'],
                                                   )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class LiveRoomInfoByIdView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=['room_id', "share_text"],
            optional_params={}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.live_room_info_by_id(room_id=main_id,
                                                         )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class CheckUserLiveStatusView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["user_id"],
            one_of_required_params=[],
            optional_params={}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.check_user_live_status(sec_user_id=main_id,
                                                           )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class LiveRoomUserListView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=['room_id', "share_text"],
            optional_params={"sort_type": "", "cookie":""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.live_room_user_list(room_id=main_id,
                                                        sort_type=validated_data["sort_type"],
                                                        cookie=validated_data.get("cookie") or None
                                                        )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class AwemeDanmakuView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=['aweme_id', "share_text"],
            optional_params={"start_time": "0", "end_time": "3200"}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.aweme_danmaku(aweme_id=main_id,
                                                  start_time=validated_data["start_time"],
                                                  end_time=validated_data["end_time"],
                                                  )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class UserShortLinkView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=['sec_user_id', "share_text"],
            optional_params={}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.user_short_link(sec_user_id=main_id, )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class AwemeShortLinkView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=['aweme_id', "share_text"],
            optional_params={}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.aweme_short_link(aweme_id=main_id, )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class AwemeQRCodeView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=['aweme_id', "share_text"],
            optional_params={}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.aweme_qr_code(aweme_id=main_id, )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class SearchSlugView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=['keyword'],
            optional_params={}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.search_sug(keyword=main_id, )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class SentenceView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=['sentence_id'],
            optional_params={"sort_type":"0", "cursor":""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.hot_spot_aladdin(sentence_id=main_id,sort_type=validated_data['sort_type'], cursor=validated_data['cursor'], )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class SchemeView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=[],
            one_of_required_params=['share_text'],
            optional_params={}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.get_scheme(share_text=validated_data['share_text'], )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class AwemeListNearByView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["city_code"],
            one_of_required_params=[],
            optional_params={"cookie":"", "latitude":"", "longitude":"", "lock_data":""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.nearby_aweme(city_code=main_id, cookie=validated_data['cookie'],latitude=validated_data['latitude'],longitude=validated_data['longitude'], lock_data=validated_data['lock_data'])
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class LiveListNearByView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["city_code"],
            one_of_required_params=[],
            optional_params={"max_time":"", "did":"", "iid":""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.live_room_by_map(city_code=main_id,max_time=validated_data['max_time'],did=validated_data['did'],iid=validated_data['iid'], )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class MediumChannelFeedView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["tag_id"],
            one_of_required_params=[],
            optional_params={"install_time":"", "refresh_index":"", "cookie":""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.medium_channel_feed(tag_id=main_id,install_time=validated_data['install_time'],refresh_index=validated_data['refresh_index'],cookie=validated_data['cookie'], )
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class AwemeBoardView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["board_type"],
            one_of_required_params=[],
            optional_params={"board_sub_type":""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.aweme_board(board_type=main_id, board_sub_type=validated_data.get("board_sub_type", None))
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg

class AwemeShortenView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["aweme_id", "aweme_type"],
            one_of_required_params=[],
            optional_params={}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))
        main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.aweme_shorten(aweme_id=validated_data['aweme_id'], aweme_type=validated_data['aweme_type'])
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class GetAnonymousCookie(HTTPMethodView):
    async def post(self, request: Request):
        retries = 0
        ex_msg = None
        while retries < 1:
            try:
                client = Client(request)
                data = await client.get_anonymous_cookie()
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg



class WeekSelectView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["term"],
            one_of_required_params=[],
            optional_params={"term":"","next_page_ids": ""}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        # main_id = validated_data["main_id"]
        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.week_select_list(term="" if validated_data['term'] == "0" else validated_data['term'], next_page_ids=validated_data['next_page_ids'])
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class IndexFeedView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["refresh_index"],
            one_of_required_params=[],
            optional_params={"refresh_index":"1", "cookie":None}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.index_feed(cookie=validated_data.get("cookie") if validated_data.get("cookie") else None, refresh_index=validated_data.get("refresh_index") or "1")
                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg


class SearchHotValueView(HTTPMethodView):
    async def post(self, request: Request):
        validator = RequestValidator(
            required_params=["keyword"],
            one_of_required_params=[],
            optional_params={"date_window":"", "page_num":1, "page_size":10, "sub_type":3001}
        )

        try:
            validated_data = await validator.validate(request)
        except ValueError as e:
            raise CustomException(message=str(e))

        retries = 0
        ex_msg = None
        while retries < 5:
            try:
                client = Client(request)
                data = await client.search_keyword_value(keyword=validated_data.get("keyword"),
                                                         date_window=validated_data.get("date_window") or 168,
                                                         page_num=validated_data.get("page_num") or 1,
                                                         page_size=validated_data.get("page_size") or 10,
                                                         sub_type=validated_data.get("sub_type") or 3001,)

                return json_success_response(data)
            except Exception as e:
                logger.error(e)
                ex_msg = e
                retries += 1
        raise ex_msg
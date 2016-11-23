import time
from flask_sqlalchemy import SQLAlchemy

from main.plugins.state import get_user_last_interact_time
from .. import app, redis
from ..utils import init_wechat_sdk
from .auth import Auth
from .user import User

db = SQLAlchemy(app)


def set_user_info(openid):
    """
    保存用户信息
    """
    redis_prefix = "wechat:user:"
    cache = redis.hexists(redis_prefix + openid, 'name')

    if not cache:
        user_info = User.query.filter_by(openid=openid).first()
        if not user_info:
            try:
                wechat = init_wechat_sdk()
                user_info = wechat.get_user_info(openid)
                if 'name' not in user_info:
                    raise KeyError(user_info)
            except Exception as e:
                app.logger.warning("获取微信用户信息API出错: %s" % e)
                user_info = None
            else:
                user = User(openid=user_info['openid'],
                            name=user_info['name'],
                            province=user_info['province'],
                            city=user_info['city'],
                            country=user_info['country'],
                            headimgurl=user_info['headimgurl'])
                user.save()
                # 与查询到的数据一致，方便redis写入
                user_info = user

        if user_info:
            # cache it
            redis.hmset(redis_prefix + user_info.openid, {
                "name": user_info.name,
                "province": user_info.province,
                "city": user_info.city,
                "country": user_info.country,
                "headimgurl": user_info.headimgurl,
                "regtime": user_info.regtime
            })
    else:
        timeout = int(time.time()) - int(get_user_last_interact_time(openid))
        if timeout > 24 * 60 * 60:
            try:
                wechat = init_wechat_sdk()
                user_info = wechat.get_user_info(openid)
                if 'name' not in user_info:
                    raise KeyError(user_info)
            except Exception as e:
                app.logger.warning('获取微信用户api出错 %s' % e)
            else:
                user = User.query.filter_by(openid=openid).first()
                user.name = user_info['nickname']
                user.province = user_info['province']
                user.city = user_info['city']
                user.country = user_info['country']
                user.headimgurl = user_info['headimgurl']
                user.regtime = user_info['regtime']
                user.update()

                redis.hmset(redis_prefix + openid, {
                    "name": user_info['nickname'],
                    "province": user_info['province'],
                    "city": user_info['city'],
                    "country": user_info['country'],
                    "headimgurl": user_info['headimgurl']
                })
        return None


def is_user_exists(openid):
    """
    check if user exist in db
    """
    redis_prefix = 'wechat:user:'
    cache = redis.exists(redis_prefix + openid)
    if not cache:
        user_info = User.query.filter_by(openid=openid).first()
        if not user_info:
            return False
        else:
            return True
    else:
        return True

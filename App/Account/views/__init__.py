from .restFul.baseInfo.login_logout import AccountBaseView
from .restFul.baseInfo.register import RegisterView
from .restFul.userInfo.userInfo import UserInfoView
from .restFul.userInfo.userMsgCountInfo import MeView
from .restFul.userInfo.stuInfo.stuUserInfo import StudentUserCheckView

# from .websocket

__all__ = [
    'AccountBaseView', 'RegisterView', 'MeView', 'UserInfoView', 'StudentUserCheckView'
]
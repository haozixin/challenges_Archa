from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 0.Exclude pages that do not require a login to access
        #   request.path_info     get the URL that the current user request for --- (/login/)
        if request.path_info in ["/login/", "/admin/login/?next=/admin/", "/image/code","/admin/"]:
            return

        # 1.read current user's session information. The user has been login if we can get the information

        info_dict = request.session.get("user_info")
        # print(info_dict)
        if info_dict:
            return

        # 2.otherwise, go back to login page
        return redirect('/login/')
        # return
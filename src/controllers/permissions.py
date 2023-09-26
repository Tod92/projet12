from src.controllers.authcontroller import AuthController



class PermissionsMixin:
    """
    Controls app user acess permission
    """

    def has_permission(self, session):
        auth_controller = AuthController()
        self._user = auth_controller.get_authenticated_user(session)
        for p in self._permissions:
            if self._user.role.name == 'Admin':
                return True
            if p == 'isAuth':
                if self._user:
                    return True
            elif p == 'isAffectedTo':
                if self.instance.user_id == self._user.id:
                    return True
            elif p == 'isGestion':
                if self._user.role.name == 'Gestion':
                    return True
            elif p == 'isCommercial':
                if self._user.role.name == 'Commercial':
                    return True
            elif p == 'isSupport':
                if self._user.role.name == 'Support':
                    return True
        self.view.permission_denied()
        exit()



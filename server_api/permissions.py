from rest_framework import permissions

class IsCreationOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            #si pas de view.action passe dans le except 
            try:
                if view.action == 'create':
                    return True
                else:
                    return False
            except:
                return False
        else:
            return True
        
class IsViewOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            #si pas de view.action passe dans le except 
            try:
                if view.action == 'list':
                    return True
                else:
                    return False
            except:
                return False
        else:
            return True
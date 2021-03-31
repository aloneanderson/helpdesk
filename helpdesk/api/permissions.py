from rest_framework import permissions
from helpdesk.models import Requisitions


class CommentPermisson(permissions.BasePermission):
    message = 'You can''t add comment'

    def has_permission(self, request, view):
        if request.method in ['POST']:
            requisitions = Requisitions.objects.get(id=request.data['requisitions'])
            if requisitions.active_status is False:
                return False
        return True


class RequisitionsPermisson(permissions.BasePermission):
    pass

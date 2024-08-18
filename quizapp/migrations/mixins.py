from django.core.exceptions import PermissionDenied


class UserIsOwnerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.quiz.author != request.user or not request.user.is_staff:
            raise PermissionDenied
        return super().dispatch(request, *args, *kwargs)
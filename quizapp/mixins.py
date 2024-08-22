from django.core.exceptions import PermissionDenied


class UserIsOwnerMixin(object):
    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.quiz.author == request.user or request.user.is_staff:
            return super().dispatch(request, *args, *kwargs)
        else:
            raise PermissionDenied


class QuizCanEditMixin(object):
    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author == request.user or request.user.is_staff:
            return super().dispatch(request, *args, *kwargs)
        else:
            raise PermissionDenied
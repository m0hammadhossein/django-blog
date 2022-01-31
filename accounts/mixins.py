from django.http import Http404


class FieldsMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = ('author', 'title', 'category', 'slug', 'description', 'thumbnail', 'publish', 'status')
        elif request.user.is_author:
            self.fields = ('title', 'category', 'slug', 'description', 'thumbnail', 'publish')
        else:
            raise Http404

        return super().dispatch(request, *args, **kwargs)
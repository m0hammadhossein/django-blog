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


class FormValidMixin:
    def form_valid(self, form):
        if not self.request.user.is_superuser:
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.status = 'd'
        return super().form_valid(form)


class AuthorAccessMixin:

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if self.request.user.is_superuser or (obj.author == self.request.user and obj.status == 'd'):
            return obj
        raise Http404


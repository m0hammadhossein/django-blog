from django.http import Http404
from django.shortcuts import redirect


class FieldsMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = ('author', 'title', 'category', 'slug', 'description', 'thumbnail', 'publish', 'is_special', 'status')
        elif request.user.is_author:
            self.fields = ('title', 'category', 'slug', 'description', 'thumbnail', 'publish', 'is_special', 'status')
        else:
            raise Http404

        return super().dispatch(request, *args, **kwargs)


class FormValidMixin:
    def form_valid(self, form):
        if not self.request.user.is_superuser:
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            if self.object.status != 'i':
                self.object.status = 'd'
        return super().form_valid(form)


class AuthorAccessMixin:

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if self.request.user.is_superuser or (obj.author == self.request.user and obj.status in ('d', 'b')):
            return obj
        raise Http404


class AuthorsAccessMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_author:
                return super().dispatch(request, *args, **kwargs)
            return redirect('accounts:profile')
        return redirect('accounts:profile')



class SuperUserAccessMixin:

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise Http404

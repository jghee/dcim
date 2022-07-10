from django.shortcuts import get_object_or_404

from django.views.generic import View

class BaseObjectView(View):
    queryset = None
    template_name = None

    def get_object(self, **kwargs):
        """
        Return the object being viewed or modified. The object is identified by an arbitrary set of keyword arguments
        gleaned from the URL, which are passed to `get_object_or_404()`. (Typically, only a primary key is needed.)

        If no matching object is found, return a 404 response.
        """
        return get_object_or_404(self.queryset, **kwargs)
    
    def get_extra_context(self, request, instance):
        """
        Return any additional context data to include when rendering the template.

        Args:
            request: The current request
            instance: The object being viewed
        """
        return {}

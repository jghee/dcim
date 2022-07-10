from django.shortcuts import redirect, render
from django.urls import reverse

from .base import BaseObjectView


class ObjectView(BaseObjectView):
    """
    Retrieve a single object for display.

    Note: If `template_name` is not specified, it will be determined automatically based on the queryset model.
    """

    def get_template_name(self):
        """
        Return self.template_name if defined. Otherwise, dynamically resolve the template name using the queryset
        model's `app_label` and `model_name`.
        """
        if self.template_name is not None:
            return self.template_name
        model_opts = self.queryset.model._meta
        return f'{model_opts.app_label}/{model_opts.model_name}.html'

    #
    # Request handlers
    #

    def get(self, request, **kwargs):
        """
        GET request handler. `*args` and `**kwargs` are passed to identify the object being queried.

        Args:
            request: The current request
        """
        instance = self.get_object(**kwargs)

        return render(request, self.get_template_name(), {
            'object': instance,
            **self.get_extra_context(request, instance),
        })


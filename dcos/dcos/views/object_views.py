from django.shortcuts import redirect, render
from django.urls import reverse

from .base import BaseObjectView, BaseMultiObjectView


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


class ObjectListView(BaseMultiObjectView):
    template_name = 'dcim/object_list.html'
    # filterset = None
    # filterset_form = None

    # def get_table(self, request):
    #     table = self.table(self.queryset)
    #     if 'pk' in table.base_columns:
    #         table.columns.show('pk')
    #
    #     return table

    #
    # Request handlers
    #
    def get(self, request):
        model = self.queryset
            # .model
        q = request.GET.get('q', '')
        if q:
            model = model.filter(name__icontains=q)
        # if self.filterset:
        #     self.filterset = self.filterset(request,GET, self.queryset).qs

        # table = self.get_table(request)

        context = {
            'model': model,
            # 'talbe': table,
            # 'filter_form': self.filterset_form(request.GET, label_suffix='') if self.filterset_form else None,
            'q': q,
            **self.get_extra_context(request),
        }

        return render(request, self.template_name, context)

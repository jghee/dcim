from django.shortcuts import redirect, render
from django.db import transaction
from django.urls import reverse

from dcos.utilites.utils import normalize_querydict
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

class ObjectEditView(BaseObjectView):
    """
    Create or edit a single object.

    Attributes:
        form: The form used to create or edit the object
    """
    template_name = 'dcim/object_edit.html'
    # template_name = 'generic/object_edit.html'
    form = None

    # def dispatch(self, request, *args, **kwargs):
    #     # Determine required permission based on whether we are editing an existing object
    #     self._permission_action = 'change' if kwargs else 'add'
    #
    #     return super().dispatch(request, *args, **kwargs)

    # def get_required_permission(self):
    #     # self._permission_action is set by dispatch() to either "add" or "change" depending on whether
    #     # we are modifying an existing object or creating a new one.
    #     return get_permission_for_model(self.queryset.model, self._permission_action)

    def get_object(self, **kwargs):
        """
        Return an object for editing. If no keyword arguments have been specified, this will be a new instance.
        """
        if not kwargs:
            # We're creating a new object
            return self.queryset.model()
        return super().get_object(**kwargs)

    def alter_object(self, obj, request, url_args, url_kwargs):
        """
        Provides a hook for views to modify an object before it is processed. For example, a parent object can be
        defined given some parameter from the request URL.

        Args:
            obj: The object being edited
            request: The current request
            url_args: URL path args
            url_kwargs: URL path kwargs
        """
        return obj

    #
    # Request handlers
    #

    def get(self, request, *args, **kwargs):
        """
        GET request handler.

        Args:
            request: The current request
        """
        obj = self.get_object(**kwargs)
        obj = self.alter_object(obj, request, args, kwargs)

        initial_data = normalize_querydict(request.GET)
        form = self.form(instance=obj, initial=initial_data)
        # restrict_form_fields(form, request.user)

        return render(request, self.template_name, {
            'object': obj,
            'form': form,
            # 'return_url': self.get_return_url(request, obj),
            **self.get_extra_context(request, obj),
        })

    def post(self, request, *args, **kwargs):
        """
        POST request handler.

        Args:
            request: The current request
        """
        # logger = logging.getLogger('netbox.views.ObjectEditView')
        obj = self.get_object(**kwargs)

        # Take a snapshot for change logging (if editing an existing object)
        # if obj.pk and hasattr(obj, 'snapshot'):
        #     obj.snapshot()

        obj = self.alter_object(obj, request, args, kwargs)

        form = self.form(data=request.POST, files=request.FILES, instance=obj)
        # restrict_form_fields(form, request.user)

        if form.is_valid():
            print("Form validation was successful")
            # logger.debug("Form validation was successful")

            # try:
            with transaction.atomic():
                    object_created = form.instance.pk is None
                    obj = form.save()

                    # Check that the new object conforms with any assigned object-level permissions
                    if not self.queryset.filter(pk=obj.pk).first():
                        print("Permission Violation")
                        # raise PermissionsViolation()

                # msg = '{} {}'.format(
                #     'Created' if object_created else 'Modified',
                #     self.queryset.model._meta.verbose_name
                # )
                # logger.info(f"{msg} {obj} (PK: {obj.pk})")
                # if hasattr(obj, 'get_absolute_url'):
                #     msg = '{} <a href="{}">{}</a>'.format(msg, obj.get_absolute_url(), escape(obj))
                # else:
                #     msg = '{} {}'.format(msg, escape(obj))
                # messages.success(request, mark_safe(msg))

                # if '_addanother' in request.POST:
                #     redirect_url = request.path
                #
                #     # If the object has clone_fields, pre-populate a new instance of the form
                #     params = prepare_cloned_fields(obj)
                #     if 'return_url' in request.GET:
                #         params['return_url'] = request.GET.get('return_url')
                #     if params:
                #         redirect_url += f"?{params.urlencode()}"
                #
                #     return redirect(redirect_url)

            return_url = '/dcim/tenants'
            # return_url = self.get_return_url(request, obj)

            return redirect(return_url)

            # except PermissionsViolation:
            #     msg = "Object save failed due to object-level permissions violation"
            #     logger.debug(msg)
            #     form.add_error(None, msg)
            #     clear_webhooks.send(sender=self)

        else:
            print("Form Validation failed")
            # logger.debug("Form validation failed")

        return render(request, self.template_name, {
            'object': obj,
            'form': form,
            # 'return_url': self.get_return_url(request, obj),
            **self.get_extra_context(request, obj),
        })

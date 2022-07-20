from django.shortcuts import render

# Create your views here.
from dcim.models import Tenant
from dcos.views.object_views import ObjectView, ObjectListView


def home(request):
    return render(request, "base.html")


class TenantView(ObjectView):
    queryset = Tenant.objects.prefetch_related('group')

    def get_extra_context(self, request, instance):
        stats = {
            # 'site_count': Site.objects.restrict(request.user, 'view').filter(tenant=instance).count(),
            # 'rack_count': Rack.objects.restrict(request.user, 'view').filter(tenant=instance).count(),
            # 'rackreservation_count': RackReservation.objects.restrict(request.user, 'view').filter(tenant=instance).count(),
            # 'location_count': Location.objects.restrict(request.user, 'view').filter(tenant=instance).count(),
            # 'device_count': Device.objects.restrict(request.user, 'view').filter(tenant=instance).count(),
            # 'vrf_count': VRF.objects.restrict(request.user, 'view').filter(tenant=instance).count(),
            # 'prefix_count': Prefix.objects.restrict(request.user, 'view').filter(tenant=instance).count(),
            # 'aggregate_count': Aggregate.objects.restrict(request.user, 'view').filter(tenant=instance).count(),
            # 'ipaddress_count': IPAddress.objects.restrict(request.user, 'view').filter(tenant=instance).count(),
            # 'vlan_count': VLAN.objects.restrict(request.user, 'view').filter(tenant=instance).count(),
            # 'circuit_count': Circuit.objects.restrict(request.user, 'view').filter(tenant=instance).count(),
            # 'virtualmachine_count': VirtualMachine.objects.restrict(request.user, 'view').filter(tenant=instance).count(),
            # 'cluster_count': Cluster.objects.restrict(request.user, 'view').filter(tenant=instance).count(),
            # 'cable_count': Cable.objects.restrict(request.user, 'view').filter(tenant=instance).count(),
            # 'asn_count': ASN.objects.restrict(request.user, 'view').filter(tenant=instance).count(),
        }

        return {
            'stats': stats,
        }


class TenantListView(ObjectListView):
    queryset = Tenant.objects.all()
    # filterset =
    # filterset_form =
    # table = tables.TenantTable

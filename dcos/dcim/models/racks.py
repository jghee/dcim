from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

__all__ = [
    'Rack',
]

#
# Racks
#
class Rack(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    site = models.ForeignKey(
        to='dcim.Site',
        on_delete=models.PROTECT,
        related_name='racks'
    )
    location = models.ForeignKey(
        to='dcim.Location',
        on_delete=models.SET_NULL,
        related_name='racks',
        blank=True,
        null=True
    )
    u_height = models.PositiveSmallIntegerField(
        default=42,
        verbose_name='Height (U)',
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text='Height in rack units'
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('dcim:rack', args=[self.pk])

    class Meta:
        ordering = ('site', 'location', 'name', 'pk')  # (site, location, name) may be non-unique
        unique_together = (
            # Name and facility_id must be unique *only* within a Location
            ('location', 'name'),
        )

    # def clean(self):
    #     super().clean()
    #
    #     # Validate location/site assignment
    #     if self.site and self.location and self.location.site != self.site:
    #         raise ValidationError(f"Assigned location must belong to parent site ({self.site}).")
    #
    #     # Validate outer dimensions and unit
    #     if (self.outer_width is not None or self.outer_depth is not None) and not self.outer_unit:
    #         raise ValidationError("Must specify a unit when setting an outer width/depth")
    #     elif self.outer_width is None and self.outer_depth is None:
    #         self.outer_unit = ''
    #
    #     if self.pk:
    #         # Validate that Rack is tall enough to house the installed Devices
    #         top_device = Device.objects.filter(
    #             rack=self
    #         ).exclude(
    #             position__isnull=True
    #         ).order_by('-position').first()
    #         if top_device:
    #             min_height = top_device.position + top_device.device_type.u_height - 1
    #             if self.u_height < min_height:
    #                 raise ValidationError({
    #                     'u_height': "Rack must be at least {}U tall to house currently installed devices.".format(
    #                         min_height
    #                     )
    #                 })
    #         # Validate that Rack was assigned a Location of its same site, if applicable
    #         if self.location:
    #             if self.location.site != self.site:
    #                 raise ValidationError({
    #                     'location': f"Location must be from the same site, {self.site}."
    #                 })
    #
    # @property
    # def units(self):
    #     if self.desc_units:
    #         return range(1, self.u_height + 1)
    #     else:
    #         return reversed(range(1, self.u_height + 1))
    #
    # def get_status_color(self):
    #     return RackStatusChoices.colors.get(self.status)
    #
    # def get_rack_units(self, user=None, face=DeviceFaceChoices.FACE_FRONT, exclude=None, expand_devices=True):
    #     """
    #     Return a list of rack units as dictionaries. Example: {'device': None, 'face': 0, 'id': 48, 'name': 'U48'}
    #     Each key 'device' is either a Device or None. By default, multi-U devices are repeated for each U they occupy.
    #     :param face: Rack face (front or rear)
    #     :param user: User instance to be used for evaluating device view permissions. If None, all devices
    #         will be included.
    #     :param exclude: PK of a Device to exclude (optional); helpful when relocating a Device within a Rack
    #     :param expand_devices: When True, all units that a device occupies will be listed with each containing a
    #         reference to the device. When False, only the bottom most unit for a device is included and that unit
    #         contains a height attribute for the device
    #     """
    #
    #     elevation = OrderedDict()
    #     for u in self.units:
    #         elevation[u] = {
    #             'id': u,
    #             'name': f'U{u}',
    #             'face': face,
    #             'device': None,
    #             'occupied': False
    #         }
    #
    #     # Add devices to rack units list
    #     if self.pk:
    #
    #         # Retrieve all devices installed within the rack
    #         queryset = Device.objects.prefetch_related(
    #             'device_type',
    #             'device_type__manufacturer',
    #             'device_role'
    #         ).annotate(
    #             devicebay_count=Count('devicebays')
    #         ).exclude(
    #             pk=exclude
    #         ).filter(
    #             rack=self,
    #             position__gt=0,
    #             device_type__u_height__gt=0
    #         ).filter(
    #             Q(face=face) | Q(device_type__is_full_depth=True)
    #         )
    #
    #         # Determine which devices the user has permission to view
    #         permitted_device_ids = []
    #         if user is not None:
    #             permitted_device_ids = self.devices.restrict(user, 'view').values_list('pk', flat=True)
    #
    #         for device in queryset:
    #             if expand_devices:
    #                 for u in range(device.position, device.position + device.device_type.u_height):
    #                     if user is None or device.pk in permitted_device_ids:
    #                         elevation[u]['device'] = device
    #                     elevation[u]['occupied'] = True
    #             else:
    #                 if user is None or device.pk in permitted_device_ids:
    #                     elevation[device.position]['device'] = device
    #                 elevation[device.position]['occupied'] = True
    #                 elevation[device.position]['height'] = device.device_type.u_height
    #                 for u in range(device.position + 1, device.position + device.device_type.u_height):
    #                     elevation.pop(u, None)
    #
    #     return [u for u in elevation.values()]
    #
    def get_available_units(self, u_height=1, rack_face=None, exclude=None):
        """
        Return a list of units within the rack available to accommodate a device of a given U height (default 1).
        Optionally exclude one or more devices when calculating empty units (needed when moving a device from one
        position to another within a rack).
        :param u_height: Minimum number of contiguous free units required
        :param rack_face: The face of the rack (front or rear) required; 'None' if device is full depth
        :param exclude: List of devices IDs to exclude (useful when moving a device within a rack)
        """
        # Gather all devices which consume U space within the rack
        devices = self.devices.prefetch_related('device_type').filter(position__gte=1)
        if exclude is not None:
            devices = devices.exclude(pk__in=exclude)

        # Initialize the rack unit skeleton
        units = list(range(1, self.u_height + 1))

        # Remove units consumed by installed devices
        for d in devices:
            if rack_face is None or d.face == rack_face or d.device_type.is_full_depth:
                for u in range(d.position, d.position + d.device_type.u_height):
                    try:
                        units.remove(u)
                    except ValueError:
                        # Found overlapping devices in the rack!
                        pass

        # Remove units without enough space above them to accommodate a device of the specified height
        available_units = []
        for u in units:
            if set(range(u, u + u_height)).issubset(units):
                available_units.append(u)

        return list(reversed(available_units))

    # def get_reserved_units(self):
    #     """
    #     Return a dictionary mapping all reserved units within the rack to their reservation.
    #     """
    #     reserved_units = {}
    #     for r in self.reservations.all():
    #         for u in r.units:
    #             reserved_units[u] = r
    #     return reserved_units

    # def get_elevation_svg(
    #         self,
    #         face=DeviceFaceChoices.FACE_FRONT,
    #         user=None,
    #         unit_width=None,
    #         unit_height=None,
    #         legend_width=RACK_ELEVATION_LEGEND_WIDTH_DEFAULT,
    #         include_images=True,
    #         base_url=None
    # ):
    #     """
    #     Return an SVG of the rack elevation
    #     :param face: Enum of [front, rear] representing the desired side of the rack elevation to render
    #     :param user: User instance to be used for evaluating device view permissions. If None, all devices
    #         will be included.
    #     :param unit_width: Width in pixels for the rendered drawing
    #     :param unit_height: Height of each rack unit for the rendered drawing. Note this is not the total
    #         height of the elevation
    #     :param legend_width: Width of the unit legend, in pixels
    #     :param include_images: Embed front/rear device images where available
    #     :param base_url: Base URL for links and images. If none, URLs will be relative.
    #     """
    #     elevation = RackElevationSVG(self, user=user, include_images=include_images, base_url=base_url)
    #     if unit_width is None or unit_height is None:
    #         config = get_config()
    #         unit_width = unit_width or config.RACK_ELEVATION_DEFAULT_UNIT_WIDTH
    #         unit_height = unit_height or config.RACK_ELEVATION_DEFAULT_UNIT_HEIGHT
    #
    #     return elevation.render(face, unit_width, unit_height, legend_width)
    #
    # def get_0u_devices(self):
    #     return self.devices.filter(position=0)
    #
    def get_utilization(self):
        """
        Determine the utilization rate of the rack and return it as a percentage. Occupied and reserved units both count
        as utilized.
        """
        # Determine unoccupied units
        available_units = self.get_available_units()

        # Remove reserved units
        # for u in self.get_reserved_units():
        #     if u in available_units:
        #         available_units.remove(u)

        occupied_unit_count = self.u_height - len(available_units)
        percentage = float(occupied_unit_count) / self.u_height * 100

        return percentage
    #
    # def get_power_utilization(self):
    #     """
    #     Determine the utilization rate of power in the rack and return it as a percentage.
    #     """
    #     powerfeeds = PowerFeed.objects.filter(rack=self)
    #     available_power_total = sum(pf.available_power for pf in powerfeeds)
    #     if not available_power_total:
    #         return 0
    #
    #     pf_powerports = PowerPort.objects.filter(
    #         _link_peer_type=ContentType.objects.get_for_model(PowerFeed),
    #         _link_peer_id__in=powerfeeds.values_list('id', flat=True)
    #     )
    #     poweroutlets = PowerOutlet.objects.filter(power_port_id__in=pf_powerports)
    #     allocated_draw_total = PowerPort.objects.filter(
    #         _link_peer_type=ContentType.objects.get_for_model(PowerOutlet),
    #         _link_peer_id__in=poweroutlets.values_list('id', flat=True)
    #     ).aggregate(Sum('allocated_draw'))['allocated_draw__sum'] or 0
    #
    #     return int(allocated_draw_total / available_power_total * 100)

# store/models.py
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from loans.models import Functionteam

class Store(models.Model):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, related_name='owned_stores',
        verbose_name=_('owner'),
    )
    name = models.CharField(
        max_length=20,
        unique=True, 
        verbose_name=_('name'),
    )
    notes = models.TextField(
        blank=True, default='', verbose_name=_('notes'),
    )

    class Meta:
        verbose_name = _('Store')
        verbose_name_plural = _('Stores')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store_detail', kwargs={'pk': self.pk})

    def can_user_delete(self, user):
        #if not self.owner or self.owner == user:
        #    return True
        if user.has_perm('stores.delete_store'):
            return True
        return False

class MenuItem(models.Model):

    store = models.ForeignKey(
        'Store', related_name='menu_items',
        verbose_name=_('store'),
    )
    build = models.CharField(
        max_length=10, blank=True, null=True,
        default=settings.BUILD_VER,
        verbose_name=_('Build'),
    )
    config = models.CharField(
        max_length=10,
        blank=True, null=True,
        verbose_name=_('Config'),
    )
    unit_no = models.CharField(
        max_length=20, blank=True, null=True,
        unique=True,
        verbose_name=_('Unit No.'),
    )
    isn = models.CharField(
        max_length=20, blank=True, null=True,
        unique=True,
        verbose_name=_('ISN'),
    )
    ffned = models.IntegerField(
        default=0,
        verbose_name=_('FF/NED'),
    )
    function_team = models.ForeignKey(
        Functionteam, blank=True, null=True,
        verbose_name=_('Function Team'),
    )
    utk = models.CharField(
        max_length=100, blank=True, null=True,
        verbose_name=_('UTK'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False,
    )
    cg_color = models.CharField(
        max_length=10, blank=True, null=True,
        verbose_name=_('CG Color'),
    )
    hsg = models.CharField(
        max_length=10, blank=True, null=True,
        verbose_name=_('HSG'),
    )
    # 0: Pending, 1: Approve, 2: Reject
    is_approved = models.IntegerField(
        default=0,
    )

    class Meta:
        verbose_name = _('MenuItem')
        verbose_name_plural = _('MenuItems')

    def get_absolute_url(self):
        return reverse('store_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.isn

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from stores.models import MenuItem

class Pegadri(models.Model):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True,
        related_name='owned_pegadri',
        verbose_name=_('owner'),
    )
    name = models.CharField(
        max_length=50,
        verbose_name=_('name'),
    )
    email = models.EmailField(
        blank=False, null=False,
        verbose_name=_('email'),
    )

    class Meta:
        verbose_name = _('Pegadri')
        verbose_name_plural = _('Pegadris')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pegadri_detail', kwargs={'pk': self.pk})

    def can_user_delete(self, user):
        if not self.owner or self.owner == user:
            return True
        if user.has_perm('events.delete_pegadri'):
            return True
        return False

class Cocodri(models.Model):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True,
        related_name='owned_cocodri',
        verbose_name=_('owner'),
    )
    name = models.CharField(
        max_length=50,
        verbose_name=_('name'),
    )
    email = models.EmailField(
        blank=False, null=False,
        verbose_name=_('email'),
    )

    class Meta:
        verbose_name = _('Cocodri')
        verbose_name_plural = _('Cocodris')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cocodri_detail', kwargs={'pk': self.pk})

    def can_user_delete(self, user):
        if not self.owner or self.owner == user:
            return True
        if user.has_perm('events.delete_cocodri'):
            return True
        return False

class Event(models.Model):

    store = models.ForeignKey('stores.Store', related_name='events')

    class Meta:
        get_latest_by = 'pk'

    def __str__(self):
        return str(self.store)

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.pk})

class Order(models.Model):

    event = models.ForeignKey(Event, related_name='orders')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders')
    item = models.ForeignKey(MenuItem, related_name='orders')
    notes = models.TextField(blank=True, default='')
    cocodri = models.ForeignKey(
        Cocodri, blank=False, null=True,
        related_name='cocodri_item', 
        verbose_name=_('CoCo DRI'),
    )
    pegadri = models.ForeignKey(
        Pegadri, blank=False, null=True,
        related_name='pegadri_item', 
        verbose_name=_('Pega DRI'),
    )

    class Meta:
        unique_together = ('event', 'user',)

    # TODO(chairco@gmail.com): use __unicode__ to solve __str__
    def __unicode__(self):
        return '{item} of {user} for {event}'.format(
            item_name=self.item, user=self.user, event=self.event
        )
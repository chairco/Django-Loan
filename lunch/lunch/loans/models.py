# loans/models.py
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import (
    MaxValueValidator, MinValueValidator, RegexValidator
)
from django.contrib.auth.models import User

class Log(models.Model):
    
    name = models.CharField(
        max_length=30,
        verbose_name=_('name'),
    )
    function = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_('function'),
    )
    info = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_('info'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    class Meta:
        verbose_name = _('Log')
        verbose_name_plural = _('Logs')

    def __str__(self):
        return self.name


class Pegadri(models.Model):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True,
        related_name='owned_laon_pegadri',
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
        return self.name+','+str(self.email)

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
        related_name='owned_loan_cocodri',
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
        return self.name+','+str(self.email)

    def get_absolute_url(self):
        return reverse('cocodri_detail', kwargs={'pk': self.pk})

    def can_user_delete(self, user):
        if not self.owner or self.owner == user:
            return True
        if user.has_perm('events.delete_cocodri'):
            return True
        return False

class Functionteam(models.Model):

    name = models.CharField(
        max_length=30,
        verbose_name=_('name'),
    )

    class Meta:
        verbose_name = _('Functionteam')
        verbose_name_plural = _('Functionteams')

    def __str__(self):
        return self.name

class Station(models.Model):

    name = models.CharField(
        max_length=30,
        verbose_name=_('name'),
    )

    class Meta:
        verbose_name = _('Station')
        verbose_name_plural = _('Stations')

    def __str__(self):
        return self.name

class Loan(models.Model):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, related_name='owned_loans',
    )
    function_team = models.ForeignKey(
        Functionteam,
        verbose_name=_('Function Team')
    )
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
    purpose = models.CharField(
        max_length=100, null=True,
        validators=[
            RegexValidator(
               regex=r"^[a-z A-Z 0-9 \[^\u4e00-\u9fa5\] /,.?~!@#$%^&*()_+]*$",
               message='Chinese characters are restricted. Must be Alphanumeric \
                        (只接受英文、數字、半形符號)',
               code='invalid',
            ),
        ]
    )
    disassemble = models.BooleanField(
        #default=False,
        blank=False,
        verbose_name=_('Disassemble（會拆機台）'),
    )
    pega_dri_mail_group = models.CharField(
        max_length=300,
        null=True,
        verbose_name=_('Pega DRI Mail Group'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Loan')
        verbose_name_plural = _('Loans')

    def __str__(self):
        return self.purpose

    def get_absolute_url(self):
        return reverse('loan_detail', kwargs={'pk': self.pk})

    def can_user_delete(self, user):
        #if not self.owner or self.owner == user:
        #    return True
        if user.has_perm('loans.delete_store'):
            return True
        return False

class Device(models.Model):

    request = models.ForeignKey(
        'Loan',
        related_name='menu_items', 
        verbose_name=_('loan'),
    )
    station = models.ForeignKey(
        'Station',
        related_name='grpnm_items', 
        verbose_name=_('Station'),
    )
    config = models.CharField(
        max_length=10,
        blank=True, null=True,
    )
    unit_no = models.CharField(
        max_length=20,
        blank=True, null=True,
    )
    isn = models.CharField(
        max_length=20,
        blank=False, null=True,
        verbose_name=_('ISN'),
    )
    failure_symptoms = models.CharField(
        max_length=300,
        blank=False, null=True,
    )
    utk = models.CharField(
        max_length=300,
        blank=True, null=True,
    )
    grpnm = models.CharField(
        max_length=30,
        blank=True, null=True,
        verbose_name=_('GRPNM'),
    )
    # Below is for admin
    status = models.IntegerField(
        default=0,
    )
    is_approved = models.BooleanField(
        default=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    sfis_status = models.BooleanField(
        default=False,
    )
    sfis_info = models.CharField(
        max_length=40,
        blank=True, null=True,
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Device')
        verbose_name_plural = _('Devices')

    def __str__(self):
        return self.isn

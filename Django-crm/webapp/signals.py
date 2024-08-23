from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from .models import *
from django.dispatch import receiver
from django.contrib.auth.models import Group


@receiver(post_save, sender=User)
# another  method to use decorator to connect reciever to sender
def customer_profile(sender, instance, created, **kwargs):
    '''receiver function when signal is received'''
    if created:
        # when user signup add customer group to user
        customer_group = Group.objects.get(name='customer')
        instance.groups.add(customer_group)
        # when user signup add user to customer
        Customer.objects.create(user=instance,
                                name=instance.username)
        print('<<<<<<<,PROFILE CREATED>>>>>>>>>>>>>')


# one method to connect reciever to sender for signal
post_save.connect(customer_profile, sender=User)

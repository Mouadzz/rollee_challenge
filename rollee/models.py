from django.db import models


"""
Relations:

- User and AccountRecord have a one-to-many relationship, where one User can have multiple AccountRecords.
- AccountRecord and Profile have a one-to-one relationship, where each AccountRecord can have one associated Profile.
- AccountRecord and Vehicle have a one-to-many relationship, where one AccountRecord can have multiple Vehicles.
"""


class User(models.Model):
    id = models.UUIDField(primary_key=True)


class Platform(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField()
    logo = models.URLField()


class AccountRecord(models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="accounts")
    name = models.CharField()
    status = models.CharField()
    avatar = models.URLField()
    email = models.EmailField()
    platform = models.ForeignKey(
        Platform, on_delete=models.SET_NULL, null=True)
    country = models.CharField()
    last_update = models.DateTimeField()
    currency = models.CharField()
    gross_earnings = models.FloatField()
    net_amount = models.FloatField()
    taxes = models.FloatField()
    bonus_amount = models.FloatField()
    platform_fee = models.FloatField()
    activity = models.JSONField(null=True)
    trips = models.JSONField(null=True)
    employment = models.JSONField(null=True)
    documents = models.JSONField(null=True)


class Profile(models.Model):
    account = models.OneToOneField(
        AccountRecord, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField()
    last_name = models.CharField()
    full_name = models.CharField()
    phone = models.CharField()
    email = models.EmailField()
    image_url = models.URLField()
    street = models.CharField()
    zip = models.CharField()
    country_phone_code = models.CharField()
    licence_number = models.CharField(null=True)
    licence_expire_dt = models.DateField(null=True)


class Vehicle(models.Model):
    account = models.ForeignKey(
        AccountRecord, on_delete=models.CASCADE, related_name="vehicles")
    make = models.CharField()
    model = models.CharField()
    year = models.CharField()
    license_plate = models.CharField()

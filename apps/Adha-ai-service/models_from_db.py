# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ApiChatconversation(models.Model):
    conversation_id = models.CharField(primary_key=True, max_length=32)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    company_context = models.JSONField()
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_chatconversation'


class ApiChatmessage(models.Model):
    message_id = models.CharField(primary_key=True, max_length=32)
    is_user = models.BooleanField()
    content = models.TextField()
    timestamp = models.DateTimeField()
    relevant_entries = models.JSONField()
    conversation = models.ForeignKey(ApiChatconversation, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'api_chatmessage'


class ApiJournalentry(models.Model):
    date = models.DateField()
    piece_reference = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    debit_data = models.JSONField()
    credit_data = models.JSONField()
    created_by = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)
    source_data = models.JSONField()
    source_type = models.CharField(max_length=20)
    company_id = models.IntegerField(blank=True, null=True)
    journal = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'api_journalentry'


class ApiTokenquota(models.Model):
    max_tokens = models.BigIntegerField()
    reset_period = models.CharField(max_length=10)
    last_reset = models.DateTimeField()
    price_per_million = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.OneToOneField('AuthUser', models.DO_NOTHING)
    monthly_quota = models.IntegerField()
    remaining_quota = models.IntegerField()
    reset_date = models.DateTimeField(blank=True, null=True)
    plan_type = models.CharField(max_length=20)
    last_updated = models.DateTimeField()
    total_tokens_used = models.BigIntegerField()
    additional_settings = models.JSONField()

    class Meta:
        managed = False
        db_table = 'api_tokenquota'


class ApiTokentransaction(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length=20)
    reference = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField()
    notes = models.TextField()
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)
    company_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'api_tokentransaction'


class ApiTokenusage(models.Model):
    operation_id = models.CharField(max_length=100)
    operation_type = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    input_tokens = models.IntegerField()
    output_tokens = models.IntegerField()
    total_tokens = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)
    model_name = models.CharField(max_length=50)
    metadata = models.JSONField()
    message_id = models.CharField(unique=True, max_length=100)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'api_tokenusage'


class ApiTokenusageNew(models.Model):
    message_id = models.TextField(primary_key=True, blank=True, null=True)
    user_id = models.IntegerField()
    operation_type = models.TextField()
    model = models.TextField()
    input_tokens = models.IntegerField()
    output_tokens = models.IntegerField()
    total_tokens = models.IntegerField()
    operation_id = models.TextField()
    metadata = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'api_tokenusage_new'


class ApiUserprofile(models.Model):
    company_name = models.CharField(max_length=100, blank=True, null=True)
    company_type = models.CharField(max_length=50, blank=True, null=True)
    sector = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    user = models.OneToOneField('AuthUser', models.DO_NOTHING)
    company_info = models.JSONField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    preferred_language = models.CharField(max_length=10)
    company_id = models.IntegerField(blank=True, null=True)
    is_company_admin = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'api_userprofile'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

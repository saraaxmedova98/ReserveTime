from django.db import models
from django.utils.translation import ugettext as _



class Company(models.Model):

    PAYMENT_CHOICES = (
        ('AMEX', 'AMEX'),
        ('DinersClub', 'Diners Club'),
        ('MasterCard', 'MasterCard'),
        ('Visa', 'Visa'),
    )
    user = models.OneToOneField("account.User", verbose_name=_(""), on_delete=models.CASCADE, related_name = 'company')
    
    company_name = models.CharField(_("Company Name"), max_length=250)
    phone_number = models.CharField(_("Phone Number"), max_length=50)
    cover_photo = models.ImageField(_("Photo"), upload_to='company-photos/', blank=True, null=True)

    city_location = models.CharField(_("City"), max_length=150)
    province_location = models.CharField(_("Province"), max_length=150)
    country_location = models.CharField(_("Country"), max_length=150)

    work_hours_from = models.TimeField(_("Start Time"), auto_now=False, auto_now_add=False, blank=True, null=True)
    work_hours_to = models.TimeField(_("Finish Time"), auto_now=False, auto_now_add=False, blank=True, null=True)

    cuisine = models.ForeignKey("restaurant.Cuisine", verbose_name=_("Cuisine"), on_delete=models.CASCADE, related_name='company', blank=True, null=True)
    dining_style = models.CharField(_("Dining Style"), max_length=50,  blank=True, null=True)
    parking_details = models.TextField(_("Parking details"), blank=True, null=True)
    public_transit = models.TextField(_("Public transit"), blank=True, null=True)
    payment_options = models.CharField(_("Payment Options"), choices = PAYMENT_CHOICES, max_length=50, blank=True, null=True)
    executive_chef = models.CharField(_("Executive chef"), max_length=50, blank=True, null=True)
    website = models.URLField(_("Website"), max_length=200, blank=True, null=True)
    private_party_contact = models.CharField(_("Private party contact"), max_length=150, blank=True, null=True)
    description = models.TextField(_("Description"),  blank=True, null=True)
    
    overall = models.IntegerField(_("Overall"), blank=True, null=True)
    created_at = models.DateField(_("Created date"), auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Comapany'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.user.email


class Cuisine(models.Model):

    title = models.CharField(_("Cuisine Title"), max_length=50)
    image = models.ImageField(_("Image"), upload_to='cuisines/', blank=True, null=True)

    class Meta:
        verbose_name = _("Cuisine")
        verbose_name_plural = _("Cuisines")

    def __str__(self):
        return self.title


class Photo(models.Model):
    PHOTO_TYPES = (
        ('food', 'Food'),
        ('drink', 'Drink'),
        ('interior', 'Interior'),
        ('exterior', 'Exterior'),
    )
    owner = models.ForeignKey("account.User", verbose_name=_("Owner"), on_delete=models.CASCADE, related_name='photo_owner')
    photo = models.ImageField(_("Company Photo"), upload_to='company-photos/')
    photo_url = models.URLField(_("Photo Url"), max_length=600)
    photo_type = models.CharField(_("type"), choices=PHOTO_TYPES ,max_length=50)

    class Meta:
        verbose_name = _("Photo")
        verbose_name_plural = _("Photos")

    def __str__(self):
        return str(self.photo)


class Menu(models.Model):
    company = models.ForeignKey("account.User", verbose_name=_("Company"), on_delete=models.CASCADE, related_name='menu')
    title = models.CharField(_("Title"), max_length=50)
    price = models.IntegerField(_("Price"))
    description = models.TextField(_("Description"))
    menu_type = models.ForeignKey("restaurant.MenuCategory", verbose_name=_("Type"), on_delete=models.CASCADE, related_name='menu')
    selected = models.BooleanField(_("Selected"), default=False)

    class Meta:
        verbose_name = _("Menu")
        verbose_name_plural = _("Menus")

    def __str__(self):
        return self.title


class MenuCategory(models.Model):
    title = models.CharField(_("Title"), max_length=50)

    class Meta:
        verbose_name = _("Menu Category")
        verbose_name_plural = _("Menu Categories")

    def __str__(self):
        return self.title

    
class Comment(models.Model):

    company = models.ForeignKey("restaurant.Company", verbose_name=_("Company"), on_delete=models.CASCADE, related_name='company_comment',blank=True, null=True)
    user = models.ForeignKey("account.User", verbose_name=_("User"), on_delete=models.CASCADE, related_name='user_comment')
    text = models.TextField(_("Comment Text"))
    commented_at = models.DateTimeField(_("Written Date"), auto_now_add=True)

    ratingFood = models.IntegerField(_("ratingFood"), blank=True, null=True)
    ratingService = models.IntegerField(_("ratingService"), blank=True, null=True)
    ratingAmbience = models.IntegerField(_("ratingAmbience"), blank=True, null=True)

    overall = models.IntegerField(_("Overall"))

    liked = models.IntegerField(_("Like"), blank=True, null=True)

    comment_image = models.ImageField(_("Comment Image"), upload_to='comment-images/', blank=True, null=True)    

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.text


class CommentImages(models.Model):

    comment = models.ForeignKey("restaurant.Comment", verbose_name=_("comment"), on_delete=models.CASCADE, related_name='comment_photos')
    photo = models.ImageField(_("Photo"), upload_to='comment-images/')    

    class Meta:
        verbose_name = _("CommentImages")
        verbose_name_plural = _("CommentImagess")

    def __str__(self):
        return self.comment



class Table(models.Model):
    TABLE_PLACES = (
        ('outside', 'Outside'),
        ('inside', 'Inside'),
    )

    company = models.ForeignKey("account.User", verbose_name=_("Company"), on_delete=models.CASCADE, related_name='company_table')
    size = models.IntegerField(_("Size"))
    table_place = models.CharField(_("Table Place"), max_length=50, choices=TABLE_PLACES)
    dates = models.ManyToManyField("restaurant.TableDate", verbose_name=_("Dates"), related_name='tables')
    
    class Meta:
        verbose_name = _("Table")
        verbose_name_plural = _("Tables")

    def __str__(self):
        return str(self.size)

    
class Time(models.Model):

    free_time = models.TimeField(_("Free Time"), auto_now=False, auto_now_add=False)
    reserved = models.BooleanField(_("Reserved"), default=False)

    class Meta:
        verbose_name = _("Time")
        verbose_name_plural = _("Times")

    def __str__(self):
        return str(self.reserved)


class TableDate(models.Model):

    date = models.DateField(_("Date"), blank=True, null=True)
    times = models.ManyToManyField("restaurant.Time", verbose_name=_("Time"), related_name='tableDates')

    class Meta:
        verbose_name = _("TableDate")
        verbose_name_plural = _("TableDates")

    def __str__(self):
        return str(self.date)

    
class Portion(models.Model):

    menu_id = models.IntegerField(_("Menu Id"))
    portion_count = models.IntegerField(_("Portion Count"))

    class Meta:
        verbose_name = _("Portion")
        verbose_name_plural = _("Portions")

    def __str__(self):  
        return str(self.menu_id)

    
class Reservation(models.Model):
    
    user = models.ForeignKey("account.User", verbose_name=_("User"), on_delete=models.CASCADE, related_name='reservation')
    company = models.ForeignKey("restaurant.Company", verbose_name=_("Company"), on_delete=models.CASCADE, related_name='reservation')
    table_id = models.IntegerField(_("Table Id"), null=True, blank=True)
    reserved_time = models.TimeField(_("Reserved Time"))
    reserved_date = models.DateField(_("Reserved Date"), blank=True, null=True)
    portions = models.ManyToManyField("restaurant.Portion", verbose_name=_("Portions"), related_name='reservation_portions')
    total_price = models.IntegerField(_("Total Price"), null=True, blank=True)
    accept = models.BooleanField(_("Accept"), default=False)
    denied = models.BooleanField(_("Denied"), default=False)
    reserved_at = models.DateField(_("Reserved at"), auto_now_add=True, blank=True, null=True)

    phone_number = models.CharField(_("Phone number"), max_length=50, blank=True, null=True)
    payment = models.BooleanField(_("Payment"), default=False)
    occasion = models.CharField(_("Occasion"), max_length=50, blank=True, null=True)
    special_request = models.TextField(_("Special Request"), blank=True, null=True)

    class Meta:
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")

    def __str__(self):
        return str(self.reserved_time)


class SavedRestaurant(models.Model):

    user = models.ForeignKey("account.User", verbose_name=_("User"), on_delete=models.CASCADE, related_name='saved_restaurants')
    company = models.ForeignKey("restaurant.Company", verbose_name=_("Company"), on_delete=models.CASCADE, related_name='saved_restaurants', blank=True, null=True)
    saved = models.BooleanField(_("Saved"),default=False)

    class Meta:
        verbose_name = _("SavedRestaurant")
        verbose_name_plural = _("SavedRestaurants")

    def __str__(self):
        return str(self.user)

    

class Notification(models.Model):

    NOTIFICATION_TYPES = (
        ('accept_reservation','Accepted Reservation'),
        ('new_reservation','New Reservation'),
    )

    sender = models.ForeignKey("account.User", verbose_name=_("Sender"), on_delete=models.CASCADE, related_name='sender_notification', blank=True, null=True)
    reciever = models.ForeignKey("account.User", verbose_name=_("Reciever"), on_delete=models.CASCADE, related_name='reciever_notification', blank=True, null=True)
    text = models.TextField(_("Text"))
    url = models.URLField(_("Url"), max_length=200, blank=True, null=True)    
    read = models.BooleanField(_("Read"), default=False)
    notified_at = models.DateTimeField(_("Notification date"), auto_now_add=True)
    notification_type = models.CharField(_("Notification type"), choices=NOTIFICATION_TYPES, max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    def __str__(self):
        return self.text

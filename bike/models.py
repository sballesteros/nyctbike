from django.db import models
import datetime

from django.contrib.auth.models import User

#to create tables:
##python manage.py validate
##python manage.py sqlall bike
##python manage.py syncdb ##<-create the tables

ACTIVATION_CHOICES = (
    ('A', 'Activated'),
    ('D', 'Desactivated')
    )

VOTE_CHOICES = (
    ('L', 'Like'),
    ('C', "Don't care"),
    ('D', "Don't like")
)

class VoteIt(models.Model):
    like = models.IntegerField() ##how many users like this idea
    dontlike = models.IntegerField()
    dontcare = models.IntegerField()
    
    activated = models.CharField(max_length=1, choices=ACTIVATION_CHOICES)

    nbsupports = models.IntegerField() ##number of support for the idea

    class Meta:
        abstract = True

class WhoDidThis(models.Model):
    creator = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_related")
    when = models.DateTimeField(auto_now_add=True) ##date of creation of the idea    

    def __unicode__(self):
        return "%s %s" % (self.creator, self.when)

    class Meta:
        abstract = True
        ordering = ['-when']


class Station(WhoDidThis, VoteIt):

    STATION_CHOICES = (
        ('H', 'Home'),
        ('W', 'Work'),
        ('O', 'Other')
        )

    ##spatial coordinates (cheesy way...)
    lat = models.FloatField()
    lon = models.FloatField()

    why = models.CharField(max_length=1, choices=STATION_CHOICES)
    comment = models.TextField() #justification of the user (my work, my home...)

    def __unicode__(self):
        return "%g %g" % (self.lat, self.lon)

class Idea(WhoDidThis, VoteIt):
    CATEGORY_CHOICES = (
        ('W', 'Website'),
        ('F', 'Inovative financing'),
        ('B', 'Bikes maintenance'),
        ('O', 'Other')
        )
    
    name = models.CharField(max_length=400)
    description = models.TextField()
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    
    def __unicode__(self):
        return "%s %s" % (self.name, self.description)



class Design(WhoDidThis, VoteIt):
    name = models.CharField(max_length=400)
    description = models.TextField()
    
    pict = models.ImageField(upload_to='pict/upload/')

    class Meta:
        abstract = True
        ordering = ['-when']

    def __unicode__(self):
        return "%s %s" % (self.name, self.description)


class DesignStation(Design):
    pass

class DesignBike(Design):
    pass




class VoteIdea(WhoDidThis):
    vote = models.CharField(max_length=1, choices=VOTE_CHOICES)
    which = models.ForeignKey(Idea)

    def __unicode__(self):
        return "%s" % (self.vote, self.which)
    
class VoteStation(WhoDidThis):
    vote = models.CharField(max_length=1, choices=VOTE_CHOICES)
    which = models.ForeignKey(Station)

    def __unicode__(self):
        return "%s" % (self.vote, self.which)

class VoteDesignStation(WhoDidThis):
    vote = models.CharField(max_length=1, choices=VOTE_CHOICES)
    which = models.ForeignKey(DesignStation)

    def __unicode__(self):
        return "%s" % (self.vote, self.which)

class VoteDesignBike(WhoDidThis):
    vote = models.CharField(max_length=1, choices=VOTE_CHOICES)
    which = models.ForeignKey(DesignBike)

    def __unicode__(self):
        return "%s" % (self.vote, self.which)



class Support(WhoDidThis):
    description = models.TextField()
    amount = models.FloatField()

    class Meta:
        abstract = True
        ordering = ['-when']

    def __unicode__(self):
        return "%s %s" % (self.description, self.supporter)


class SupportStation(Support):
    supported = models.ForeignKey(Station, related_name="%(app_label)s_%(class)s_related")

class SupportIdea(Support):
    supported = models.ForeignKey(Idea, related_name="%(app_label)s_%(class)s_related")

class SupportDesignBike(Support):
    supported = models.ForeignKey(DesignBike, related_name="%(app_label)s_%(class)s_related")

class SupportDesignStation(Support):
    supported = models.ForeignKey(DesignStation, related_name="%(app_label)s_%(class)s_related")


class News(WhoDidThis):
    title = models.CharField(max_length=400)
    content = models.TextField()


class UserProfile(models.Model):
#adapted from http://www.djangosnippets.org/snippets/494/
#using UN country and 3 char code list from http://unstats.un.org/unsd/methods/m49/m49alpha.htm
#correct as of 17th October 2008

    COUNTRY_CHOICES = (
        ('AFG', 'Afghanistan'), 
        ('ALA', 'Aland Islands'),
        ('ALB', 'Albania'),
        ('DZA', 'Algeria'),
        ('ASM', 'American Samoa'),
        ('AND', 'Andorra'),
        ('AGO', 'Angola'),
        ('AIA', 'Anguilla'),
        ('ATG', 'Antigua and Barbuda'),
        ('ARG', 'Argentina'),
        ('ARM', 'Armenia'),
        ('ABW', 'Aruba'),
        ('AUS', 'Australia'),
        ('AUT', 'Austria'),
        ('AZE', 'Azerbaijan'),
        ('BHS', 'Bahamas'),
        ('BHR', 'Bahrain'),
        ('BGD', 'Bangladesh'),
        ('BRB', 'Barbados'),
        ('BLR', 'Belarus'),
        ('BEL', 'Belgium'),
        ('BLZ', 'Belize'),
        ('BEN', 'Benin'),
        ('BMU', 'Bermuda'),
        ('BTN', 'Bhutan'),
        ('BOL', 'Bolivia'),
        ('BIH', 'Bosnia and Herzegovina'),
        ('BWA', 'Botswana'),
        ('BRA', 'Brazil'),
        ('VGB', 'British Virgin Islands'),
        ('BRN', 'Brunei Darussalam'),
        ('BGR', 'Bulgaria'),
        ('BFA', 'Burkina Faso'),
        ('BDI', 'Burundi'),
        ('KHM', 'Cambodia'),
        ('CMR', 'Cameroon'),
        ('CAN', 'Canada'),
        ('CPV', 'Cape Verde'),
        ('CYM', 'Cayman Islands'),
        ('CAF', 'Central African Republic'),
        ('TCD', 'Chad'),
        ('CIL', 'Channel Islands'),
        ('CHL', 'Chile'),
        ('CHN', 'China'),
        ('HKG', 'China - Hong Kong'),
        ('MAC', 'China - Macao'),
        ('COL', 'Colombia'),
        ('COM', 'Comoros'),
        ('COG', 'Congo'),
        ('COK', 'Cook Islands'),
        ('CRI', 'Costa Rica'),
        ('CIV', 'Cote d\'Ivoire'),
        ('HRV', 'Croatia'),
        ('CUB', 'Cuba'),
        ('CYP', 'Cyprus'),
        ('CZE', 'Czech Republic'),
        ('PRK', 'Democratic People\'s Republic of Korea'),
        ('COD', 'Democratic Republic of the Congo'),
        ('DNK', 'Denmark'),
        ('DJI', 'Djibouti'),
        ('DMA', 'Dominica'),
        ('DOM', 'Dominican Republic'),
        ('ECU', 'Ecuador'),
        ('EGY', 'Egypt'),
        ('SLV', 'El Salvador'),
        ('GNQ', 'Equatorial Guinea'),
        ('ERI', 'Eritrea'),
        ('EST', 'Estonia'),
        ('ETH', 'Ethiopia'),
        ('FRO', 'Faeroe Islands'),
        ('FLK', 'Falkland Islands (Malvinas)'),
        ('FJI', 'Fiji'),
        ('FIN', 'Finland'),
        ('FRA', 'France'),
        ('GUF', 'French Guiana'),
        ('PYF', 'French Polynesia'),
        ('GAB', 'Gabon'),
        ('GMB', 'Gambia'),
        ('GEO', 'Georgia'),
        ('DEU', 'Germany'),
        ('GHA', 'Ghana'),
        ('GIB', 'Gibraltar'),
        ('GRC', 'Greece'),
        ('GRL', 'Greenland'),
        ('GRD', 'Grenada'),
        ('GLP', 'Guadeloupe'),
        ('GUM', 'Guam'),
        ('GTM', 'Guatemala'),
        ('GGY', 'Guernsey'),
        ('GIN', 'Guinea'),
        ('GNB', 'Guinea-Bissau'),
        ('GUY', 'Guyana'),
        ('HTI', 'Haiti'),
        ('VAT', 'Holy See (Vatican City)'),
        ('HND', 'Honduras'),
        ('HUN', 'Hungary'),
        ('ISL', 'Iceland'),
        ('IND', 'India'),
        ('IDN', 'Indonesia'),
        ('IRN', 'Iran'),
        ('IRQ', 'Iraq'),
        ('IRL', 'Ireland'),
        ('IMN', 'Isle of Man'),
        ('ISR', 'Israel'),
        ('ITA', 'Italy'),
        ('JAM', 'Jamaica'),
        ('JPN', 'Japan'),
        ('JEY', 'Jersey'),
        ('JOR', 'Jordan'),
        ('KAZ', 'Kazakhstan'),
        ('KEN', 'Kenya'),
        ('KIR', 'Kiribati'),
        ('KWT', 'Kuwait'),
        ('KGZ', 'Kyrgyzstan'),
        ('LAO', 'Lao People\'s Democratic Republic'),
        ('LVA', 'Latvia'),
        ('LBN', 'Lebanon'),
        ('LSO', 'Lesotho'),
        ('LBR', 'Liberia'),
        ('LBY', 'Libyan Arab Jamahiriya'),
        ('LIE', 'Liechtenstein'),
        ('LTU', 'Lithuania'),
        ('LUX', 'Luxembourg'),
        ('MKD', 'Macedonia'),
        ('MDG', 'Madagascar'),
        ('MWI', 'Malawi'),
        ('MYS', 'Malaysia'),
        ('MDV', 'Maldives'),
        ('MLI', 'Mali'),
        ('MLT', 'Malta'),
        ('MHL', 'Marshall Islands'),
        ('MTQ', 'Martinique'),
        ('MRT', 'Mauritania'),
        ('MUS', 'Mauritius'),
        ('MYT', 'Mayotte'),
        ('MEX', 'Mexico'),
        ('FSM', 'Micronesia, Federated States of'),
        ('MCO', 'Monaco'),
        ('MNG', 'Mongolia'),
        ('MNE', 'Montenegro'),
        ('MSR', 'Montserrat'),
        ('MAR', 'Morocco'),
        ('MOZ', 'Mozambique'),
        ('MMR', 'Myanmar'),
        ('NAM', 'Namibia'),
        ('NRU', 'Nauru'),
        ('NPL', 'Nepal'),
        ('NLD', 'Netherlands'),
        ('ANT', 'Netherlands Antilles'),
        ('NCL', 'New Caledonia'),
        ('NZL', 'New Zealand'),
        ('NIC', 'Nicaragua'),
        ('NER', 'Niger'),
        ('NGA', 'Nigeria'),
        ('NIU', 'Niue'),
        ('NFK', 'Norfolk Island'),
        ('MNP', 'Northern Mariana Islands'),
        ('NOR', 'Norway'),
        ('PSE', 'Occupied Palestinian Territory'),
        ('OMN', 'Oman'),
        ('PAK', 'Pakistan'),
        ('PLW', 'Palau'),
        ('PAN', 'Panama'),
        ('PNG', 'Papua New Guinea'),
        ('PRY', 'Paraguay'),
        ('PER', 'Peru'),
        ('PHL', 'Philippines'),
        ('PCN', 'Pitcairn'),
        ('POL', 'Poland'),
        ('PRT', 'Portugal'),
        ('PRI', 'Puerto Rico'),
        ('QAT', 'Qatar'),
        ('KOR', 'Republic of Korea'),
        ('MDA', 'Republic of Moldova'),
        ('REU', 'Reunion'),
        ('ROU', 'Romania'),
        ('RUS', 'Russian Federation'),
        ('RWA', 'Rwanda'),
        ('BLM', 'Saint-Barthelemy'),
        ('SHN', 'Saint Helena'),
        ('KNA', 'Saint Kitts and Nevis'),
        ('LCA', 'Saint Lucia'),
        ('MAF', 'Saint-Martin (French part)'),
        ('SPM', 'Saint Pierre and Miquelon'),
        ('VCT', 'Saint Vincent and the Grenadines'),
        ('WSM', 'Samoa'),
        ('SMR', 'San Marino'),
        ('STP', 'Sao Tome and Principe'),
        ('SAU', 'Saudi Arabia'),
        ('SEN', 'Senegal'),
        ('SRB', 'Serbia'),
        ('SYC', 'Seychelles'),
        ('SLE', 'Sierra Leone'),
        ('SGP', 'Singapore'),
        ('SVK', 'Slovakia'),
        ('SVN', 'Slovenia'),
        ('SLB', 'Solomon Islands'),
        ('SOM', 'Somalia'),
        ('ZAF', 'South Africa'),
        ('ESP', 'Spain'),
        ('LKA', 'Sri Lanka'),
        ('SDN', 'Sudan'),
        ('SUR', 'Suriname'),
        ('SJM', 'Svalbard and Jan Mayen Islands'),
        ('SWZ', 'Swaziland'),
        ('SWE', 'Sweden'),
        ('CHE', 'Switzerland'),
        ('SYR', 'Syrian Arab Republic'),
        ('TJK', 'Tajikistan'),
        ('THA', 'Thailand'),
        ('TLS', 'Timor-Leste'),
        ('TGO', 'Togo'),
        ('TKL', 'Tokelau'),
        ('TON', 'Tonga'),
        ('TTO', 'Trinidad and Tobago'),
        ('TUN', 'Tunisia'),
        ('TUR', 'Turkey'),
        ('TKM', 'Turkmenistan'),
        ('TCA', 'Turks and Caicos Islands'),
        ('TUV', 'Tuvalu'),
        ('UGA', 'Uganda'),
        ('UKR', 'Ukraine'),
        ('ARE', 'United Arab Emirates'),
        ('GBR', 'United Kingdom'),
        ('TZA', 'United Republic of Tanzania'),
        ('USA', 'United States of America'),
        ('VIR', 'United States Virgin Islands'),
        ('URY', 'Uruguay'),
        ('UZB', 'Uzbekistan'),
        ('VUT', 'Vanuatu'),
        ('VEN', 'Venezuela (Bolivarian Republic of)'),
        ('VNM', 'Viet Nam'),
        ('WLF', 'Wallis and Futuna Islands'),
        ('ESH', 'Western Sahara'),
        ('YEM', 'Yemen'),
        ('ZMB', 'Zambia'),
        ('ZWE', 'Zimbabwe')
        )

    user = models.OneToOneField(User)
    country = models.CharField(max_length=3, choices=COUNTRY_CHOICES, blank=True)
    about = models.TextField() #about you

##    #Home and work address so that we can get lattitudes and longitudes of our users
##    homeaddress = models.CharField(max_length=100)
##    homecity = models.CharField(max_length=50)
##    homezip = models.CharField(max_length=20)
##    homecountry = models.CharField(max_length=30)
##
##    workaddress = models.CharField(max_length=100)
##    workcity = models.CharField(max_length=50)
##    workzip = models.CharField(max_length=20)
##    workcountry = models.CharField(max_length=30)
##
##    ##commuting informations
##    hasabike = models.BooleanField(max_length=30)
##    commute = models.CharField(max_length=20) ##type of commuting (subway, train (LIRR, NJ Transit, Amtrack), car, bus, other)

    def __unicode__(self):
        return "%s" % (self.country)



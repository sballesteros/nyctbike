from django import forms
from django.forms import ModelForm
from models import Support, Idea
import StringIO
from PIL import Image
from django.contrib.comments.forms import CommentForm


class IdeaForm(ModelForm):
    name = forms.CharField(label="Idea's title", max_length=400, widget=forms.TextInput(attrs={'size': 100}))
    description = forms.CharField(widget = forms.Textarea(attrs={'cols': 80, 'rows':40}))

    class Meta:
        model = Idea
        fields = ('name', 'description', 'category', )
        #exclude = ('creator', 'structure', )


class DesignForm(forms.Form):
    title = forms.CharField(max_length=400,  widget=forms.TextInput(attrs={'size': 100}))
    image = forms.ImageField(help_text='Image to illustrate your desigm (size <1MB and width and height < 800*800px)', required=True)
    description = forms.CharField(widget = forms.Textarea(attrs={'cols': 80, 'rows':20}))

#    license_name = forms.CharField(label='License', max_length=400, initial='CC BY-SA 3.0')

    #custom validation as to be named with 'clean' '_' 'field_name_to_validate'
    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image._size > 1*1024*1024:
                raise forms.ValidationError('Picture file too large ( > 1MB)')
            else:
                str=""
                for c in image.chunks():
                    str += c

                imagefile = StringIO.StringIO(str)
                myimage = Image.open(imagefile)
                width, height = myimage.size[0], myimage.size[1]
                if width > 800 or height > 800:
                    raise forms.ValidationError('size is {0}*{1} and max dim allowed are: 800*800 pixels'.format(width, height))

        return image



class StationForm(forms.Form):
    STATION_CHOICES = (
        ('H', 'Home'),
        ('W', 'Work'),
        ('O', 'Other')
        )

    latitude = forms.FloatField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    longitude = forms.FloatField(widget = forms.TextInput(attrs={'readonly':'readonly'}))

    why = forms.ChoiceField(widget=forms.widgets.RadioSelect, choices=STATION_CHOICES)

    comment = forms.CharField(widget = forms.Textarea)



class ProfileForm(forms.Form):
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


    ##belongs to User model
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email =  forms.EmailField(required=True,  widget=forms.TextInput(attrs={'size':'40'}))

    ##belongs to UserProfile model
    country = forms.ChoiceField(required=True, choices=COUNTRY_CHOICES)

    about = forms.CharField(required=True, widget = forms.Textarea(attrs={'cols': 60, 'rows':15}))

##to the form from the model!
##class SupportForm(ModelForm):
##    class Meta:
##        model = Support


class SupportForm(forms.Form):
    description = forms.CharField(widget = forms.Textarea, help_text='Why do you support this idea? What do you expect from it?')
    amount = forms.FloatField(label='Amount (US$)', widget = forms.TextInput)

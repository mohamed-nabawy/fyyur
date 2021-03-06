from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, ValidationError
from wtforms.validators import DataRequired, AnyOf, URL, Length
from enum import Enum
import re

class StateEnum(Enum):
    AL = 'AL'
    AK = 'AK'
    AZ = 'AZ'
    AR = 'AR'
    CA = 'CA'
    CO = 'CO'
    CT = 'CT'
    DE = 'DE'
    DC = 'DC'
    FL = 'FL'
    GA = 'GA'
    HI = 'HI'
    ID = 'ID'
    IL = 'IL'
    IN = 'IN' 
    IA = 'IA'
    KS = 'KS'
    KY = 'KY'
    LA = 'LA'
    ME = 'ME'
    MT = 'MT'
    NE = 'NE'
    NV = 'NV'
    NH = 'NH'
    NJ = 'NJ'
    NM = 'NM'
    NY = 'NY'
    NC = 'NC'
    ND = 'ND'
    OH = 'OH'
    OK = 'OK'
    OR = 'OR'
    MD = 'MD'
    MA = 'MA'
    MI = 'MI'
    MN = 'MN'
    MS = 'MS'
    MO = 'MO'
    PA = 'PA'
    RI = 'RI'
    SC = 'SC'
    SD = 'SD'
    TN = 'TN'
    TX = 'TX'
    UT = 'UT'
    VT = 'VT'
    VA = 'VA'
    WA = 'WA'
    WV = 'WV'
    WI = 'WI'
    WY = 'WY'

    @classmethod
    def choices(cls):
        return [(choice, choice.name) for choice in cls]

    @classmethod
    def coerce(cls, item):
        return cls(str(item)) if not isinstance(item, cls) else item

    def __str__(self):
        return str(self.value)

class GenresEnum(Enum):
    Alternative = 'Alternative'
    Blues = 'Blues'
    Classical = 'Classical'
    Country = 'Country'
    Electronic = 'Electronic'
    Folk = 'Folk'
    Funk = 'Funk'
    Hip_Hop = 'Hip-Hop'
    Heavy_Metal = 'Heavy Metal'
    Instrumental = 'Instrumental'
    Jazz = 'Jazz'
    Musical_Theatre = 'Musical Theatre'
    Pop = 'Pop'
    Punk = 'Punk'
    R_B = 'R&B'
    Reggae = 'Reggae'
    Rock_n_Roll = 'Rock n Roll'
    Soul = 'Soul'
    Other = 'Other'
    
    @classmethod
    def choices(cls):
        return [(choice, choice.name) for choice in cls]

    @classmethod
    def coerce(cls, item):
        return cls(str(item)) if not isinstance(item, cls) else item.value

    def __str__(self):
        return str(self.value)

def validate_phone(form, field):
        if not field.data:
            return

        if not re.search(r"^[0-9]+-[0-9]+-[0-9]+$", field.data):
            raise ValidationError("Invalid Phone number")

class ShowForm(Form):
    artist_id = StringField(
        'artist_id', validators=[DataRequired()]
    )
    venue_id = StringField(
        'venue_id', validators=[DataRequired()]
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=StateEnum.choices(),
        coerce = StateEnum.coerce
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[validate_phone, Length(max=15, message="must be lower than 15 chars")]
    )
    image_link = StringField(
        'image_link', validators=[URL(), Length(max=500, message="must be lower than 500 chars")]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=GenresEnum.choices(),
        coerce=GenresEnum.coerce
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL(), Length(max=500, message="must be lower than 500 chars")]
    )
    website = StringField(
        'website', validators=[URL(), Length(max=500, message="must be lower than 500 chars")]
    )
    seeking_talent = SelectField(
        'seeking_talent', choices=[('No', 'No'), ('Yes', 'Yes')]
    )
    seeking_description = StringField(
        'seeking_description', validators=[Length(max=120, message="must be lower than 120 chars")]
    )

class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=StateEnum.choices(),
        coerce = StateEnum.coerce
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone', validators=[validate_phone, Length(max=15, message="must be lower than 15 chars")]
    )
    image_link = StringField(
        'image_link', validators=[URL(), Length(max=500, message="must be lower than 500 chars")]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
         choices=GenresEnum.choices(),
        coerce=GenresEnum.coerce
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL(), Length(max=500, message="must be lower than 500 chars")]
    )
    website = StringField(
        'website', validators=[URL(), Length(max=500, message="must be lower than 500 chars")]
    )
    seeking_venue = SelectField(
        'seeking_venue', choices=[('No', 'No'), ('Yes', 'Yes')]
    )
    seeking_description = StringField(
        'seeking_description', validators=[Length(max=120, message="must be lower than 120 chars")]
    )

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM

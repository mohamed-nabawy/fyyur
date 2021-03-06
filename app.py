#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import date

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
Migrate(app, db)
# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(500), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    seeking_talent = db.Column(db.Boolean(), nullable=False)
    website = db.Column(db.String(500), nullable=False)
    #one to many: venue has many shows
    shows = db.relationship('Show', backref='Venue', lazy='dynamic')
    _phone = db.relationship('VenuePhone', backref='Venue', lazy='dynamic')
    _seeking_description = db.relationship('VenueSeekingDescription', backref='Venue', lazy='dynamic')
    @property
    def phone(self):
       return self._phone.first().phone
    @property
    def seeking_description(self):
       return self._seeking_description.first().seeking_description   
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    def __init__(self, name, city, state, address, genres, image_link, facebook_link, seeking_talent, website):
      self.name = name.title()
      self.city = city
      self.state = state
      self.address = address
      self.genres = genres
      self.image_link = image_link
      self.facebook_link = facebook_link
      self.seeking_talent = seeking_talent
      self.website = website

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(500), nullable=False)
    seeking_venue = db.Column(db.Boolean(), nullable=False)
    website = db.Column(db.String(500), nullable=False)
     # one to many: artist may have many shows
    shows = db.relationship('Show', backref='Artist', lazy='dynamic')
    _phone = db.relationship('ArtistPhone', backref='Artist', lazy='dynamic')
    @property
    def phone(self):
       return self._phone.first().phone

    _seeking_description = db.relationship('ArtistSeekingDescription', backref='Artist', lazy='dynamic')
    @property
    def seeking_description(self):
       return self._seeking_description.first().seeking_description
       
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    def __init__(self, name, city, state, genres, image_link, facebook_link, seeking_venue, website):
      self.name = name.title()
      self.city = city
      self.state = state
      self.genres = genres
      self.image_link = image_link
      self.facebook_link = facebook_link
      self.seeking_venue = seeking_venue
      self.website = website

class ArtistPhone(db.Model):
    __tablename__ = 'artist_phone'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    def __init__(self, phone, artist_id):
      self.artist_id = artist_id
      self.phone = phone

class ArtistSeekingDescription(db.Model):
    __tablename__ = 'artist_seeking_description'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    seeking_description = db.Column(db.String(120), nullable=False)
    def __init__(self, seeking_description, artist_id):
      self.artist_id = artist_id
      self.seeking_description = seeking_description

class VenuePhone(db.Model):
    __tablename__ = 'venue_phone'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    def __init__(self, phone, venue_id):
      self.venue_id = venue_id
      self.phone = phone

class VenueSeekingDescription(db.Model):
    __tablename__ = 'venue_seeking_description'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    seeking_description = db.Column(db.String(120), nullable=False)
    def __init__(self, seeking_description, venue_id):
      self.venue_id = venue_id
      self.seeking_description = seeking_description


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    start_time = db.Column(db.DateTime(), nullable=False)
    artist = db.relationship('Artist', backref='Show', uselist=False)
    venue = db.relationship('Venue', backref='Show', uselist=False)
    def __init__(self, artist_id, venue_id, start_time):
      self.artist_id = artist_id
      self.venue_id = venue_id
      self.start_time = start_time

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  venues = Venue.query.all()
  # group venues by city and state
  response = []
  cities_states = []
  now = datetime.now()
  for venue in venues:
    # adding a num_upcoming_shows property to the each venue in the list
    venue.num_upcoming_shows = len(venue.shows.filter(Show.start_time > now).all())
    if((venue.city, venue.state) not in cities_states):
      cities_states.append((venue.city, venue.state))
      response.append({"city": venue.city, "state": venue.state, "venues": [venue]})
    else:
      for venues_obj in response:
        if(venues_obj["city"] == venue.city and venues_obj["state"] == venue.state):
          venues_obj["venues"].append(venue)

  return render_template('pages/venues.html', areas=response)

def toJSON(obj):
  return {"id":obj.id, "name":obj.name, "num_upcoming_shows": 0}
            
@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form["search_term"]
  if(not search_term.strip()):
    response = {
      "count": 0,
      "data": []
    }
  else:
    venues = Venue.query.filter(Venue.name.ilike("%"+search_term.strip()+"%")).all()
    results = []
    for venue in venues:
      results.append(toJSON(venue))
    response = {
      "count":len(results),
      "data": results
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  try:
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    data = Venue.query.get(venue_id)
    if(data is None):
      flash('Venue does not exists!')
      return redirect(url_for("venues"))
    data.genres = data.genres.split(",")
    now = datetime.now()
    # preparing past shows
    data.past_shows = []
    past_shows = data.shows.filter(Show.start_time < now)
    for show in past_shows:
      data.past_shows.append({
      "artist_id": show.artist.id,
      "artist_name":  show.artist.name,
      "artist_image_link":  show.artist.image_link,
      "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      })
    data.past_shows_count = len(data.past_shows)

    # preparing upcoming shows
    data.upcoming_shows = []
    upcoming_shows = data.shows.filter(Show.start_time > now)
    for show in upcoming_shows:
      data.upcoming_shows.append({
      "artist_id": show.artist.id,
      "artist_name":  show.artist.name,
      "artist_image_link":  show.artist.image_link,
      "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      })
    data.upcoming_shows_count =  len(data.upcoming_shows)
    return render_template('pages/show_venue.html', venue=data)
  except:
    db.session.rollback()
    flash('An error occurred.')
    return redirect(url_for("venues"))
  finally:
    db.session.close()

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  try:
    form = VenueForm(request.form)
    # check form validation
    if form.validate() == False:
      form.genres.data = ",".join([choice.value for choice in form.genres.data])
      return render_template("forms/new_venue.html", form=form)
    name = form.name.data
    city = form.city.data
    state = str(form.state.data)
    address = form.address.data
    phone = form.phone.data
    genres = ",".join([choice.value for choice in form.genres.data])
    image_link = form.image_link.data
    facebook_link = form.facebook_link.data
    website = form.website.data
    seeking_talent = False if form.seeking_talent.data == "No" else True
    seeking_description = form.seeking_description.data
    new_venue = Venue(name, city, state, address, genres, image_link, facebook_link, seeking_talent, website)
    db.session.add(new_venue)
    db.session.commit()
    #adding phone if exists
    if phone:
      new_phone = VenuePhone(phone, new_venue.id)
      db.session.add(new_phone)
      #adding seeking description if exists
    if seeking_description:
      new_seeking_description = VenueSeekingDescription(seeking_description, new_venue.id)
      db.session.add(new_seeking_description)

    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
  # TODO: on unsuccessful db insert, flash an error instead.
    db.session.rollback()
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  finally:
    db.session.close()
    return redirect(url_for("venues"))

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    #remove any rows in other tables that refrence this row i.e. show, venue_phone or venue_seeking_description
    venue_phone = VenuePhone.query.filter_by(venue_id=venue_id)
    db.session.delete(venue_phone)
    venue_seeking_description = VenueSeekingDescription.query.filter_by(venue_id=venue_id)
    show = Show.query.filter_by(venue_id=venue_id)
    db.session.delete(venue_phone)
    db.session.delete(venue_seeking_description)
    db.session.delete(show)
    venue = Venue.query.get(venue_id)
    #remove referencing tables rows first
    db.session.delete(venue)
    db.session.commit()
    flash('Venue was successfully deleted!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue could not be deleted.')
  finally:
    db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for("venues"))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form["search_term"]
  if(not search_term.strip()):
    response = {
      "count": 0,
      "data": []
    }
  else:
    artists = Artist.query.filter(Artist.name.ilike("%"+search_term.strip()+"%")).all()
    results = []
    for artist in artists:
      results.append(toJSON(artist))
    response = {
      "count":len(results),
      "data": results
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  try:
    data = Artist.query.get(artist_id)
    if(data is None):
      flash('Artist does not exists!')
      return redirect(url_for("artists"))
    # preparing genres for view
    data.genres = data.genres.split(",")
    now = datetime.now()
    # preparing past shows
    data.past_shows = []
    past_shows = data.shows.filter(Show.start_time < now)
    for show in past_shows:
      data.past_shows.append({"venue_id": show.venue.id,
      "venue_name":  show.venue.name,
      "venue_image_link":  show.venue.image_link,
      "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      })
    data.past_shows_count = len(data.past_shows)

    # preparing upcoming shows
    data.upcoming_shows = []
    upcoming_shows = data.shows.filter(Show.start_time > now)
    for show in upcoming_shows:
      data.upcoming_shows.append({"venue_id": show.venue.id,
      "venue_name":  show.venue.name,
      "venue_image_link":  show.venue.image_link,
      "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
      })
    data.upcoming_shows_count = len(data.upcoming_shows)
    return render_template('pages/show_artist.html', artist=data)
  except:
    db.session.rollback()
    flash('An error occurred.')
    return redirect(url_for("artists"))
  finally:
    db.session.close()
    
#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  artist.seeking_description
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  try:
    form = ArtistForm(request.form)
    # check form validation
    artist = Artist.query.get(artist_id)
    artist.name = form.name.data
    artist.city = form.city.data
    artist.state = str(form.state.data)
    artist.genres = ",".join([choice.value for choice in form.genres.data])
    artist.image_link = form.image_link.data
    artist.facebook_link = form.facebook_link.data
    artist.seeking_venue = False if form.seeking_venue.data == "No" else True
    artist.website = form.website.data

    if form.validate() == False:
      return render_template("forms/edit_artist.html", form=form, artist=artist)
    # check if form submission has a phone
    if  form.phone.data:
      old_phone = ArtistPhone.query.filter_by(artist_id =artist_id).first()
    # check if artist has an old phone to update else create a new one
      if old_phone:
        db.session.query(ArtistPhone).filter_by(artist_id = artist_id).update({ArtistPhone.phone:form.phone.data})
      else:
        new_phone = ArtistPhone(form.phone.data, artist.id)
        db.session.add(new_phone)
    # check if form submission has a phone
    if  form.seeking_description.data:
      old_seeking_description = ArtistSeekingDescription.query.filter_by(artist_id =artist_id).first()
    # check if artist has an old phone to update else create a new one
      if old_seeking_description:
        db.session.query(ArtistSeekingDescription).filter_by(artist_id = artist_id).update({ArtistSeekingDescription.seeking_description:form.seeking_description.data})
      else:
        new_seeking_description = ArtistSeekingDescription(form.seeking_description.data, artist.id)
        db.session.add(new_seeking_description)

    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
  except:
  # # TODO: on unsuccessful db insert, flash an error instead.
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
  finally:
    db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  try:
    form = VenueForm(request.form)
    venue = Venue.query.get(venue_id)
    venue.name = form.name.data
    venue.city = form.city.data
    venue.state = str(form.state.data)
    venue.address = form.address.data
    venue.genres = ",".join([choice.value for choice in form.genres.data])
    venue.image_link = form.image_link.data
    venue.facebook_link = form.facebook_link.data
    venue.seeking_talent = False if form.seeking_talent.data == "No" else True
    venue.website = form.website.data
    # check form validation
    if form.validate() == False:
      return render_template("forms/edit_venue.html", form=form, venue=venue)
      
    if form.phone.data:
      old_phone = VenuePhone.query.filter_by(venue_id = venue_id).first()
      # check if artist has an old phone to update else create a new one
      if old_phone:
        db.session.query(VenuePhone).filter_by(venue_id = venue_id).update({VenuePhone.phone:form.phone.data})
      else:
        new_phone = VenuePhone(form.phone.data, venue.id)
        db.session.add(new_phone)
        
    if form.seeking_description.data:
      old_seeking_description = VenueSeekingDescription.query.filter_by(venue_id = venue_id).first()
      # check if artist has an old seeking description to update else create a new one
      if old_seeking_description:
        db.session.query(VenueSeekingDescription).filter_by(venue_id = venue_id).update({VenueSeekingDescription.website:form.website.data})
      else:
        new_seeking_description = VenueSeekingDescription(form.seeking_description.data, venue.id)
        db.session.add(new_seeking_description)

    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
  except:
  # TODO: on unsuccessful db insert, flash an error instead.
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
  finally:  
    db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  try:
    form = ArtistForm(request.form)
    # check form validation
    if form.validate() == False:
      form.genres.data = ",".join([choice.value for choice in form.genres.data])
      return render_template("forms/new_artist.html", form=form)

    name = form.name.data
    city = form.city.data
    state = str(form.state.data)
    phone = form.phone.data
    genres = ",".join([choice.value for choice in form.genres.data])
    image_link = form.image_link.data
    facebook_link = form.facebook_link.data
    website = form.website.data
    seeking_venue = False if form.seeking_venue.data == "No" else True
    seeking_description = form.seeking_description.data
    new_artist = Artist(name, city, state, genres, image_link, facebook_link, seeking_venue, website)
    db.session.add(new_artist)
    db.session.commit()
    if phone:
      new_phone = ArtistPhone(phone, new_artist.id)
      db.session.add(new_phone)
    if seeking_description:
      new_seeking_description = ArtistSeekingDescription(seeking_description, new_artist.id)
      db.session.add(new_seeking_description)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
  # TODO: on unsuccessful db insert, flash an error instead.
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
    return redirect(url_for('artists'))

#  Shows
#  ----------------------------------------------------------------
@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real shows data.
  # preparing real data shows for view
  shows = []
  data = Show.query.all()
  for show in data:
    shows.append({
    "venue_id": show.venue.id,
    "venue_name": show.venue.name,
    "artist_id": show.artist.id,
    "artist_name": show.artist.name,
    "artist_image_link": show.artist.image_link,
    "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M:%S")})
  return render_template('pages/shows.html', shows=shows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  try:
    form = ShowForm(request.form)
    # check form validation
    if form.validate() == False:
      return render_template("forms/new_show.html", form=form)
    artist_id = form.artist_id.data
    venue_id = form.venue_id.data
    start_time = form.start_time.data
    artist = Artist.query.get(artist_id)
    #check if entities exists first for data integrity
    if artist is None:
      flash('Artist does not exists!')
    venue = Venue.query.get(venue_id)
    if venue is None:
      flash('Venue does not exists!')
    if(artist is None or venue is None):
      return render_template("forms/new_show.html", form=form)
    
    new_show = Show(artist_id, venue_id, start_time)
    db.session.add(new_show)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
  # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

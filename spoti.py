#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, render_template, jsonify

# Spotify API wrapper, documentation here: http://spotipy.readthedocs.io/en/latest/
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# Authenticate with Spotify using the Client Credentials flow
with open("credentials.txt", "r") as file:
    client_id = file.readline().split()[0]
    client_secret = file.readline().split()[0]

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def homepage():
    # Displays homepage
    return render_template('main.html')

@app.route('/new_releases', methods=['GET'])
def new_releases():

    # Use the country from the query parameters, if provided
    if 'country' in request.args:
        country = request.args['country']
    else:
        country = 'SE'

    # Send request to the Spotify API
    new_releases = sp.new_releases(country=country, limit=20, offset=0)

    # Return the list of new releases
    return jsonify(new_releases)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

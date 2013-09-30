#!/bin/bash --login
# Installs common packages and libraries for a base ami

# To use this script you must do the following:
#  1. Run as the user lt3 (sudo su lt3)
#  2. Create .virtualenvs/2.6 .virtualenvs/2.7 in ~ (for lt3)
#  3. Use rvm to install ruby 1.9.3 and 2.0.0

set -e
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y ruby-dev python-dev libzmq-dev mongodb mongodb-server libsqlite3-dev libjpeg-dev libjpeg8-dev libfreetype6-dev libpng-dev zlib1g-dev libxslt-dev libxml2-dev libmysqlclient-dev libyaml-dev
sudo apt-get install -y gfortran libopenblas-dev liblapack-dev libffi-dev

for PY_VERSION in '2.6' '2.7'
do
        source /home/lt3/.virtualenvs/$PY_VERSION/bin/activate
        pip install --upgrade pip
        pip install --upgrade numpy
        pip install --upgrade scipy
        pip install --upgrade pyzmq pymongo pysqlite MySQL-python pillow amqp pycrypto kombu librabbitmq msgpack-python boto simplejson redis argparse psycopg2 matplotlib mechanize sqlalchemy httplib2 momoko toro jsonschema motor lxml jsonpickle plac selenium sphinx nose python-dateutil nose-cov chai billiard paramiko requests beautifulsoup4 pyyaml cffi tox docutils mock rsa httpretty
        pip install --upgrade twisted gevent gunicorn eventlet tornado django flask jinja2 celery Werkzeug
        pip install --upgrade ipython cython
done

rvm get stable --auto-dotfiles
rvm install 1.9.3
rvm install 2.0.0
for RB_VERSION in '1.9.3' '2.0.0'
do
        rvm use $RB_VERSION
        gem update --system
        gem install --no-ri --no-rdoc rdoc rake tzinfo bundler 
        gem install --no-ri --no-rdoc httparty colored tinder hipchat d3_rails jruby-openssl celluloid-io grape grape-entity stamp enumerize kaminari haml-rails carrierwave fog seed-fu acts-as-taggable-on nokogiri slim redcarpet haml uglifier handlebars_assets jquery-rails foreman
        gem install --no-ri --no-rdoc mysql2 pg sqlite3 mongoid redis cache
        gem install --no-ri --no-rdoc rails unicorn slim sinatra sidekiq eventmachine
        gem install --no-ri --no-rdoc omniauth omniauth-google-oauth2 omniauth-twitter omniauth-github omniauth-facebook omniauth-openid omniauth-wordpress twitter rails_admin stripe stripe_event
        gem install --no-ri --no-rdoc multi_fetch_fragments activerecord-import activerecord activeresource
        gem install --no-ri --no-rdoc coveralls rspec-rails spinach-rails capybara pry database_cleaner launchy minitest ffaker guard guard-rspec guard-spinach poltergeist spork jasmine simplecov shoulda-matchers webmock test_after_commit webrat mocha insist parallel_tests selenium-webdriver cucumber-rails cucumber
        gem install --no-ri --no-rdoc mini_portile highline rest daemons polyglot atomic treetop diff execjs actionmailer activesupport ffi multi_json activemodel script tilt arel json test sprockets formatador journey mime mail i18n erubis types sass ssl hike builder thor actionpack rack
done

# The task

Coding-challange
--------------

Create a service that shows the user hotels near a specific location on a map.

The task is designed to assess your interest and experience. We want to see your code, your approach, and your talent.

To get the places, we recommend using the [HERE Places API](https://developer.here.com/documentation/places/dev_guide/topics/quick-start-find-text-string.html) although you can use a different places service if you wish (e.g. Google or Foursquare).

Technical spec
--------------

The architecture will be split between a back-end and a web front-end, for
instance providing a JSON in/out RESTful API. Feel free to use any other
technologies provided that respects the client/service architecture.

Choose **one** of the following technical tasks that best suits your role:

1. **Back-end**: write, document and test your API as if it will be used by other
   services. Include a minimal front-end (e.g. a static view) and an API
   docs. 
2. **Front-end**: focus on making the interface as polished as possible (e.g. hotel cards, map, list view). Include a minimal back-end, or use the `Here API` service
   directly. 
3. **Full-stack**: include both front-end and back-end tasks.


### Back-end

We assume that you will use the web framework that will best meet the challenge requirements (JS or Python are a plus).

Here are some technologies we are more familiar with:

* JavaScript
* Python
* C#
* PostgreSQL

Choosing the right endpoints design is part of the task evaluation.

### Front-end

The front-end should ideally be a single page app.
Please **do not use** any UI frameworks (e.g. Boostrap or Material Design)
You may take this opportunity to demonstrate your CSS or HTML knowledge.

We are more familiar with:

* React or Angular
* TypeScript

Host it
--------

When you’re done, host it somewhere (e.g. on Amazon EC2, Heroku..) and send us the git repo link giving also clear instructions about making it work locally.

What we're looking for
--------

In your app we'll be looking for:

- Completeness of solution - does the app work as per the requirements?
- Quality of code - is your code clean & well written?
- User interface - does the page look ok, does it look broken?
- Tests - What should be tested?

If you can't complete your app, give us a description of what you were planning / how you would approach it.

Final words
--------

We're interested in your feedback, so do let us know what you thought of the task. Good​ ​luck​ ​and​ ​feel​ ​free​ ​to​ ​ask​ ​if​ ​there​ ​are​ ​any​ ​questions: [devs@limehome.de](mailto:devs@limehome.de)

# The solution

I am full-stack engineer, but have much more experience with backend and Django.

When I read the task I think that small API-proxy service is enough.
And as for me asynchronous web-servers can handle such tasks with more performance, compared to Django or Flask.

That's why I implemented simple `apiproxy` script that just uses HERE Maps API.

However I wanted to show more of my skills working with `django`, `django-rest-framework` and `PostGIS`. And so I created 2nd version of backend - `apistored`. It uses the same HERE API, but stores hotels in local DB.

## Run instructions

### API proxy

This repo uses `Pipenv` to manage requirements and virtual environment. You should install [pipenv](https://pipenv.kennethreitz.org/en/latest/) before installing python packages.

I used `python 3.6.3`, so any later version will work. `3.5` will not work as `f`-strings are used in project.

Also note that there is single `Pipfile` to handle both `aiohttp` and `django` versions of backend.

#### Getting started

1. Install dependencies with `pipenv install --dev`
1. Create `.env` file at root of the repo
1. Add 2 variables for Here API - `LH_MAPS_APP_ID` and `LH_MAPS_APP_CODE`. Check [Here guide](https://developer.here.com/documentation/places/dev_guide/common/credentials.html) on how to get credentials
1. Run `pipenv run apiproxy`

### API Stored

For `django` based version you need a little more of preparations.

You need to install geospatial libraries first.

You can consult Django's doc about [Installing Geo Django](https://docs.djangoproject.com/en/3.0/ref/contrib/gis/install/#installation) and [Installing geo libraries](https://docs.djangoproject.com/en/3.0/ref/contrib/gis/install/geolibs/).

At minimum you need to set `GDAL_DATA` env variable to correct path. And also `gdal/bin` should be in your `PATH` variable.

Also you need Redis to run celery and PostGIS to run DB. If you use docker you can run both with `docker-compose up -d`

After this you can do

1. `pipenv install --dev`
1. Activate virtual env with `pipenv shell`
1. `cd apistored`
1. `python manage.py migrate`
1. `python manage.py runserver 8080`

If you need celery, you can activate another `pipenv shell` in 2nd terminal window, navigate to `cd apistored` and run `celery worker -A apistored`. **Note** on Windows you should also add `--pool=solo`.

Things I would do if I want to prepare this for production:

1. `runserver` is not production ready, so I will use `uwsgi`
1. Nginx front

### Hotelmap

Frontend application build on react. You should have node installed.

I worked on `node` 11 and `npm` 6.

This code is built on top of `react-script`.

You should run `npm install` and after it you can use

`npm start` to run dev server on `localhost:3000` with hot-reload.
Please note that this server proxies api calls to `localhost:8080`. So you should run `apiproxy` or `apistored` side-by-side with this server

`npm run build` to build files under `build` folder, ready for production.


Some things I'd implement for bigger project:

* Use SCSS
* Use Redux or Context if project get's bigger (deeper nesting of components)
* There is a terrible fix for `here-maps-react` to handle markers update. I would like to similar apps, maybe some of them will perform better.
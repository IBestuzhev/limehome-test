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
# Understanding and Using the App


### Overview
included file

app overview, source code


### Using the App

1. First Test - Hello
   As a simple test that the app has been successfully deployed and is started go to its "hello" page. The URL is `http://yourAppName.eu-gb.mybluemix.net/hello` if you deployed to the London/EU-GB data center or `http://yourAppName.mybluemix.net/hello` for the US-SOUTH/NG data center. You should see the following as response.

   ```
   Hello folks, this is Python with Flask on Bluemix!
   ```
   
   The output corresponds with what we have in the [app](webclient/readapp.py) itself. When the path `/hello` is visited, the Flask framework directs the request to the code path for the "hello" route and executes the given code:

   ```
   # Simple route to test the app. It does not use a template, just returns a string.
   @app.route('/hello')
   def hello():
       return "Hello folks, this is Python with Flask on Bluemix!"
   ```


2. Initialize
   Based on the configuration the app knows where the database is located and which database system is going to be used. As you remember, we didn't create any tables or inserted any data yet. We are going to do this as part of the initialization. Instead of `/hello` we are now going to use the `/init` path. In the app first all tables related to the model are dropped (if existing), then created. When done, a short message with a link to the index page is returned. Dropping existing tables is useful when the schema is changed as part of testing or code extensions. 

   ```
   # This is a "secret" init page that can be called to initialize an empty database
   # with our "readlist" table. The table structure is defined above through the model.
   @app.route('/init')
   def init():
	   db.drop_all()
	   db.create_all()
	   return 'ok, go to <a href="/">home</a>'
   ```


3. Index Page

4. Adding an Entry

### Closing Remarks
Go back to the [overview document](README.md).

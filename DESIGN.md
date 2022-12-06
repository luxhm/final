### Understanding

#### `app.py`

Open up `app.py`. Atop the file are a bunch of imports, among them CS50's SQL module and a few helper functions. More on those soon.

After configuring [Flask](http://flask.pocoo.org/), notice how this file disables caching of responses (provided you're in debugging mode, which you are by default in your code50 codespace), lest you make a change to some file but your browser not notice. It then further configures Flask to store [sessions](https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions) on the local filesystem (i.e., disk) as opposed to storing them inside of (digitally signed) cookies, which is Flask's default. The file then configures CS50's SQL module to use `app.db`.

Thereafter are a whole bunch of routes, only two of which are fully implemented: `login` and `logout`. Read through the implementation of `login` first. Notice how it uses `db.execute` (from CS50's library) to query `finance.db`. And notice how it uses `check_password_hash` to compare hashes of users' passwords. Also notice how `login` "remembers" that a user is logged in by storing his or her `user_id`, an INTEGER, in `session`. That way, any of this file's routes can check which user, if any, is logged in. Finally, notice how once the user has successfully logged in, `login` will redirect to `"/"`, taking the user to their home page.  Meanwhile, notice how `logout` simply clears `session`, effectively logging a user out.

Notice how most routes are "decorated" with `@login_required` (a function defined in `helpers.py` too). That decorator ensures that, if a user tries to visit any of those routes, he or she will first be redirected to `login` so as to log in.

Notice too how most routes support GET and POST. Even so, most of them (for now!) simply return an "apology," since they're not yet implemented.

#### `helpers.py`

Next take a look at `helpers.py`. Ah, there's the implementation of `apology`. Notice how it ultimately renders a template, `apology.html`. It also happens to define within itself another function, `escape`, that it simply uses to replace special characters in apologies. By defining `escape` inside of `apology`, we've scoped the former to the latter alone; no other functions will be able (or need) to call it.

Next in the file is `login_required`. No worries if this one's a bit cryptic, but if you've ever wondered how a function can return another function, here's an example!

#### `requirements.txt`

Next take a quick look at `requirements.txt`. That file simply prescribes the packages on which this app will depend.

#### `templates/`

Now look in `templates/`. In `login.html` is, essentially, just an HTML form, stylized with [Bootstrap](http://getbootstrap.com/). In `apology.html`, meanwhile, is a template for an apology. Recall that `apology` in `helpers.py` took two arguments: `message`, which was passed to `render_template` as the value of `bottom`, and, optionally, `code`, which was passed to `render_template` as the value of `top`. Notice in `apology.html` how those values are ultimately used! And [here's why](https://github.com/jacebrowning/memegen) 0:-)

Last up is `layout.html`. It's a bit bigger than usual, but that's mostly because it comes with a fancy, mobile-friendly "navbar" (navigation bar), also based on Bootstrap. Notice how it defines a block, `main`, inside of which templates (including `apology.html` and `login.html`) shall go. Layout also holds the documentation for a footer that appears on each page giving the user a description about the website.

## Specification

### `register`

Implementation of `register` in such a way that it allows a user to register for an account via a form.

* Require that a user input a username, implemented as a text field whose `name` is `username`. Render an apology if the user's input is blank or the username already exists.
* Require that a user input a password, implemented as a text field whose `name` is `password`, and then that same password again, implemented as a text field whose `name` is `confirmation`. Render an apology if either input is blank or the passwords do not match.
* Submit the user's input via `POST` to `/register`.
* `INSERT` the new user into `users`, storing a hash of the user's password, not the password itself. Hash the user's password with [`generate_password_hash`](https://werkzeug.palletsprojects.com/en/1.0.x/utils/#werkzeug.security.generate_password_hash) Odds are you'll want to create a new template (e.g., `register.html`) that's quite similar to `login.html`.

Once you've implemented `register` correctly, you should be able to register for an account and log in (since `login` and `logout` already work)! And you should be able to see your rows via phpLiteAdmin or `sqlite3`.

### addClothing

Implementaion of `clothing` in such a way that it allows a user to upload an image, title the piece of clothing, and provide its price

The addClothing page extends the layout page through the format `{% extends "layout.html" %}` which will import that navigation bar and footer that is expected on every page of the website

* An input of type text that takes input from the user for `item_name`
* An input of type number with minimum of 1 that takes an input from the user for `cost` of the item
* An input of type file that allows the user to upload an image from their computer
* A submit button that submits the information inputted by the user 

### closet

Implementation of `closet` in such a way that it displays the images uploaded by the user and allows the count of each piece of clothing to be incremented

The closet page extends the layout page through the format `{% extends "layout.html" %}` which will import that navigation bar and footer that is expected on every page of the website

* A grid system is created by defining the container class and the row and column class which will hold the cards of images with name and count
* The for loop iterates through each image in the dicitonary pictureDict that is defined in app.py to hold all of the uploaded images and their information
* The image displayed is found from the file_blob saved at upload and then using b64 encoding to convert from base64 back to a visual that can be displayed
* Below the image the clothing piece name is displayed with `{{item.item_name }}`
* A form that allows the user to update the count of each piece of clothing that will update the count within the sqlite database when the form is submitted
* A button of type submit that will submit the input from the form which will then later be updated in the database
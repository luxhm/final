### Understanding

#### `app.py`

Open up `app.py`. Atop the file are a bunch of imports, among them CS50's SQL module and a few helper functions. More on those soon.

After configuring [Flask](http://flask.pocoo.org/), notice how this file disables caching of responses (provided you're in debugging mode, which you are by default in your code50 codespace), lest you make a change to some file but your browser not notice. It then further configures Flask to store [sessions](https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions) on the local filesystem (i.e., disk) as opposed to storing them inside of (digitally signed) cookies, which is Flask's default. The file then configures CS50's SQL module to use `app.db`.

Thereafter are a whole bunch of routes, only two of which are fully implemented: `login` and `logout`. Read through the implementation of `login` first. Notice how it uses `db.execute` (from CS50's library) to query `app.db`. And notice how it uses `check_password_hash` to compare hashes of users' passwords. Also notice how `login` "remembers" that a user is logged in by storing his or her `user_id`, an INTEGER, in `session`. That way, any of this file's routes can check which user, if any, is logged in. Finally, notice how once the user has successfully logged in, `login` will redirect to `"/"`, taking the user to their home page.  Meanwhile, notice how `logout` simply clears `session`, effectively logging a user out.

Notice how most routes are "decorated" with `@login_required` (a function defined in `helpers.py` too). That decorator ensures that, if a user tries to visit any of those routes, he or she will first be redirected to `login` so as to log in.

Notice too how most routes support GET and POST. 

`index` will render `index.html` which will show the home page. Next, `table` includes the query of the sqlite table   `image_uploads` which holds the information of each image. Within this it will query `app.db` with `db.execute` for a sepcific user_id session in order to ensure the closet from a specific person are accessed. The information is stored in `clothing` an then redirected to `table.html` where the information will be displayed in a table. Then, `register` will use a POST method in order to get a username and password from the user. Apologies are shown if the user does not input a proper username or password. When a username and password are accepted `db.execute` will query the database `app.db` and insert the information into the user table with a hash function to compares hashes of users' passwords and then redirect to `/`. At the end if something is not inputted correctly, it will render the `register.html` template again until proper input is inputted. 

`addClothing` adds a piece of clothing to a user's closet. This take a post method, specifically a file uploaded by the user The function checks if the uploaded picture is an acceptable file, with a proper name, and proper cost; if these are not inputted, an apology will be shown. `request.files` requests the file uploaded by the user, specifically usin this dot notation it will request the filename. Then, using `.read()` it will read the image file to a variable. Then using `db.execute` to query the table it will insert the image file into the table `image_uploads` with the file_name, user_id, item_name, file_blob, and cost. Specifically, `file_blob` is meant to hold the image as a Binary large Object because it cannot be stored and then displayed directly as an image. In the query, a number of `request.form.get` methods are used in order to get the information inputted by the user such as `item_name` and `cost`. `user_id` is provided based on the sesion user id which is defined above. Once the information is inserted into the table, it will redirect to `/closet`. If inputs are not put in correctly, it will continue to render the `addClothing.html` page.

`closet` displays the uploaded images that were inserted into the database `image_uploads` above. The function takes a post request and ensures that a proper count is inputted for each image with the if statements. If the count is changed properly then a query can be run that will update the `image_uploads` table by setting `count` to the inputted count value where the id is determined by `image_id`. It will then redirect to `/closet`. In the else statement, all of the images that have been upladed are selected from the image_uploads table and saved in a dictionary of pictures and their related information. These images are specific to each session `user_id` which ensures that each individuals information is saved. Then, the `closet.html` template will be rendered with `picturesDict` as its input which will be displayed as a grid. 

#### `helpers.py`

Next take a look at `helpers.py`. Ah, there's the implementation of `apology`. Notice how it ultimately renders a template, `apology.html`. It also happens to define within itself another function, `escape`, that it simply uses to replace special characters in apologies. By defining `escape` inside of `apology`, we've scoped the former to the latter alone; no other functions will be able (or need) to call it.

Next in the file is `login_required`. No worries if this one's a bit cryptic, but if you've ever wondered how a function can return another function, here's an example!

#### `requirements.txt`

Next take a quick look at `requirements.txt`. That file simply prescribes the packages on which this app will depend.

#### `static/`

Glance too at `static/`, inside of which is `styles.css`. That's where some initial CSS lives. You're welcome to alter it as you see fit.

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

### `addClothing`

Implementaion of `clothing` in such a way that it allows a user to upload an image, title the piece of clothing, and provide its price

The addClothing page extends the layout page through the format `{% extends "layout.html" %}` which will import that navigation bar and footer that is expected on every page of the website

* An input of type text that takes input from the user for `item_name`
* An input of type number with minimum of 1 that takes an input from the user for `cost` of the item
* An input of type file that allows the user to upload an image from their computer
* A submit button that submits the information inputted by the user 

### `closet`

Implementation of `closet` in such a way that it displays the images uploaded by the user and allows the count of each piece of clothing to be incremented

The closet page extends the layout page through the format `{% extends "layout.html" %}` which will import that navigation bar and footer that is expected on every page of the website

* A grid system is created by defining the container class and the row and column class which will hold the cards of images with name and count
* The for loop iterates through each image in the dicitonary pictureDict that is defined in app.py to hold all of the uploaded images and their information
* The image displayed is found from the file_blob saved at upload and then using b64 encoding to convert from base64 back to a visual that can be displayed
* Below the image the clothing piece name is displayed with `{{item.item_name }}`
* A form that allows the user to update the count of each piece of clothing that will update the count within the sqlite database when the form is submitted
* A button of type submit that will submit the input from the form which will then later be updated in the database

### `index`

Implementation of `index.html` which will act as the home page for the website

* A heading is created `What is the Green Closet?` followed by a description of the website and the purpose for its creation -- to promote sustainable shopping and wearing practices
* Below this there are muliple links to websites that are educational about fast fashion and sustainable fashion. Using the html attribute href links to other websites are accessible through our website.
* Upon clicking the link, users will be redirected to these webpages

### `login`

* A form of method post that allows the user to enter a username and password 
* The first input field takes a username and employs a placeholder `Username` to indicate the required input from the user and a type username to ensure the correct implementation
* The second input field takes a password and employs a placeholder `Password` to indicate the required input from the user and of type `password` to ensure correct inputs
* A button that allows the user to submit their information which will log them into their account

### `table`

* Create a table which will hold the name of each piece, cost, times worn, and cost per wear
* The first block `<tr>` creates the first row in the table which holds the titles for all of the information that will be held in the table as images and their information are submitted
* The for loop iterates through each clothing item and retrieves the `item_name`, `cost`, `count`, and calculates the cost per wear of each item to be displayed
* The table is updated each time a new item is added to the clothing database where the for loop is retrieving information from
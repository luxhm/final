# TheGreenCloset

# This is the README page for Lux Hogan-Murphy's and Molly Stoltz's final project, The Green Closet, for CS50 at Harvard 2022.

# Started on October 30th, 2022

# Link to our youtube video: https://youtu.be/m-FCC5caau4

### Running

Start Flask's built-in web server (within `final/`):

```
$ flask run
```

Visit the URL outputted by `flask` to see the distribution code in action. The link will take you to the home page of the website and you can begin to interact with the site. In the top right corner there is a button for register and login. First you will have to register an account. Click the register button and you will be taken to a page with a number of input fields. In the top you will input your username and then below you will input your password and then confirm. After you register, you can now login. Login with the username and password you used to register, you now have access to your closet!

Now that you have created an account you can start building your closet. Go to the page titled `Add Clothing` in the navigation bar at the top. This will lead you to a page with a more input fields that you can fill in. Before you fill out the form, make sure you have images of the clothing that you want to add to your closet. Upload the images to your computer so that you can easily access them when you want to add them to your closet. First input the name of a certain piece of clothing you will be adding to your virtual closet. Then input the cost, or an estimate if you can't remember the cost exactly. In the final field, press the file upload button which will take you to the files on your computer. Select the image you wish to upload and confirm your selection. Once you have done this you will be able to submit all of your information onto the site and your information will be added to your closet. You can continue to add items to the closet using the same steps and each will be added as a piece to your closet.

To view your closet you will go to the page titles `Closet`. Access the page through the button in the navigation bar on top of the page. Clicking on this will take you straight to your closet where you will now be able to view all of the clothing you uploaded! You will see a picture of your item, its name, and a count section and button. As you add more items to your closet, each item will be displayed in a grid format so you can easily view your pieces. The count section tells you how many times you have worn your piece of clothing. If you wish to update the count, you can either type it into the input box or press the arrow to increase or decrease your count by one. If you have updated the count, submit your changes to accurately demonstrate your wear of the item.

Building a closet is fun, but now you want to see how much you're wearing your clothes and the cost per wear of each item. This is so important for building sustainable shopping and wearing habits. To access all of your closet's information with item names, count, price, and cost per wear go up to the navigation bar and press on `Cost Per Wear`. You will see all of this information displayed in a table so that you can easily see all of your closet's information displayed. When you add new images or change the number of times you wear each piece the table will display everything. As you wear your owned items more often you will see your cost per wear decrease. Try and get it as low as possible! We want to encourage you to keep the table as small as possible and wear your preowned items as much as you can. Through this format, we hope that you will think more about your shopping practices and continue to have cost per wear on your mind when you are looking for new items.

Within `final/`, run `sqlite3 app.db` to open `app.db` with `sqlite3`. If you run `.schema` in the SQLite prompt, notice how `app.db` comes with a table called `image_uploads` and `users`. Take a look at its structure (i.e., schema). Notice how there is a file name, an item name, a file blob which holds a Binary Large Object, cost, user id and count. Notice there is a second table called users which holds the user id, username and hash in order to keep track of users' accounts.

Another way to view `app.db` is with a program called phpLiteAdmin. Click on `app.db` in your codespace's file browser, then click the link shown underneath the text "Please visit the following link to authorize GitHub Preview". You should see information about the database itself, as well as a table, `image_uploads` and `users`, just like you saw in the `sqlite3` prompt with `.schema`.


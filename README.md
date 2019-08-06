# Neighborbood Lending Library
Capstone project PDX Code Guild (Summer 2019)

## Project Overview

This app is inspired by a <a href="https://www.kptv.com/news/scout-troop-asks-for-help-finding-trailer-stolen-day-before/article_a3fb09f2-ae98-11e9-aab6-8fca529363ff.html" target="\_blank">KPTV news story</a> about a Girl Scout troop whose trailer full of camping gear was stolen the day before a big trip to Crater Lake. At the eleventh hour neighbors, friends, and family rallied to ensure the troop had the gear they needed to take the trip as scheduled. People loaned or donated tents, sleeping bags, stoves, tarps, lights, etc.

For anything that was _on loan only_, the scout leader presumably had to keep track of who each item belonged to. Why not make an app that makes it easy for neighbors, friends, family, teams, hobby groups, basically people that know each other IRL (in real life), to share their stuff.

**Think of a virtual library for more than just books.** Also, DVDs (if anyone uses those anymore), games (board, video), garden tools, camping gear, sport equipment, beach gear, tools, luggage, ... the list goes on; stuff people have in their garages that is probably gathering dust most of the time.

**This app will include:**
- a user registration system
- user profile pages
- a catalog of items that can be checked out from a variety of categories
- an interface for lenders to add, edit, and remove items
- an interface for borrowers to request, checkout/check in items

**This app will be built with the following technologies:**
- _Django_, for user registration, catalog management, and generating the user profile pages
- _Python_ for the initial password generation during user account creation
- _Javascript/HTML/CSS_ for additional functionality and styling on the front end

## Functionality

### Homepage ###
Visitors will see a list of categories to choose from, like Craigslist.

Note: *An upcoming version there will have a search field and corresponding results page.*

When a category is clicked, they will go to that Category's listing page.

### Category page ###
This page will fetch all the items for that category from the item catalog and display them to the user.

- **Name**
- **Subcategories** - for Camping Equipment, the subcategories might be: Tents, Sleeping bags, Stoves, etc.
- **Owner** (aka the Lender)
- **Availability**

### Profile page ###
<u>Owners will be able to</u>: (1) manage checkout requests, (2) see, at a glance, which items are checked out and by whom, (3) change availability of an item, and (4) check in items.

<u>Owners will see</u>:
- **Checkout Requests**: which item was requested, name of the perspective borrower
- **Items that have been checked out**: name, due date, current borrower
- **A form** to Add, Edit, and Delete items
- **A list of all items** they have in their catalog

<u>Visitors will be able to</u>: (1) browse available items, (2) contact the owner.

<u>Visitors will see</u>:
- **All the items that an owner (Lender) has to offer**
  - Name
  - Category & subcategory
  - Availability (if item is currently checked out, the expected return date will be shown)
- **A form to contact the owner**

When users click on the Item Name, they will go to an Item Detail page.

### Item Detail page ###
This page will have (1) additional information (not shown on the homepage or profile pages), (2) and a form to request to check out an item.
- Additional information:
  - Name
  - Description
  - Category and subcategory
  - Availability
  - Condition of the item (Like New, Very Good, Good, Acceptable)
  - Replacement cost, if item is lost or damaged
  - Owner
- Request form:
  - Name - prepopulated from ```user.username```
  - Text field - to add any information to the request like when item is needed
  - Contact phone number - prepopulated from ```user.phone_number```

## Data Model

### User ###
```
id
username
email
phone_number
```
### UserItem ###
```
id
name
description
type (category/subcategory)
availability
condition
replacement_cost
owner (User)
hidden (Boolean)
```
### UserItemCheckout ###
```
id
user_item (User_Item)
status (CheckoutStatus)
request_date
checkout_date (nullable)
checkin_date (nullable)
borrower (User)
due_date
```
### CheckoutStatus ###
```
id
name (Requested, Borrowed, Returned, Lost, Denied)
```
### UserItemCategories ###
```
id
name

- Books (Technical, Fiction, Nonfiction, Kids, Cooking, etc.)
- Games (Board games, Handhelds, Video game DVDs (PS, Xbox), etc.)
- DVDs (Movies, TV shows, Instructional, Concert videos, etc.)
- Camping equipment (Tents, Chairs, Coolers, Sleeping bags, Tarps, etc,)
- Sports equipment (Basketballs, Baseballs bats, Gloves, Water skis, Snow gear, etc.)
- Beach equipment (Quickshade, straw mats, stuff making sand castles, etc.)
- Tools (Hand tools - hammers, screwdrivers, etc; Power tools - saws, drill, driver, bit sets, etc.)
- Garden equipment (Rakes, Hoes, Brooms, Hedge clippers, Trimmers, Garden gloves, Trowels, etc.)
- Luggage (Rolling suitcases, Carryons, Hanging bags, etc.)
- Event equipment (Tables, Chairs, Umbrellas, etc.)
- Cooking equipment (Pots and pans, Plates, Bowls, Silverware, etc.)
- Stuff for parents (Stroller, play pens, etc.)
```

## Schedule

Here you'll want to come up with some (very rough) estimates of the timeframe for each section. State specifically which steps you'll take in the implementation. This section should also include work you're planning to do after the capstone is finished.

```Javascript
let something = document.querySelector('#something')
```

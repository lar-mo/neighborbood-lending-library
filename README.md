# Neighborbood Lending Library
Django Capstone project PDX Code Guild (Summer 2019)

## Project Overview

The creation of this app was inspired by a [KPTV news story](https://www.kptv.com/news/scout-troop-asks-for-help-finding-trailer-stolen-day-before/article_a3fb09f2-ae98-11e9-aab6-8fca529363ff.html) about a girl scout troop whose trailer full of camping gear was stolen the day before a big trip to Crater Lake. At the eleventh hour neighbors, friends, and family rallied to ensure the troop had the gear they needed to take the trip as scheduled. People loaned or donated tents, sleeping bags, stoves, tarps, lights, etc.

For anything that was _on loan only_, the scout leader presumably had to keep track of who each item belonged to. Why not make an app that makes it easy for neighbors, friends, family, teams, hobby groups, basically people that know each other IRL (in real life), to share their stuff?

**Think of a virtual library for more than just books.** Also, DVDs (if anyone uses those anymore), games (board, video), garden tools, camping gear, sport equipment, beach gear, tools, luggage, ... the list goes on; stuff people have in their garages that is probably gathering dust most of the time.

**This app will include:**
- a user registration system
- user profile pages
- a catalog of items that can be checked out from a variety of categories
- an interface for lenders to add, edit, and remove items
- an interface for borrowers to request, checkout/check in items

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

Owners will also see a Checkout History for that item.

## Data Model

### User ###
```
id                          (Automatic PK field)
username                    (CharField)
email                       (CharField)  
phone_number                (CharField)
```
### UserItem ###
```
id                          Automatic PK field
name                        CharField
description                 TextField
type (category)             ForeignKey(UserItemCategories)
availability                BooleanField
condition                   CharField
replacement_cost            CharField
owner                       ForeignKey(User)
hidden                      BooleanField
```
### UserItemCheckout ###
```
id                          Automatic PK field
user_item                   ForeignKey(User_Item)
status                      ForeignKey(CheckoutStatus)
request_date                DateTimeField
checkout_date (nullable)    DateTimeField
checkin_date (nullable)     DateTimeField
borrower                    ForeignKey(User)
due_date                    DateTimeField
```
### CheckoutStatus ###
```
id                          Automatic PK field
name                        CharField

name: Requested, Borrowed, Returned, Lost, Denied
```
### UserItemCategories ###
```
id                         Automatic PK field
name                       CharField

- Books (Technical, Fiction, Nonfiction, Kids, Cooking, etc.)
- Games (Board Games, Handhelds, Video Game DVDs (PS, Xbox), etc.)
- DVDs (Movies, TV Shows, Instructional, Concert Videos, etc.)
- Camping Equipment (Tents, Chairs, Coolers, Sleeping Bags, Tarps, etc,)
- Sports Equipment (Basketballs, Baseballs Bats, Gloves, Water Skis, Snow Gear, etc.)
- Beach Equipment (Quickshade, Straw Mats, Stuff making sand castles, etc.)
- Tools (Hand Tools - Hammers, Screwdrivers, etc; Power Tools - Saws, Drills, Bit Sets, etc.)
- Garden Equipment (Rakes, Hoes, Brooms, Hedge Clippers, Trimmers, Garden Gloves, Trowels, etc.)
- Luggage (Rolling Suitcases, Carryons, Hanging Bags, etc.)
- Event Equipment (Tables, Chairs, Umbrellas, etc.)
- Cooking Equipment (Pots and Pans, Plates, Bowls, Silverware, etc.)
- Stuff for Parents (Stroller, Play Pens, etc.)
```

## Schedule
<table>
  <tr>
    <th>Section</th>
    <th>Duration</th>
    <th>Done?</th>
  </tr>
  <tr><th colspan="3" align="center">Aug 5 - 27</th></tr>
  <tr>
    <td>Registration & Login</td>
    <td>~2 days</td>
    <td></td>
  </tr>
  <tr>
    <td>User Item Management</td>
    <td>~3 days</td>
    <td></td>
  </tr>
  <tr>
    <td>User Profile</td>
    <td>~3 days</td>
    <td></td>
  </tr>
  <tr>
    <td>Create Borrow Request</td>
    <td>~2 days</td>
    <td></td>
  </tr>
  <tr>
    <td>Approve/Deny, Check In Item</td>
    <td>~2 days</td>
    <td></td>
  </tr>
  <tr>
    <td>Improved Styling</td>
    <td>~2 days</td>
    <td></td>
  </tr>
  <tr><th colspan="3" align="center">Post Graduation</th></tr>
  <tr>
    <td>Location-based filtering & Groups</td>
    <td>~4 days</td>
    <td></td>
  </tr>
  <tr>
    <td>Rating & Reviews</td>
    <td>~7 days</td>
    <td></td>
  </tr>
</table>

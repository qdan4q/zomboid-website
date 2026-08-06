Create a small and simple website for a private Project Zomboid roleplay server.

The website will only be used by approximately 10–20 people. Do not overengineer it. It should look like an amateur fan website made in the early 2000s using basic HTML and CSS.

The website should include:

* a news section managed by the administrator;
* a marketplace where survivors can post items for sale or trade;
* user accounts;
* a very small administrator panel;
* simple Project Zomboid-inspired lore.

## 1. Project concept

The website represents an old surviving internet or intranet portal connected to the Knox Exclusion Zone.

In this setting, the outside world has not completely collapsed. Governments, military groups, radio stations, scientists, and surviving cities are still fighting the infection.

The lore should suggest that:

* the Knox Exclusion Zone is isolated;
* the outside world is still active;
* official news does not always tell the truth;
* survivors inside the zone receive local reports;
* zombies are gradually becoming more intelligent;
* strange zombie behavior is being investigated;
* military and scientific organizations are hiding information;
* survivors use the website to trade supplies and read news.

Use an editable temporary website name such as:

`Knox Community Network`

Do not copy official Project Zomboid text or assets. Create original fictional content inspired by the setting.

---

## 2. Technology

Use a simple stack:

* Python;
* Django;
* Django Templates;
* SQLite;
* HTML;
* CSS;
* minimal vanilla JavaScript.

Do not use:

* React;
* Vue;
* Angular;
* Tailwind;
* Bootstrap;
* SPA architecture;
* external frontend frameworks;
* complicated APIs;
* Docker unless it is very easy to add;
* unnecessary service layers;
* unnecessary abstractions.

The website should be easy for one beginner developer to understand and edit.

Use Django’s built-in authentication system.

---

## 3. User roles

There should only be two roles.

### Survivor

A normal registered user.

A survivor can:

* log in and log out;
* view news that is visible to survivors;
* view marketplace listings;
* create a marketplace listing;
* edit their own listing;
* delete their own listing;
* mark their own listing as sold;
* view their profile;
* edit basic profile information.

### Administrator

An administrator can:

* do everything a survivor can do;
* create news;
* edit news;
* delete news;
* change news visibility;
* view administrator-only news;
* view all marketplace listings;
* edit or delete any marketplace listing;
* manage users;
* access the administrator panel.

Use Django’s `is_staff` or `is_superuser` fields for administrator permissions.

Do not create moderator, game master, faction leader, or other roles.

All permission checks must happen on the backend.

---

## 4. News system

The news system should be very simple.

Each news article should have:

* title;
* short summary;
* full text;
* image, optional;
* author;
* created date;
* last edited date;
* in-game date, optional;
* news type;
* visibility.

News types:

* World News;
* Knox Zone News;
* Military Report;
* Scientific Report;
* Radio Message;
* Survivor Rumor.

Visibility should only have two possible values:

* `Survivors and Administrators`;
* `Administrators Only`.

When an administrator creates a news article, they choose its visibility.

If a news article is set to `Administrators Only`, normal survivors must not see it anywhere:

* not on the home page;
* not in the news list;
* not in search results;
* not through a direct URL;
* not inside the HTML source.

The administrator must be able to click an `Edit` button and change the visibility later.

For example:

1. The administrator creates a secret scientific report.
2. The report is initially visible only to administrators.
3. A roleplay event happens on the game server.
4. The administrator opens the report in the admin panel.
5. The administrator changes visibility to `Survivors and Administrators`.
6. The report immediately becomes visible to all logged-in survivors.

Do not create:

* automatic unlock rules;
* event triggers;
* faction visibility;
* zone visibility;
* character-specific visibility;
* secret codes;
* scheduled unlocks;
* complex permission systems.

The administrator changes visibility manually.

---

## 5. Marketplace

Registered survivors can create simple marketplace listings.

Listing categories:

* For Sale;
* Wanted;
* Trade;
* Services;
* Group Recruitment;
* Warning;
* Other.

Each listing should have:

* title;
* description;
* category;
* author;
* character name;
* requested price or trade;
* meeting location;
* contact information;
* image, optional;
* created date;
* status.

Listing statuses:

* Active;
* Sold;
* Closed.

A survivor can:

* create a listing;
* edit their own listing;
* delete their own listing;
* mark their own listing as sold;
* view all active listings.

An administrator can edit or delete any listing.

Do not add:

* advanced filters;
* favorites;
* reports;
* bidding;
* shopping carts;
* payment systems;
* private messaging;
* complicated item databases;
* automatic expiration;
* advanced marketplace analytics.

A simple search field for listing titles is optional, but it is not required.

---

## 6. Profiles

Each user has one simple profile.

Profile fields:

* username;
* character name;
* avatar, optional;
* short biography;
* occupation;
* current status;
* registration date.

Possible statuses:

* Alive;
* Missing;
* Injured;
* Unknown;
* Dead.

The survivor can edit:

* character name;
* avatar;
* biography;
* occupation.

The administrator can edit every field.

Do not create multiple characters per account.

Do not add:

* Steam integration;
* Discord integration;
* factions;
* reputation;
* achievements;
* character statistics;
* inventories;
* friend lists.

---

## 7. Pages

Create the following pages.

### Home page

The home page should show:

* website banner;
* short welcome message;
* latest survivor-visible news;
* latest active marketplace listings;
* emergency message;
* fictional server status;
* number of registered survivors;
* last website update date;
* small visitor counter;
* login or profile link.

### News page

Show all news visible to the current user.

Survivors only see survivor-visible news.

Administrators see:

* survivor-visible news;
* administrator-only news.

Administrator-only news should have a clear label such as:

`ADMIN ONLY`

Each news article should have its own detail page.

### Marketplace page

Show active listings in a simple list or table.

Each listing should have its own detail page.

Include a button:

`Create Listing`

### Profile page

Show the user’s:

* avatar;
* username;
* character name;
* biography;
* occupation;
* status;
* marketplace listings.

### Login page

Use a basic Django login form.

Public registration can either be:

* enabled with a simple registration form;
* disabled so the administrator creates accounts manually.

Choose the simpler option. Prefer administrator-created accounts because only 10–20 people will use the website.

### Administrator panel

Create a simple custom page at:

`/control-panel/`

Also keep the standard Django admin page available at:

`/admin/`

---

## 8. Simple administrator panel

The custom administrator panel should be very small.

It should contain links to:

* Create News;
* Manage News;
* Manage Marketplace Listings;
* Manage Users;
* Edit Site Message.

### Manage News

Show a basic table containing:

* title;
* news type;
* visibility;
* created date;
* Edit button;
* Delete button.

The administrator can:

* create a news article;
* edit a news article;
* change visibility;
* delete a news article.

The news edit form must include a clear visibility field.

Example:

```text
Visibility:
(o) Survivors and Administrators
( ) Administrators Only
```

### Manage Marketplace Listings

Show:

* title;
* author;
* category;
* status;
* Edit button;
* Delete button.

### Manage Users

Show a basic list of users.

The administrator can:

* create a user;
* deactivate a user;
* edit the user profile;
* make a user an administrator.

### Site message

Allow the administrator to edit:

* emergency message;
* server status text;
* website name;
* welcome message.

Do not build a complicated dashboard with graphs or analytics.

---

## 9. Visual style

The website must look like a real amateur website from approximately 1999–2004.

It should not look like a modern website with a retro filter.

Use:

* a fixed central width around 800–950 pixels;
* a repeating background texture;
* simple borders;
* small text;
* Verdana, Tahoma, Arial, or Courier New;
* basic tables;
* simple two-column layout;
* old-style buttons;
* small icons;
* horizontal separators;
* square interface elements;
* simple navigation links separated by `|`;
* a banner image or text banner at the top;
* a small visitor counter;
* `Last Updated` text;
* `Best viewed at 1024x768`;
* a small `SERVER ONLINE` or `SERVER OFFLINE` indicator;
* dark green, grey, beige, dark blue, and muted red colors.

Example navigation:

```text
HOME | NEWS | MARKETPLACE | PROFILE | LOGOUT
```

The website should feel handmade.

It is acceptable for the design to be slightly uneven or visually imperfect.

Do not use:

* glassmorphism;
* large rounded cards;
* gradients everywhere;
* modern dashboards;
* huge buttons;
* excessive animations;
* smooth modern page transitions;
* modern mobile-app design;
* professional corporate styling.

Use little or no border radius.

The website should still remain readable.

On smaller screens, allow horizontal scrolling or stack the content vertically. Do not spend too much development time on advanced responsive design.

---

## 10. Suggested layout

Use a simple layout.

### Header

* banner;
* website title;
* small subtitle;
* navigation.

### Left sidebar

* login information;
* profile link;
* server status;
* emergency message;
* visitor counter;
* last updated date.

### Main content

* current page content;
* latest news;
* listings;
* forms.

### Footer

Example:

```text
Knox Community Network © 1998–199X
This network is maintained by local volunteers.
Best viewed at 1024x768.
```

The date can intentionally look incorrect or corrupted as part of the lore.

---

## 11. Django models

Keep the database simple.

### UserProfile

Fields:

* user;
* character_name;
* avatar;
* biography;
* occupation;
* status.

### NewsArticle

Fields:

* title;
* summary;
* content;
* image;
* news_type;
* visibility;
* author;
* in_game_date;
* created_at;
* updated_at.

Suggested visibility values:

```python
SURVIVORS = "survivors"
ADMIN_ONLY = "admin_only"
```

### MarketplaceListing

Fields:

* title;
* description;
* category;
* author;
* character_name;
* price_or_trade;
* meeting_location;
* contact_information;
* image;
* status;
* created_at;
* updated_at.

### SiteSettings

There should only be one SiteSettings object.

Fields:

* website_name;
* welcome_message;
* emergency_message;
* server_status;
* last_updated.

Do not create unnecessary models.

---

## 12. Django application structure

Keep the number of Django applications small.

Suggested structure:

```text
project/
├── config/
├── core/
├── accounts/
├── news/
├── marketplace/
├── templates/
├── static/
├── media/
├── manage.py
└── requirements.txt
```

Responsibilities:

* `core`: home page and site settings;
* `accounts`: profiles and authentication;
* `news`: news articles;
* `marketplace`: marketplace listings.

Do not split the project into ten or more applications.

Do not create repository patterns, selectors, event buses, or microservices.

Use normal Django:

* models;
* views;
* forms;
* templates;
* URL configurations.

Class-based or function-based views are both acceptable. Choose whichever produces simpler code.

---

## 13. Security

Even though the website is small, implement basic security correctly.

Requirements:

* survivors cannot edit other users’ listings;
* survivors cannot access the administrator panel;
* survivors cannot create or edit news;
* survivors cannot open administrator-only news through a direct URL;
* administrator-only news content must not be included in HTML sent to survivors;
* forms must use CSRF protection;
* uploaded files must have size limits;
* uploaded images must be validated;
* passwords must use Django authentication;
* secrets must use environment variables;
* production must not use `DEBUG=True`;
* use Django ORM instead of raw SQL.

Do not add complex enterprise security systems.

---

## 14. Demo content

Create a management command:

```bash
python manage.py seed_demo_data
```

It should create:

* one administrator;
* five survivor accounts;
* several profiles;
* eight public news articles;
* four administrator-only news articles;
* ten marketplace listings;
* initial site settings.

Use simple development credentials and clearly document them in the README.

Example news titles:

* `Government Claims the Kentucky Situation Is Contained`;
* `Unknown Radio Signal Detected Near West Point`;
* `Military Convoy Fails to Reach Louisville`;
* `Survivors Report Infected Opening Doors`;
* `Research Team Disappears Near Restricted Facility`;
* `Water Supply Declared Unsafe`;
* `Behavioral Report KX-17`;
* `New Quarantine Line Established`.

Administrator-only article examples:

* `KX-17: Confirmed Problem-Solving Behavior`;
* `Loss of Contact with Research Station`;
* `Orders to Suppress Civilian Radio Broadcasts`;
* `Possible Infection Outside Kentucky`.

Create original fictional article text.

---

## 15. Tests

Only add essential tests.

Test that:

1. a survivor can log in;
2. a survivor can view public news;
3. a survivor cannot view administrator-only news;
4. a direct URL does not reveal administrator-only news;
5. an administrator can view administrator-only news;
6. an administrator can change news visibility;
7. a hidden article becomes visible after its visibility is changed;
8. a survivor can create a marketplace listing;
9. a survivor can edit their own listing;
10. a survivor cannot edit another user’s listing;
11. an administrator can edit or delete any listing;
12. a survivor cannot access `/control-panel/`.

Do not try to achieve complete test coverage.

---

## 16. README

Create a simple README explaining:

* what the project is;
* required Python version;
* how to create a virtual environment;
* how to install dependencies;
* how to run migrations;
* how to create demo data;
* how to start the server;
* how to access the administrator account;
* how to create news;
* how to change news visibility;
* how to create survivor accounts;
* where CSS and templates are located.

Example commands:

```bash
python -m venv .venv
```

```bash
pip install -r requirements.txt
```

```bash
python manage.py migrate
```

```bash
python manage.py seed_demo_data
```

```bash
python manage.py runserver
```

Include a `.env.example`.

---

## 17. Implementation order

Implement the project in this order.

### Step 1

* create the Django project;
* create the four Django applications;
* configure SQLite;
* configure templates, static files, and media files;
* create the base HTML layout;
* create the early-2000s CSS design.

### Step 2

* implement login;
* implement survivor profiles;
* implement administrator-created user accounts.

### Step 3

* implement the news model;
* implement news list and detail pages;
* implement the two visibility options;
* protect administrator-only news.

### Step 4

* implement marketplace listings;
* implement create, edit, delete, and mark-as-sold actions;
* enforce listing ownership.

### Step 5

* implement the custom administrator panel;
* implement news creation and editing;
* implement the visibility change control;
* implement listing and user management.

### Step 6

* add demo data;
* add essential tests;
* add README;
* check all links and forms.

After every step:

* run migrations;
* run the development server;
* fix errors;
* verify permissions;
* keep the code simple.

---

## 18. Definition of done

The project is complete when:

* it starts locally without errors;
* the administrator can create survivor accounts;
* survivors can log in;
* survivors can read public news;
* survivors cannot access administrator-only news;
* the administrator can create and edit news;
* the administrator can change a news article from administrator-only to survivor-visible;
* survivors can create marketplace listings;
* survivors can edit only their own listings;
* the administrator can manage all listings;
* the website looks like a simple amateur portal from the early 2000s;
* the README explains how to run and manage the project.

Do not turn this into a large professional platform.

The priority is:

1. simplicity;
2. working permissions;
3. early-2000s amateur appearance;
4. easy maintenance;
5. readable beginner-friendly code.

Before writing code, briefly show:

1. the proposed directory structure;
2. the models;
3. the main URLs;
4. the implementation plan.

Then begin implementing the project.

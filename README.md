Final Project: Web Scrapping Wkipedia


Distinctiveness and Complexity: 
I believe this project stands out for several reasons:
1.	Separated Back-End and Front-End: Unlike other projects in this course, which often use a monolithic architecture, this project is built on a decoupled back-end and front-end. This architectural choice alone sets it apart in terms of design philosophy and operational complexity.
2.	Technological Depth: This project forced me to dive deep into new technologies and frameworks. I had to familiarize myself with React for the front-end, which was a first for me in the course.
3.	API and REST Learning Curve: The decoupled nature of the project required a robust understanding of APIs and RESTful architecture. This involved learning how to effectively use serializers and class-based views in Django, which was covered in the views.py and serializers.py files.
4.	Admin Functions: A unique feature of this project is the admin-specific web scraping function. While in the course we saw how incredible the super-admin privilege was and how to use it, I ventured into unexplored territory by customizing the base structures of Django-admin templates. This was an area we hadn't delved into during the course. The need to modify these templates led me to consult additional documentation, contributing another layer of complexity to the project. This experience also served as a testament to Django's flexibility and robustness, further enriching my understanding of the framework. 
5.	Synchronizing Data: Managing data synchronization between the front-end and back-end added another layer of complexity. I implemented multiple debug segments to monitor and ensure that data was correctly being synced across the two ends.
6.	Handling CORS: The separated architecture led me to face Cross-Origin Resource Sharing (CORS) issues. This forced me to understand and implement CORS policies, adding to both the complexity and the learning experience.
7.	Error Handling: The architecture and technologies involved resulted in frequent errors that could originate from either the back-end, the front-end, or both. This situation pushed me to be more deliberate in my code structuring to facilitate easier debugging and error tracing.
8.	Documentation and Research: The unique setup and technologies necessitated extensive research and reading of documentation. This not only added complexity but also enriched my learning experience.
By adopting a split architecture, wrestling with CORS, incorporating admin-specific functions, and adopting new technologies, I was able to challenge myself and step outside the comfort zone of the course's standard curriculum.


Folders and Files Explanation


The project is neatly organized into distinct directories for both back-end and front-end components. To manage dependencies and streamline the sharing of the project, I chose to use Poetry for the back-end. This approach simplified my development workflow and made it convenient to document the various libraries and packages that the project depends on.
Back-End
The back-end code is located in the BackEnd directory, which houses a sub-folder named music_history. Although the initial setup was not ideal, and the Django project should have been created here, it nonetheless serves as the root project folder. This directory follows the typical Django project structure that we've been using throughout the course.
Inside music_history, you'll find core files like asgi.py, settings.py, urls.py, and wsgi.py.
Parallel to the manage.py file is the app directory, which contains:
1-	Management Folder: Within this, under the commands/ sub-directory, there's a file named delete_all_cards.py. This is a custom Django management command used to delete all card records from the database. This was especially useful during development for testing various web scraping approaches.
2-	Migrations: This folder holds all the database migration files, as you'd expect in a standard Django project. Nothing out of the ordinary here.
3-	Templates: The folder structure for templates mirrors what we've seen in the course. However, an additional path exists at templates/admin/. Within this path, the templates/admin/app/card directory contains a change_list.html file that extends the base admin/change_list.html. This extension allows for the addition of a hyperlink to access the data scraping feature directly from the admin panel, eliminating the need to manually type it into the address bar.
4-	Models.py: Here, I have a single model named “Card” that serves as a blueprint for the data I was collecting and storing. Let me explain each fields:
a.	Title: The title field is a CharField with a maximum length of 200 characters. This field holds the title of the historical event or card. It is set to be nullable and can be left blank, offering flexibility during data entry.
b.	Event Date: Interestingly, the event_date field is also a CharField and not a DateTimeField. This was a deliberate choice due to the inconsistency and variety of date formats found on Wikipedia, including terms like BCE, CE, AC, and BC. Given the difficulty in both scraping this data consistently and mapping these varied date formats to a standard DateTimeField, a CharField was used for greater flexibility.
c.	Description: The description field is a TextField that can be null and blank. It holds a textual description of the event, which might be a detailed narrative or a brief summary.
d.	Image URL: The image_url is a URLField that stores the URL of an associated image. Like other fields, it is nullable and can be blank.
e.	Source URL: Another URLField, source_url, holds the source URL of the data. This is particularly useful for citation and could be the URL of the Wikipedia page from where the data was scraped.
5-	Utils.py: This is where the heart of my app is. For imports I used:
a.	BeautifulSoup: to pull the data out of HTML and XML. 
b.	Requests: To allow HTTP/HTTPS request, used specifically to get the page content. 
c.	Card: The Django model where the scraped data is being stored. 
d.	Logging: For debugging. 
e.	Re: Regular expression library for pattern matching. 
f.	Scrape_history_data function: This function takes a title and URL as arguments and scrapes the web page content:
1.	HTTP Request: It initiates an HTTP GET request to fetch the webpage.
2.	HTML Parsing: BeautifulSoup is used to parse the HTML content.
3.	Data Cleaning: Removes unnecessary tags like divs of class 'quotebox', 'thumbinner multiimageinner', style tags, and figcaption tags.
4.	Section Extraction: It uses regular expressions to find all the sections with headers (h1, h2, etc.) that match the given title. It then filters out unwanted sections like "bibliography," "references," etc.
5.	Data Aggregation: The function collects the title and content of each matching section and stores it in a list.
g.	Save_history_data function: This function is responsible for saving the scraped data into the database. 
1.	Data Validation: It checks if the scraped data is valid.
2.	Data Duplication Check: The function checks for existing records that match the title and source URL.
3.	Data Update or Insert: If a match is found, the existing record is updated; otherwise, a new record is created.
h.	Validate_input function: A simple function to validate the input string. 
6-	Views.py: Overall, this file is responsible for setting up the API endpoints and handling the business logic behind them. It leverages several features of Django's REST framework, such as custom actions, permissions, and pagination.
7-	Serializers.py: The CardSerializer class in serializers.py serves as the data bridge between Card model and the API.
8-	Form.py: The “ScrapeHistoryDataForm” is designed to facilitate user input fir web scraping. It does say “year_or_title” but it only works with titles. Like I mentioned before, there wasn’t an enough consistent way for me to scrap years correctly. 
9-	Apps.py: Just setting some default behaviours for the app. 
10-	Admin.py: In this file`, the `CardAdmin` class is a customized Django admin class for the `Card` model. It specifies which fields should be displayed in the admin list view through `list_display`. The `get_urls` method extends the default admin URLs by adding a custom URL path for the `scrape_history_data_view` method. This custom method defines the behaviour for the web scraping admin interface. When a POST request is made, the method retrieves the title and URL submitted by the user, validates them, and then initiates the web scraping process by calling `scrape_history_data`. If the data is successfully scraped and saved, a success message is displayed; otherwise, an error message is shown. Finally, the `Card` model is registered with the `CardAdmin` class to apply these customizations to the Django admin interface.


Front-End Explanation:

The front-end code is located in the FrontEnd directory, which houses a sub-folder named music_history-frontend. Although, again, the initial setup was not ideal, and the React project should have been created here, it nonetheless serves as the root project folder. This directory follows the typical npm project structure.

Main File: TimeLine.js
The primary file for the front-end is “TimeLine.js”, which is a React component responsible for displaying the timeline of music history events. Below are the key functionalities and aspects of this file:

1. State Management: I used React's `useState` and `useEffect` hooks for state management and side effects. Initial states for the timeline data, pagination, and more are set using `useState`.

2. Data Transformation: The function `transformData` takes raw data fetched from the API and transforms it into the desired format, extracting key information like `id`, `title`, `event_date`, `description`, and `image_url`.

3. Data Fetching: The `fetchData` function is responsible for fetching data from the backend API. This function uses the `fetch` API to request data and updates the local state upon successfully fetching it. The function also handles pagination with the `page` state.

4. Infinite Scrolling: The component is designed to fetch more data when the user scrolls to the bottom of the page, implementing a form of infinite scrolling.

5. Event Handling: The `handleScroll` function listens for the scroll event on the timeline and fetches the next set of data if the user reaches the bottom of the page. 

6. Content Display: The `VerticalTimeline` and `VerticalTimelineElement` components from the `react-vertical-timeline-component` library are used to visually represent the timeline. 

7. Card Expansion: Each timeline element or card has an option to expand or collapse its content. This is managed by the `toggleExpand` function, which updates the `expandedCards` state.

8. Styling: Custom CSS classes and inline styles are used to style the timeline and its elements. Even though I’m really bad at it, I tried. 

9. Error Handling: Basic error handling is implemented using `try-catch` blocks in the `fetchData` function.



How to Run


Back-End:
1.	Navigate to the Back-End Directory: Open your terminal and navigate to the directory where the back-end code is located.
2.	Activate Virtual Environment: If you're using Poetry, run poetry shell to activate the virtual environment.
3.	Install Dependencies: Run poetry install to install the required Python packages.
4.	Run Server: Execute python manage.py runserver or poetry run python manage.py runserver to start the Django development server. You should see output indicating that the server is running as usual on http://127.0.0.1:8000/.
Front-End:
1.	Navigate to the Front-End Directory: Open a new terminal and navigate to the directory where the front-end code is located.
2.	Install Dependencies: Run npm install or yarn install to install the required JavaScript packages.
3.	Run Server: Execute npm start or yarn start to start the React development server. Your default web browser should automatically open displaying the app, usually on http://localhost:3000/.


NOTE: Overall, During this course, I've learned a lot and feel much more confident in my skills than when I started. A big thank you to everyone involved, and especially to those who read and grade our projects. Your time and effort are much appreciated. 

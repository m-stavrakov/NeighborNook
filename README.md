# NeighborNook
Welcome to NeighborNook, a platform designed to help you find and connect with like-minded individuals through local events and activities. Whether you're new to the area or just looking to expand your social circle, our website makes it easier to discover and join events that match your interests.

Background

Having moved from Bulgaria to the UK at the age of 18, I faced the challenge of finding people with similar interests in a new environment. Despite trying numerous social media platforms and forums, the abundance of information made it overwhelming to find relevant activities and connect with others. This experience inspired the creation of NeighborNook—a platform to streamline the process of finding and joining local events.

Features

User Authentication: Sign up and log in to create a unique profile with your username, email, name, password, bio, and profile image.
Live Weather: View the current weather forecast for London with an icon.
Events: Create, view, and join events with details including name, overview, description, location, time, age limit, weather conditions, category, what to bring, images, and a countdown timer.
Categories: Browse events based on specific categories.
Messages: Communicate with other users through direct messaging.
Password Reset: Easily reset your password if forgotten.
Customer Support: Access customer support via a chat box for assistance and queries.
Search Page: Find events based on categories or keywords.
Technology Stack

Languages: HTML5, CSS, JavaScript, Python
Frameworks: Django, Django Test Auth, Django Security Middleware, Bootstrap 5
Database: PostgreSQL
Hosting: Fly.io
API: Meteomatics API Documentation
Chat Box: Tidio
Wireframe: Figma, LucidSpark
Technology Choices
Django: Chosen for its efficient model handling, form handling, testing capabilities, and API management.
Fly.io: Selected for its cost-effectiveness and ease of use, overcoming previous issues with Render.
Challenges

React: Initially planned for the frontend, but omitted due to time constraints and limited familiarity. Future development will include React for enhanced functionality.
Weather API: Implemented a weather widget, but faced difficulties with a weekly forecast feature. Plan to address this in future updates.
Local vs. Fly.io Server: Encountered issues with database communication between local and Fly.io servers, resolved by setting up WireGuard tunneling. Fly.io Networking Documentation, YouTube Setup Guide.
Multiple Image Uploads: Faced issues with allowing multiple image uploads for events. Resolved by creating a separate model and form for images.
Event Image Editing: Users can currently only edit event details except for images. Further development needed to enable image modifications.
Future Implementations

React Integration: Incorporate React to enhance the frontend and add new features.
Group Chat: Introduce group chat functionality for multiple users.
Weekly Weather Forecast: Add a dedicated page for weekly weather forecasts.
Location-Based Events: Implement functionality for users to enter addresses and postcodes to find nearby events and weather.
Event Image Management: Allow users to add, delete, or change images for events they created.
Event Editing Permissions: Enable users to grant others permission to edit their created events.
Event Likes: Add a "like" button to events and a page to view favorited events.
Event Location Map: Replace text-based location with a map for event locations.
Thank you for using Community Connection! We hope you find this platform helpful in discovering and connecting with new people and activities. If you have any feedback or need support, please don't hesitate to reach out through our customer support chat.

# Deployment 
in terminal write fly deploy
then it should come up with this link https://neighbornook-backend.fly.dev/
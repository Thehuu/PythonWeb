# My JS Project

## Overview
This project is a web application that utilizes Google Maps to display various incident markers. It provides an interactive map experience, allowing users to view and interact with markers representing different types of incidents.

## Project Structure
```
my-js-project
├── staticfiles
│   ├── css
│   │   └── styles.css        # Styles for the project
│   ├── js
│   │   ├── map_statistic.js  # JavaScript for Google Maps functionality
│   │   └── oms.min.js        # Overlapping Marker Spiderfier library
├── index.html                # Main HTML document
└── README.md                 # Project documentation
```

## Setup Instructions
1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd my-js-project
   ```

2. **Open `index.html`** in your web browser to view the application.

3. **Ensure you have an active internet connection** for loading Google Maps and any external resources.

## Usage
- The application displays a Google Map centered at a predefined location.
- Markers are placed on the map to represent different types of incidents.
- Clicking on a marker will display additional information about the incident.
- The Overlapping Marker Spiderfier library is included to manage overlapping markers effectively.

## Dependencies
- Google Maps JavaScript API
- Overlapping Marker Spiderfier (OMS)

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
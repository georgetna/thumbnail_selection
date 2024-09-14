
# Thumbnail Selector

A Streamlit app that allows users to select the best thumbnail for videos based on associated keywords (concepts). The app collects user selections to analyze preferences and is backend agnostic regarding thumbnail storage (local folder or AWS S3).

## Features

- **User Authentication**: Secure login system to track user selections.
- **Thumbnail Selection**: Users select thumbnails that best represent given keywords.
- **Data Storage**: Stores votes and user preferences for analysis.
- **Backend Agnostic**: Supports loading thumbnails from local storage or AWS S3.

## Requirements

- Python 3.8 or higher
- [Poetry](https://python-poetry.org/) for dependency management

## Installation

### 1. Clone the Repository

```bash
git clone https://gitlab.hulk.tech/George/thumbnail_platform.git
cd thumbnail-selector
```

### 2. Install Poetry

If you don't have Poetry installed, install it using the following command:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

For detailed instructions, visit the [Poetry documentation](https://python-poetry.org/docs/).

### 3. Install Dependencies

```bash
poetry install
```

This command will create a virtual environment and install all the required dependencies.

### 4. Activate the Virtual Environment

```bash
poetry shell
```

### 5. Configure the Application

-Add or edit the file video_metadata.csv -this should have two columns,
The first being the video filename, the second should be a list of keywords for the video, 
separated by commas. 
-t helps if the video filename is it's title

Next, run this to spin up the database
python modules/database.py

Then run this to load the videos, generate the thumbnails
TODO - plugin thumbnail generation algorithms, at the moment this just grabs random frames
python scripts/populate_data.py



### 6. Run the Application

```bash
streamlit run app.py
```

Open the displayed URL in your web browser to access the app.

## Usage

1. **Login or Register**: Create a new account or log in with your existing credentials.

2. **Select Thumbnails**:

   - View the presented video title and associated keywords.
   - For each keyword, select the thumbnail that best represents it.
   - Click 'Save' to submit your selections.

3. **Continue**:

   - After saving, you'll be presented with new thumbnails and keywords.
   - Repeat the selection process.


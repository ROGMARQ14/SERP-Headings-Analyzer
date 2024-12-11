# SERP Analyzer

A Streamlit web application to analyze the top Google search results for any query and extract HTML elements like titles, meta descriptions, and headers (H1-H6).

## Features

- User-friendly web interface built with Streamlit
- Fetches top Google search results for any query
- Extracts page title, meta description, and headers (H1-H6)
- Saves results in both JSON and Excel formats
- Includes ranking position for each result
- Interactive results display with expandable sections
- Download options for analyzed data
- Progress tracking during analysis
- Configurable number of results and request delays

## Installation

1. Clone this repository
2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

The web interface will allow you to:
1. Enter your search query
2. Set the number of results to analyze
3. Configure delay between requests
4. View analysis progress in real-time
5. Download results in JSON or Excel format
6. View detailed analysis with expandable sections

## Output Format

The tool generates two downloadable files for each analysis:
1. JSON file with detailed structured data
2. Excel file with formatted results for easy viewing

Each result includes:
- URL
- Ranking position
- Page title
- Meta description
- H1-H6 headers

## Error Handling

The application includes robust error handling for:
- Network issues
- Invalid URLs
- Timeout errors
- Parsing errors

## Note

Please be mindful of Google's terms of service when using this tool. Consider implementing delays between requests for production use.

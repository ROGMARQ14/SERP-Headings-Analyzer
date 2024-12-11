# SERP Analyzer

A Python tool to analyze the top Google search results for any query and extract HTML elements like titles, meta descriptions, and headers (H1-H6).

## Features

- Fetches top Google search results for any query
- Extracts page title, meta description, and headers (H1-H6)
- Saves results in both JSON and Excel formats
- Includes ranking position for each result
- Handles errors gracefully with proper error messages
- User-friendly command line interface

## Installation

1. Clone this repository
2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the script:
```bash
python serp_analyzer.py
```

The script will prompt you for:
1. Search query
2. Number of results to analyze (default: 10)

Results will be saved in the `output` directory in both JSON and Excel formats.

## Output Format

The tool generates two files for each analysis:
1. JSON file with detailed structured data
2. Excel file with formatted results for easy viewing

Each result includes:
- URL
- Ranking position
- Page title
- Meta description
- H1-H6 headers

## Error Handling

The script includes robust error handling for:
- Network issues
- Invalid URLs
- Timeout errors
- Parsing errors

## Note

Please be mindful of Google's terms of service when using this tool. Consider implementing delays between requests for production use.

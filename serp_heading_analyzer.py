import requests
from bs4 import BeautifulSoup
from googlesearch import search
import pandas as pd
from typing import List, Dict
from datetime import datetime
import json
import os
import time

class SERPAnalyzer:
    def __init__(self, query: str, num_results: int = 10, delay: float = 2.0):
        """
        Initialize the SERP analyzer
        
        Args:
            query (str): Search query to analyze
            num_results (int): Number of results to fetch (default: 10)
            delay (float): Delay between requests in seconds (default: 2.0)
        """
        self.query = query
        self.num_results = num_results
        self.delay = delay
        self.results = []
        
    def get_serp_urls(self) -> List[str]:
        """Fetch URLs from Google SERP"""
        try:
            results_generator = search(self.query, num_results=self.num_results, lang="en")
            return list(results_generator)
        except Exception as e:
            print(f"Error fetching SERP results: {e}")
            return []

    def extract_page_elements(self, url: str) -> Dict:
        """
        Extract HTML elements from a given URL
        
        Args:
            url (str): URL to analyze
            
        Returns:
            dict: Dictionary containing extracted elements
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            
            # Add delay between requests
            time.sleep(self.delay)
            
            page = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(page.text, "html.parser")
            
            # Extract elements
            elements = {
                'url': url,
                'title': self._get_text(soup.find('title')),
                'meta_description': self._get_meta_description(soup),
                'h1': [h.get_text(strip=True) for h in soup.find_all('h1') if h.get_text(strip=True)],
                'h2': [h.get_text(strip=True) for h in soup.find_all('h2') if h.get_text(strip=True)],
                'h3': [h.get_text(strip=True) for h in soup.find_all('h3') if h.get_text(strip=True)],
                'h4': [h.get_text(strip=True) for h in soup.find_all('h4') if h.get_text(strip=True)],
                'h5': [h.get_text(strip=True) for h in soup.find_all('h5') if h.get_text(strip=True)],
                'h6': [h.get_text(strip=True) for h in soup.find_all('h6') if h.get_text(strip=True)]
            }
            
            return elements
            
        except Exception as e:
            print(f"Error analyzing {url}: {e}")
            return None

    def _get_text(self, element) -> str:
        """Safely extract text from a BS4 element"""
        return element.get_text(strip=True) if element else ''

    def _get_meta_description(self, soup) -> str:
        """Extract meta description from soup"""
        meta = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
        return meta.get('content', '').strip() if meta else ''

    def analyze_serp(self) -> List[Dict]:
        """Analyze all SERP results"""
        urls = self.get_serp_urls()
        results = []
        
        print(f"\nFound {len(urls)} URLs to analyze")
        print("Starting analysis (this may take a few minutes)...\n")
        
        for i, url in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}] Analyzing: {url}")
            page_elements = self.extract_page_elements(url)
            if page_elements:
                page_elements['rank'] = i
                results.append(page_elements)
                print(f"✓ Successfully analyzed URL {i}\n")
            else:
                print(f"✗ Failed to analyze URL {i}\n")
        
        self.results = results
        return results

    def save_results(self, output_dir: str = "output"):
        """
        Save results to JSON and Excel files
        
        Args:
            output_dir (str): Directory to save results
        """
        if not self.results:
            print("No results to save")
            return

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"{self.query.replace(' ', '_')}_{timestamp}"
        
        # Save as JSON
        json_path = os.path.join(output_dir, f"{base_filename}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        # Save as Excel
        excel_path = os.path.join(output_dir, f"{base_filename}.xlsx")
        
        # Convert nested lists to strings for Excel
        excel_data = []
        for result in self.results:
            row = result.copy()
            for key in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                row[key] = '\n'.join(row[key])
            excel_data.append(row)
            
        df = pd.DataFrame(excel_data)
        df.to_excel(excel_path, index=False)
        
        print(f"\nResults saved to:")
        print(f"- JSON: {json_path}")
        print(f"- Excel: {excel_path}")

def main():
    print("SERP Analyzer - Extract headers from top Google search results")
    print("=" * 60 + "\n")
    
    # Get user input
    query = input("Enter your search query: ").strip()
    while not query:
        print("Error: Search query cannot be empty")
        query = input("Enter your search query: ").strip()
    
    try:
        num_results = int(input("Enter number of results to analyze (default 10): ").strip() or "10")
        if num_results <= 0:
            print("Invalid number, using default: 10")
            num_results = 10
    except ValueError:
        print("Invalid input, using default: 10")
        num_results = 10
    
    # Create analyzer and run analysis
    analyzer = SERPAnalyzer(query, num_results)
    analyzer.analyze_serp()
    
    # Save results
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    analyzer.save_results(output_dir)

if __name__ == "__main__":
    main()

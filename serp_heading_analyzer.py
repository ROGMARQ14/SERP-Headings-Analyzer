import requests
from bs4 import BeautifulSoup
from googlesearch import search
import pandas as pd
from typing import List, Dict
from datetime import datetime
import json
import os

class SERPAnalyzer:
    def __init__(self, query: str, num_results: int = 10):
        """
        Initialize the SERP analyzer
        
        Args:
            query (str): Search query to analyze
            num_results (int): Number of results to fetch (default: 10)
        """
        self.query = query
        self.num_results = num_results
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
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            page = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(page.text, "html.parser")
            
            # Extract elements
            elements = {
                'url': url,
                'title': self._get_text(soup.find('title')),
                'meta_description': self._get_meta_description(soup),
                'h1': [h.get_text(strip=True) for h in soup.find_all('h1')],
                'h2': [h.get_text(strip=True) for h in soup.find_all('h2')],
                'h3': [h.get_text(strip=True) for h in soup.find_all('h3')],
                'h4': [h.get_text(strip=True) for h in soup.find_all('h4')],
                'h5': [h.get_text(strip=True) for h in soup.find_all('h5')],
                'h6': [h.get_text(strip=True) for h in soup.find_all('h6')]
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
        meta = soup.find('meta', attrs={'name': 'description'})
        return meta.get('content', '') if meta else ''

    def analyze_serp(self) -> List[Dict]:
        """Analyze all SERP results"""
        urls = self.get_serp_urls()
        results = []
        
        for i, url in enumerate(urls, 1):
            print(f"Analyzing result {i}/{len(urls)}: {url}")
            page_elements = self.extract_page_elements(url)
            if page_elements:
                page_elements['rank'] = i
                results.append(page_elements)
        
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
        
        print(f"Results saved to:")
        print(f"- JSON: {json_path}")
        print(f"- Excel: {excel_path}")

def main():
    # Example usage
    query = input("Enter your search query: ")
    num_results = int(input("Enter number of results to analyze (default 10): ") or "10")
    
    analyzer = SERPAnalyzer(query, num_results)
    print(f"\nAnalyzing top {num_results} results for: {query}")
    analyzer.analyze_serp()
    
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    analyzer.save_results(output_dir)

if __name__ == "__main__":
    main()

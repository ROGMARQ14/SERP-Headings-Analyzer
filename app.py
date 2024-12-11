import streamlit as st
from serp_analyzer import SERPAnalyzer
import pandas as pd
import json
import os
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="SERP Analyzer",
    page_icon="🔍",
    layout="wide"
)

# Title and description
st.title("🔍 SERP Analyzer")
st.markdown("""
This tool analyzes the top Google search results for any query and extracts HTML elements 
like titles, meta descriptions, and headers (H1-H6) to help you understand how top-ranking 
pages structure their content.
""")

# Sidebar controls
with st.sidebar:
    st.header("Settings")
    query = st.text_input("Search Query", placeholder="Enter your search query...")
    num_results = st.slider("Number of results", min_value=1, max_value=20, value=10)
    delay = st.slider("Delay between requests (seconds)", min_value=1.0, max_value=5.0, value=2.0, step=0.5)
    
    analyze_button = st.button("Analyze SERP", type="primary")

# Main content area
if analyze_button and query:
    try:
        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Initialize analyzer
        analyzer = SERPAnalyzer(query, num_results, delay)
        
        # Get URLs
        urls = analyzer.get_serp_urls()
        if not urls:
            st.error("No URLs found. Please try a different query.")
            st.stop()
            
        # Create expander for URLs
        with st.expander("Found URLs", expanded=False):
            for i, url in enumerate(urls, 1):
                st.text(f"{i}. {url}")
        
        # Analyze each URL
        results = []
        for i, url in enumerate(urls, 1):
            # Update progress
            progress = i / len(urls)
            progress_bar.progress(progress)
            status_text.text(f"Analyzing URL {i}/{len(urls)}: {url}")
            
            # Analyze URL
            page_elements = analyzer.extract_page_elements(url)
            if page_elements:
                page_elements['rank'] = i
                results.append(page_elements)
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        if not results:
            st.error("No results could be analyzed. Please try again.")
            st.stop()
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        # Save JSON
        json_filename = f"{query.replace(' ', '_')}_{timestamp}.json"
        json_path = os.path.join(output_dir, json_filename)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Save Excel
        excel_filename = f"{query.replace(' ', '_')}_{timestamp}.xlsx"
        excel_path = os.path.join(output_dir, excel_filename)
        
        # Prepare data for display and Excel
        display_data = []
        for result in results:
            row = result.copy()
            for key in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                row[key] = '\n'.join(row[key])
            display_data.append(row)
        
        df = pd.DataFrame(display_data)
        df.to_excel(excel_path, index=False)
        
        # Display results
        st.success("Analysis completed!")
        
        # Download buttons
        col1, col2 = st.columns(2)
        with col1:
            with open(json_path, 'rb') as f:
                st.download_button(
                    label="Download JSON",
                    data=f,
                    file_name=json_filename,
                    mime="application/json"
                )
        with col2:
            with open(excel_path, 'rb') as f:
                st.download_button(
                    label="Download Excel",
                    data=f,
                    file_name=excel_filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        # Display results in tabs
        tab1, tab2 = st.tabs(["📊 Overview", "📑 Detailed Results"])
        
        with tab1:
            # Summary statistics
            st.subheader("Summary")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total URLs Analyzed", len(results))
            with col2:
                avg_h1 = sum(len(r['h1']) for r in results) / len(results)
                st.metric("Average H1 Tags", f"{avg_h1:.1f}")
            with col3:
                avg_h2 = sum(len(r['h2']) for r in results) / len(results)
                st.metric("Average H2 Tags", f"{avg_h2:.1f}")
        
        with tab2:
            # Detailed results
            st.subheader("Detailed Results")
            for result in results:
                with st.expander(f"#{result['rank']} - {result['title']}", expanded=False):
                    st.write("**URL:**", result['url'])
                    st.write("**Meta Description:**", result['meta_description'])
                    
                    # Display headers
                    for header in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                        if result[header]:
                            st.write(f"**{header.upper()}:**")
                            for h in result[header]:
                                st.write(f"- {h}")
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

else:
    if analyze_button and not query:
        st.warning("Please enter a search query.")

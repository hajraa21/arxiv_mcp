from mcp.server.mcpserver import MCPServer
import arxiv
import logging
import sys
import fitz
import requests


logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


mcp= MCPServer()

client = arxiv.Client()

@mcp.tool()
def get_arxiv(max_results: int, topic: str):
    """Gets the latest papers from arxiv based on the topic given by user (eg., Machine Learning, Astro physics, Chemistry,Mathematics, etc. )and returns the following information for them: Title, Author, Summary, Link, Published date, Important information"""

    search = arxiv.Search(
        query= topic,
        max_results= max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    logger.info(f"Searching for papers on topic: {topic} with max results: {max_results}")

    papers_output = []
    results = list(client.results(search))[:max_results]

    for idx, paper in enumerate(results, 1):
        paper_info = (
            f"Title: {paper.title}\n"
            f"Authors: {', '.join([author.name for author in paper.authors])}\n"
            f"Summary: {paper.summary}\n"
            f"Link: {paper.pdf_url}\n"
            f"Published: {paper.published}\n"
            "-" * 40
        )
        papers_output.append(paper_info)
        

    if not papers_output:
            return "No papers found for the given topic. Try a different topic or check your internet connection."

    return "\n\n".join(papers_output)


@mcp.tool()
def get_paper_content(pdf_url: str, max_pages:int):
     
     """Downloads a specific ArXiv paper using its PDF link and extracts its text for deep research."""

     logger.info(f"Downloading and parsing PDF from: {pdf_url}")
    
     try:
        response = requests.get(pdf_url, timeout=20)
        response.raise_for_status()
            
        # Open PDF 
        with fitz.open(stream=response.content, filetype="pdf") as doc:
                extracted_text = []
                total_pages = len(doc)
                pages_to_read = min(max_pages, total_pages)
                
                extracted_text.append(f"Successfully loaded paper. Total pages: {total_pages}. Displaying first {pages_to_read} pages:\n" + "=" * 40)
                
                for page_num in range(pages_to_read):
                    page = doc[page_num]
                    extracted_text.append(f"\n--- Page {page_num + 1} ---\n" + page.get_text())
                    
                return "\n".join(extracted_text)
                
     except Exception as e:
        logger.error(f"Failed to process PDF: {e}")
        return f"Error downloading or parsing the PDF: {str(e)}"

if __name__ == "__main__":
    mcp.run()
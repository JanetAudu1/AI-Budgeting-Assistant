import os

def get_sources() -> str:
    """Retrieve financial sources from environment or default list."""
    # Default sources list
    default_sources = [
        "Investopedia",
        "NerdWallet",
        "Financial Times",
        "Bloomberg",
        "The Wall Street Journal"
    ]
    
    # Fetch from environment or use default
    sources = os.getenv("FINANCIAL_SOURCES", ", ".join(default_sources))
    return sources

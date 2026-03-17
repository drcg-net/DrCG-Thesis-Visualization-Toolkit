"""Bibliometric analysis and network generation."""

import pandas as pd
import logging
from typing import Dict, List, Optional, Tuple
from collections import Counter
import networkx as nx

logger = logging.getLogger(__name__)


def parse_authors_field(authors_str: str, separator: str = ";") -> List[str]:
    """Parse authors from semicolon or comma-separated string."""
    if not authors_str or pd.isna(authors_str):
        return []
    return [a.strip() for a in str(authors_str).split(separator)]


def extract_keywords_field(keywords_str: str, separator: str = ";") -> List[str]:
    """Extract keywords from semicolon or comma-separated string."""
    if not keywords_str or pd.isna(keywords_str):
        return []
    return [k.strip() for k in str(keywords_str).split(separator)]


def create_coauthorship_network(df: pd.DataFrame, author_column: str = "authors") -> Tuple[nx.Graph, Dict]:
    """
    Create a co-authorship network from bibliographic data.
    
    Returns:
        (NetworkX Graph, node statistics dictionary)
    """
    G = nx.Graph()
    
    edge_counts = Counter()
    
    for authors_str in df[author_column]:
        authors = parse_authors_field(authors_str)
        # Add edges between all pairs of authors
        for i, a1 in enumerate(authors):
            G.add_node(a1)
            for a2 in authors[i+1:]:
                edge = tuple(sorted([a1, a2]))
                edge_counts[edge] += 1
                G.add_edge(a1, a2, weight=edge_counts[edge])
    
    # Calculate node stats
    node_stats = {
        node: {
            "degree": G.degree(node),
            "publications": sum(1 for _ in G.neighbors(node)),
            "betweenness": nx.betweenness_centrality(G).get(node, 0),
        }
        for node in G.nodes()
    }
    
    logger.info(f"Created co-authorship network with {len(G)} authors and {len(G.edges())} collaborations")
    return G, node_stats


def create_keyword_network(df: pd.DataFrame, keyword_column: str = "keywords") -> Tuple[nx.Graph, Dict]:
    """
    Create a keyword co-occurrence network.
    
    Returns:
        (NetworkX Graph, node statistics dictionary)
    """
    G = nx.Graph()
    
    for keywords_str in df[keyword_column]:
        keywords = extract_keywords_field(keywords_str)
        # Add edges between all pairs of keywords
        for i, k1 in enumerate(keywords):
            G.add_node(k1)
            for k2 in keywords[i+1:]:
                if G.has_edge(k1, k2):
                    G[k1][k2]["weight"] += 1
                else:
                    G.add_edge(k1, k2, weight=1)
    
    node_stats = {
        node: {
            "degree": G.degree(node),
            "centrality": nx.betweenness_centrality(G).get(node, 0),
        }
        for node in G.nodes()
    }
    
    logger.info(f"Created keyword network with {len(G)} keywords and {len(G.edges())} co-occurrences")
    return G, node_stats


def create_source_frequency_table(df: pd.DataFrame, source_column: str = "source") -> pd.DataFrame:
    """Create frequency table of publication sources."""
    freq = df[source_column].value_counts().reset_index()
    freq.columns = ["source", "count"]
    freq["percentage"] = (freq["count"] / freq["count"].sum() * 100).round(2)
    return freq


def create_citations_over_time(df: pd.DataFrame, year_column: str = "year", citation_column: str = "citations") -> pd.DataFrame:
    """Create citation trends over time."""
    df_sorted = df.sort_values(year_column)
    df_sorted["cumulative_citations"] = df_sorted[citation_column].cumsum()
    return df_sorted[[year_column, citation_column, "cumulative_citations"]]


def extract_bibliometric_summary(df: pd.DataFrame) -> Dict:
    """Extract summary statistics from bibliographic data."""
    return {
        "total_publications": len(df),
        "publication_years": f"{df['year'].min()}-{df['year'].max()}" if "year" in df.columns else "N/A",
        "average_citations": df["citations"].mean() if "citations" in df.columns else 0,
        "unique_authors": sum(len(parse_authors_field(str(a))) for a in df.get("authors", [])) if "authors" in df.columns else 0,
        "unique_sources": df["source"].nunique() if "source" in df.columns else 0,
        "unique_keywords": sum(len(extract_keywords_field(str(k))) for k in df.get("keywords", [])) if "keywords" in df.columns else 0,
    }


def prepare_vosvviewer_data(df: pd.DataFrame, export_type: str = "authors") -> pd.DataFrame:
    """
    Prepare data in VOSviewer-compatible format.
    
    Export types: 'authors', 'keywords', 'sources', 'citations'
    """
    if export_type == "authors":
        # Create author co-occurrence matrix
        author_pairs = []
        for authors_str in df.get("authors", []):
            authors = parse_authors_field(authors_str)
            for i, a1 in enumerate(authors):
                for a2 in authors[i+1:]:
                    author_pairs.append({"author1": a1, "author2": a2})
        return pd.DataFrame(author_pairs)
    
    elif export_type == "keywords":
        keyword_pairs = []
        for keywords_str in df.get("keywords", []):
            keywords = extract_keywords_field(keywords_str)
            for i, k1 in enumerate(keywords):
                for k2 in keywords[i+1:]:
                    keyword_pairs.append({"keyword1": k1, "keyword2": k2})
        return pd.DataFrame(keyword_pairs)
    
    elif export_type == "sources":
        return df[["source", "year", "citations"]].copy() if "source" in df.columns else df
    
    elif export_type == "citations":
        return create_citations_over_time(df)
    
    return df


def create_cooccurrence_table(df: pd.DataFrame, field: str = "keywords", min_count: int = 2) -> pd.DataFrame:
    """Create co-occurrence table for VOSviewer or external analysis."""
    items = []
    for value_str in df.get(field, []):
        values = extract_keywords_field(value_str) if field == "keywords" else parse_authors_field(value_str)
        items.extend(values)
    
    freq = Counter(items)
    freq = {k: v for k, v in freq.items() if v >= min_count}
    
    df_cooccurrence = pd.DataFrame(
        list(freq.items()),
        columns=[field, "count"]
    ).sort_values("count", ascending=False)
    
    return df_cooccurrence

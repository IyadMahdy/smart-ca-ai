from collections import defaultdict


def group_law_results(results, max_chunks_per_article=3):
    """
    Group retrieved law chunks by article_number
    and keep top-N chunks per article.
    """
    grouped = defaultdict(list)

    for r in results:
        grouped[r["article_number"]].append(r)

    final = []

    for article_number, chunks in grouped.items():
        chunks = sorted(chunks, key=lambda x: x["score"], reverse=True)

        final.append({
            "article_number": article_number,
            "max_score": chunks[0]["score"],
            "chunks": chunks[:max_chunks_per_article],
        })

    final.sort(key=lambda x: x["max_score"], reverse=True)
    return final

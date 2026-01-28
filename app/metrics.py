metrics = {
    "total_queries": 0,
    "rejected_queries": 0,
    "total_similarity": 0.0,
    "total_latency_ms": 0.0,
    "answered_queries": 0
}

def record_query(similarity, latency_ms: float, rejected: bool):
    metrics["total_queries"] += 1
    metrics["total_latency_ms"] += float(latency_ms)

    if rejected:
        metrics["rejected_queries"] += 1
        return

    metrics["answered_queries"] += 1

    # 🔥 FORCE numpy → python float
    if similarity is not None:
        metrics["total_similarity"] += float(similarity)


def get_metrics():
    avg_similarity = (
        metrics["total_similarity"] / metrics["answered_queries"]
        if metrics["answered_queries"] > 0
        else 0.0
    )

    avg_latency = (
        metrics["total_latency_ms"] / metrics["total_queries"]
        if metrics["total_queries"] > 0
        else 0.0
    )

    # 🔥 ENSURE PURE PYTHON TYPES
    return {
        "total_queries": int(metrics["total_queries"]),
        "rejected_queries": int(metrics["rejected_queries"]),
        "avg_similarity": round(float(avg_similarity), 4),
        "avg_latency_ms": round(float(avg_latency), 2)
    }

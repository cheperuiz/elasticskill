# pylint: disable=import-error
# pylint: disable=no-name-in-module

from nlp.stopwords import is_valid_term, extra_stopwords
from utils.common import batch_generator


def scroll_ids(es, index, fields=[], keywords=[], operator="or", pagesize=250, scroll_timeout="1m", **kwargs):
    body = {}
    if any(keywords):
        query = {
            "query": " ".join(keywords),
            "operator": operator,
            "type": "cross_fields",
        }
        if len(fields) > 0:
            query["fields"] = fields
        body["query"] = {"multi_match": query}

    result = es.search(
        index=index, scroll=scroll_timeout, body=body, _source_includes=[], size=pagesize, **kwargs
    )
    while True:
        scroll_id = result["_scroll_id"]
        hits = result["hits"]["hits"]
        # Stop after no more docs
        if not hits:
            break
        # Yield each entry
        yield from (hit["_id"] for hit in hits)
        # Continue scrolling
        result = es.scroll(body={"scroll_id": scroll_id, "scroll": scroll_timeout}, **kwargs)


def combine_tags_from_docs(es, index, ids, fields, **kwargs):
    if len(ids) == 0:
        return []
    result = es.mtermvectors(
        index=index, ids=ids, fields=fields, positions=False, offsets=False, term_statistics=True, **kwargs
    )
    yield from (tag for doc in result["docs"] for tag in combined_tags_with_statistics(doc["term_vectors"]))


def combined_tags_with_statistics(term_vectors_by_field):
    tags = (item for field in term_vectors_by_field.values() for item in field["terms"].items())
    yield from tags


def aggregate_tags(tags):
    aggregated_tags = {}
    for term, statistics in tags:
        if is_valid_term(term):
            if term not in aggregated_tags:
                aggregated_tags[term] = statistics
                aggregated_tags[term]["tf-idf"] = statistics["term_freq"] / statistics["doc_freq"]
            else:
                aggregated_tags[term]["term_freq"] += statistics["term_freq"]
                aggregated_tags[term]["tf-idf"] += statistics["term_freq"] / statistics["doc_freq"]
    return aggregated_tags


def sort_by_statistics(terms, ordered_fields=["tf-idf", "ttf", "doc_freq", "term_freq",]):
    tuples = []
    for term, stats in terms.items():
        if stats["doc_freq"] <= 2:
            continue
        l = [stats[field] for field in ordered_fields]
        l.append(term)
        tuples.append(tuple(l))
    tuples.sort(reverse=True)
    return tuples


def tags_from_index(es, index, fields, keywords, operator):
    for ids in batch_generator(
        scroll_ids(es, index=index, fields=fields, keywords=keywords, operator=operator)
    ):
        for tag in combine_tags_from_docs(es, index=index, ids=ids, fields=fields):
            yield tag


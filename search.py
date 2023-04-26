from models import Seing
from fuzzywuzzy import fuzz

def search_db(query):
    results = Seing.query
    results = results.filter(Seing.site.ilike('%' + query + '%'))
    results_list = results.order_by(Seing.site).all()
    return results_list

def fuzz_db(query, sort_col="score"):
    results = Seing.query.all()
    matches = []
    for result in results:
        ratio = fuzz.token_sort_ratio(query, result.site)
        if ratio >= 60:
            matches.append(result)
    ranked_matches = sorted(matches, key=lambda x: getattr(x, sort_col))
    return ranked_matches

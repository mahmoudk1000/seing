from models import Seing
from fuzzywuzzy import fuzz, process

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
        if ratio >= 50:
            matches.append(result)
    if not matches:
        results = search_db(query)
        return results
    ranked_matches = sorted(matches, key=lambda x: getattr(x, sort_col))
    
    return ranked_matches


def fetch_suggestions(query):
    choices = Seing.query.all()
    suggestions = process.extractBests(query, [choice.site for choice in choices], scorer=fuzz.token_sort_ratio,  
  limit=10)

    return [suggestion[0] for suggestion in suggestions]

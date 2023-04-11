from models import Seing

def search_db(query):
    results = Seing.query
    results = results.filter(Seing.site.ilike('%' + query + '%'))
    results_list = results.order_by(Seing.site).all()
    return results_list

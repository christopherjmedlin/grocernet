from grocernet.util.ratings import get_rating_average
from grocernet.vendors.models import Rating

def test_get_rating_average():
    ratings = [5, 5, 5, 3, 3, 3, 4, 2, 5, 2, 3, 1, 2, 3, 4, 5]
    ratings = list(map(lambda r: Rating(r, 1, 1), ratings))
    
    avg = get_rating_average(ratings)
    assert avg == 3.44

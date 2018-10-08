

def get_rating_average(ratings):
    """
    Returns average of 1 or more Rating objects

    Rounds to the hundredth
    """
    ratings = list(map(lambda r: r.rating, ratings))
    return round(sum(ratings)/len(ratings), 2)

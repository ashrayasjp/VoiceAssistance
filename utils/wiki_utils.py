import wikipedia

def search_wikipedia(query):
    try:
        return wikipedia.summary(query, sentences=3)
    except:
        return "I could not find anything on Wikipedia about that."

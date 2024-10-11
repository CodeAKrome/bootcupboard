import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError

class WikipediaEntitySearch:
    def __init__(self):
        self.entity_indicators = {
            'person': ['births', 'deaths'],
            'organization': ['organizations', 'companies', 'institutions'],
            'location': ['countries', 'cities', 'places', 'geography stubs']
        }

    def search_entities(self, query, entity_type, max_results=10):
        try:
            search_results = wikipedia.search(query, results=max_results)
            entities = []

            for result in search_results:
                try:
                    page = wikipedia.page(result, auto_suggest=False)
                    if self._is_entity_type(page.categories, entity_type):
                        entities.append({
                            'title': page.title,
                            'summary': page.summary[:200] + '...' if len(page.summary) > 200 else page.summary
                        })
                except (DisambiguationError, PageError):
                    continue

            return entities
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def _is_entity_type(self, categories, entity_type):
        indicators = self.entity_indicators.get(entity_type.lower(), [])
        return any(any(indicator in category.lower() for indicator in indicators) for category in categories)

# Example usage
if __name__ == "__main__":
    searcher = WikipediaEntitySearch()
    
    entity_type = input("Enter entity type (person, organization, or location): ").lower()
    search_query = input("Enter a search query: ")
    
    if entity_type not in searcher.entity_indicators:
        print("Invalid entity type. Please choose person, organization, or location.")
    else:
        results = searcher.search_entities(search_query, entity_type)
        
        print(f"\n{entity_type.capitalize()}s found:")
        for entity in results:
            print(f"Title: {entity['title']}")
            print(f"Summary: {entity['summary']}")
            print()

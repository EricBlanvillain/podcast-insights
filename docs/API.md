# API Documentation

## QueryProcessor

### `detect_query_type(query: str) -> Dict[str, Any]`
Analyse le type de requête et retourne une classification structurée.

### `calculate_content_relevance(text: str, metadata: Dict[str, Any], query_analysis: Dict[str, Any]) -> float`
Calcule le score de pertinence d'un contenu.

### `generate_response(query: str, results: List[Dict[str, Any]], query_analysis: Dict[str, Any]) -> str`
Génère une réponse basée sur les résultats de recherche.

## UIComponents

### `setup_page()`
Configuration initiale de la page Streamlit.

### `create_controls() -> Dict[str, Any]`
Crée les contrôles de l'interface utilisateur.

### `display_results(results: list, query_analysis: Dict, show_confidence: bool = False)`
Affiche les résultats de recherche.
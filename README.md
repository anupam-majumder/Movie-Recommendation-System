# Auto-Suggest-System

### Building an Autosuggest System

The Autosuggest enhances the search experience through suggest-as-you-type functionality built into the search form. As one starts to enter search terms, the module detects a pause in typing and offers a list of suggested searches. One can then easily pick one of the suggestions or continue refining the suggestions by typing in more of the query. For example, if you type "student" might offer suggestions that include "student form" or "student grade".

## Architecture of Autosuggest System

![Autosuggest](autosuggest.png)

Components of our auto suggest system:

1.Autosuggest Corpus — A static dataset of suggestions that we can offer users. This is computed offline at a scheduled interval and loaded into the engine.

2.Engine — A REST API responsible for Retrieval (getting the list of candidate suggestions for a given user input) and Ranking (ordering the retrieved suggestions).

3.Client — The client application that runs in your browser, asks the engine for results, and displays them to the user.

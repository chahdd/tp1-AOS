# Partie 2 — Service Web SOAP


## En quoi SOAP impose-t-il davantage de structure qu'un script monolithique ?

- **Contrat formel (WSDL)** : le service publie un document WSDL qui décrit
  précisément les opérations disponibles, leurs paramètres et leurs types.
  N'importe quel client peut lire ce contrat pour savoir comment dialoguer
  avec le service, sans lire le code source — impossible avec le monolithe.
- **Typage strict** : chaque paramètre (`Integer`, `Unicode`, `Float`) est
  validé par le protocole SOAP/XML avant même d'arriver dans la logique
  métier.
- **Séparation transport / logique** : le service (`LibraryService`) ne
  contient plus aucun code d'interface graphique ; il est indépendant du
  client qui l'appelle (Postman, SoapUI, une appli mobile...).
- **Enveloppe standardisée** : tous les échanges suivent le même format XML
  (`Envelope`/`Header`/`Body`), ce qui impose une structure commune à tous
  les messages, contrairement à un script où le format des données est
  libre et changeant.

Cette rigueur a un coût : les messages XML sont verbeux et la mise en place
est plus lourde qu'un simple script — ce que la partie 3 (REST) viendra
alléger.

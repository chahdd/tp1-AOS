# Partie 3 — Service Web REST


## Comparaison SOAP vs REST

| Critère              | SOAP                                                             | REST                                                                 |
|-----------------------|-------------------------------------------------------------------|------------------------------------------------------------------------|
| **Lisibilité**        | Messages XML verbeux (enveloppe, header, body à chaque appel)     | JSON léger et lisible directement                                     |
| **Facilité d'usage**  | Nécessite un client SOAP (Postman/SoapUI en mode XML) et de connaître l'enveloppe | Utilise les verbes HTTP standards (GET/POST/PUT/DELETE), testable au navigateur ou avec `curl` |
| **Contrat**           | WSDL, formel et rigide, généré/maintenu séparément                | OpenAPI/Swagger généré automatiquement à partir du code (`/docs`)     |
| **Intégration**       | Plus lourd à intégrer côté web/mobile, mais standardisé pour des échanges d'entreprise fiables (transactions, sécurité WS-*) | S'intègre nativement au web et au mobile, format JSON consommé partout |
| **Validation**        | Typage XML strict via le contrat                                  | Validation déclarative via les schémas Pydantic                        |

En résumé : SOAP apporte un contrat très strict et des garanties utiles pour
des systèmes d'entreprise critiques, mais au prix de la légèreté. REST est
plus simple, plus rapide à mettre en œuvre et mieux adapté aux clients
web/mobile modernes — ce qui explique pourquoi BiblioTech termine son
évolution avec cette architecture.

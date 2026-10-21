# Partie 1 — Version monolithique



## Limites de l'approche monolithique

1. **Couplage fort** : la connexion DB, le modèle, la logique métier (CRUD,
   validation) et l'interface graphique sont dans le même fichier. Modifier
   une partie (ex. changer la validation) risque d'impacter les autres.
2. **Pas réutilisable** : si une appli mobile ou un site web veut aussi gérer
   les livres, il faudrait dupliquer tout le code — il n'y a aucune interface
   standard (pas d'API) pour y accéder de l'extérieur.
3. **Difficile à tester** : la logique métier est mélangée à l'UI PyQt5, donc
   on ne peut pas facilement tester `create_book()` sans lancer toute
   l'application graphique.
4. **Déploiement monobloc** : on ne peut pas mettre à jour ou faire évoluer
   une seule fonctionnalité (ex. la validation) sans redéployer tout le
   programme.
5. **Pas de scalabilité indépendante** : impossible de faire tourner "plus
   d'instances" juste de la partie métier sans dupliquer toute l'application,
   GUI comprise.
6. **Un seul langage/plateforme client** : seul un utilisateur qui lance ce
   script Python avec PyQt5 installé peut utiliser le système.

C'est exactement ce que corrige une architecture orientée services (SOAP puis
REST) : exposer la logique métier via un contrat standard, indépendant du
client.

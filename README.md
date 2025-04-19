# Python Game Server Base 🎮

## Description 📜
`Python Game Server Base` est un projet de jeu multijoueur utilisant Python et des sockets. Ce projet comprend un **serveur** et un **client** permettant aux joueurs de se connecter, de rejoindre une partie et de se déplacer sur une grille.

- **Serveur** : Gère les connexions des joueurs, leurs positions, et le lancement du jeu 🖥️.
- **Client** : Permet à l'utilisateur de se connecter, de se déplacer sur une grille, et de participer à la partie 🎮.

---

## Fonctionnement ⚙️

### Serveur (`serveur.py`) 🌐
Le serveur attend les connexions des clients, gère les requêtes entrantes et maintient l'état du jeu.

#### Paquets 📦
Les paquets envoyés par les clients et traités par le serveur sont formatés comme suit : `0x[code]...`. Chaque type de paquet est associé à une action spécifique sur le serveur.

| Code | Signification       | Action                                |
|------|---------------------|----------------------------------------|
| `0x1` | Connexion           | Ajoute un joueur ➕                    |
| `0x2` | Déconnexion         | Retire un joueur ❌                    |
| `0x3` | Liste des joueurs   | Envoie la liste des autres joueurs 📋 |
| `0x4` | Requête de position | Envoie la position actuelle 📍        |
| `0x5` | Mise à jour de position | Modifie la position d’un joueur 🔄 |
| `0x466f756e64` | Démarrage du jeu | Le jeu commence 🚀              |

---

## Client (`client.py`) 💻

Le client permet :
- La connexion au serveur avec un nom d’utilisateur unique 🔑
- Le déplacement dans une grille 9x9 à l’aide des touches clavier 🎮
- La réception et l’envoi de paquets pour synchroniser les positions 📡

### Commandes Clavier 🎮

| Touche | Direction | Effet     |
|--------|-----------|-----------|
| `z`    | Haut      | Y - 1 ⬆️  |
| `s`    | Bas       | Y + 1 ⬇️  |
| `q`    | Gauche    | X - 1 ⬅️  |
| `d`    | Droite    | X + 1 ➡️  |

---

## Format des Paquets 📨

### 1. Connexion d’un joueur (`0x1`) 🔑
```text
0x1<NomUtilisateur>
Exemple : 0x1John

Ajoute le joueur si le nom est unique.
Renvoie 0x1796573 si succès, 0x16E6F si échec.
```

### 2. Déconnexion (0x2) ❌
```
0x2
Exemple : 0x2

Déconnecte le joueur et ferme la session.
Aucune réponse attendue.
```

### 3. Liste des joueurs (0x3) 📋
```
0x3<NomUtilisateur>
Exemple : 0x3John

Retourne une liste des autres joueurs connectés, séparés par virgule.
Réponse : 0x3Alice,Bob,Charlie

```

### 4 .Requête de position (0x4) 📍
```
0x4<NomUtilisateur>
Exemple : 0x4John

Renvoie la position du joueur.
Réponse : 0x4<2>AND<5>  → X=2, Y=5
```

### 5. Mise à jour de position (0x5) 🔄
```
0x5<X>AND<Y>AND<NomUtilisateur>
Exemple : 0x5<4>AND<6>AND<John>

Met à jour les coordonnées du joueur dans la grille.
Aucune réponse attendue.
```

### 6. Démarrage du jeu (0x466f756e64) 🚀
```
0x466f756e64
Exemple : 0x466f756e64

Envoyé automatiquement par le serveur lorsque deux joueurs sont connectés.
Déclenche le début de la partie.
```

## Installation et Dépendances 💾
### Prérequis

#### ●Python 3.x

### Bibliothèques :
```
 ●socket
 ●keyboard
 ●colorama
```
## Lancement 🚀
### Lancer le serveur
#### ```python serveur.py```
### Lancer un client
#### ```python client.py```

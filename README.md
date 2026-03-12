# Find My Loved One -APi docs

<p>
Notre Api consitue la partie backend de l'application 
<i><b>find my loved</b></i> one 
Elle a pour but de permettre aux personnes disparues 
d'êtres retrouvées facilement.
</p>
<br/>

## Les endpoints

### 1 - Authentification

api-url ``http://localhost/login``
Il s'agit d'une requète type post. Dans le corp de la requete, 
vous metrez le login et le mot de passe comme suit:

```json
{
    "login": "toko.michel",
    "password": "toko"
}
```

Il s'agit là du mot de passe d'un utilisateur existant déjà dans la base de données

* **Authentification à django admin**: les identifiants sont les suivant:

```json
{
  "login": "toko",
  "password": "toko"
}
```
<br/>

Après l'authentification effectuée, le reste des requêtes que vous effectuerez se fera
en insérant le jwt token dans les headers de la requête.

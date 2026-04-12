# Find My Loved One - API docs

<p>
Notre Api constitue la partie backend de l'application 
<i><b>find my loved</b></i> one 
Elle a pour but de permettre aux personnes disparues 
d'êtres retrouvés facilement.
</p>
<br/>

## Les endpoints

### 1 - Création de compte

api-url: "http://localhost/create/". Pour celà, il faut lui passer les éléments structurés de la façon suivante:
````json
{
    "first_name": "Toko",
    "last_name": "Michel",
    "login": "toko.michel",
    "password": "toko",
    "email": "toko.michel@example.com",
    "first_phone": "0785473124",
    "second_phone": "0785473124",
    "city": "Limoges",
    "adresse": "12 rue des Lilas"
}
````

### 2 - Authentification

Api-url ``http://localhost/login``
Il s'agit d'une requète type post. Dans le corp de la requete, 
vous mettrez le login et le mot de passe comme suit :

```json
{
    "login": "toko.michel",
    "password": "toko"
}
```

Il s'agit là du mot de passe d'un utilisateur existant déjà dans la base de données

* **Authentification à django admin** : les identifiants sont les suivants :

```json
{
  "login": "toko",
  "password": "toko"
}
```
<br/>

Après l'authentification effectuée, le reste des requêtes que vous effectuerez se fera
en insérant le jwt token dans les headers de la requête.

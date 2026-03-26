# CM — Introduction à BGP

## 1. Pourquoi BGP ?

Dans un réseau d’entreprise, **OSPF** suffit pour le routage interne.

Dès que l’on échange des routes avec un **réseau extérieur** :

- fournisseur d’accès ;
- autre organisation ;
- second accès WAN ;
- interconnexion multi-sites étendue ;

on utilise généralement **BGP**.

**Idée clé :**
OSPF gère l’intérieur d’un domaine.
BGP gère les échanges **entre domaines de routage**.

---

## 2. Positionnement d’OSPF et de BGP

```{mermaid}
flowchart LR
    subgraph AS65000[AS 65000 - Entreprise]
        R1[R1]
        R2[R2]
        R3[R3]
        R1 ---|OSPF| R2
        R2 ---|OSPF| R3
        R1 ---|OSPF| R3
    end

    ISP1[ISP1 - AS 65100]
    ISP2[ISP2 - AS 65200]

    R1 -->|eBGP| ISP1
    R2 -->|eBGP| ISP2
```

**Lecture :**

- **OSPF** est utilisé **dans** l’entreprise ;
- **eBGP** est utilisé **entre** l’entreprise et les FAI.

---

## 3. Définition de BGP

**BGP** signifie **Border Gateway Protocol**.

C’est un protocole de routage :

- de **bordure** ;
- orienté **politique de routage** ;
- utilisé entre **systèmes autonomes**.

BGP ne cherche pas uniquement le “plus court chemin”.
Il permet aussi de choisir :

- une sortie principale ;
- une sortie de secours ;
- un chemin préféré ;
- un voisin à privilégier.

---

## 4. Qu’est-ce qu’un AS ?

Un **AS** (_Autonomous System_) est :

- un ensemble de routeurs ;
- administrés par une même entité ;
- partageant une politique de routage cohérente.

Exemple dans une maquette :

- **AS 65000** : entreprise ;
- **AS 65100** : FAI 1 ;
- **AS 65200** : FAI 2.

**Le numéro d’AS n’est pas une adresse IP.**
C’est un **identifiant logique de domaine de routage BGP**.

---

## 5. Pourquoi des AS différents ?

```{mermaid}
flowchart LR
    A[AS 65000\nEntreprise] --> B[AS 65100\nISP1]
    A --> C[AS 65200\nISP2]
```

Quand deux voisins BGP appartiennent à des **AS différents** :

- on parle de **eBGP**.

Quand deux voisins BGP appartiennent au **même AS** :

- on parle de **iBGP**.

---

## 6. iBGP et eBGP

| Type | Signification           | Cas typique                                 |
| ---- | ----------------------- | ------------------------------------------- |
| iBGP | BGP interne au même AS  | Entre deux routeurs d’une même organisation |
| eBGP | BGP entre AS différents | Entre entreprise et fournisseur             |

Dans une architecture d’entreprise classique :

- **OSPF** pour le routage interne ;
- **eBGP** vers le ou les FAI.

---

## 7. Où se situe BGP dans le modèle OSI ?

BGP est un protocole **applicatif**.

Il fonctionne :

- au-dessus de **TCP** ;
- sur le **port 179**.

```{mermaid}
flowchart TD
    L7[Couche 7 - Application\nBGP]
    L4[Couche 4 - Transport\nTCP port 179]
    L3[Couche 3 - Réseau\nIP]
    L2[Couche 2 - Liaison\nEthernet]

    L7 --> L4 --> L3 --> L2
```

**Point important :**
les informations d’AS sont transportées dans les **messages BGP**, pas dans l’en-tête IP ni dans l’en-tête Ethernet.

---

## 8. Encapsulation d’un échange BGP

```{mermaid}
flowchart TD
    E[Trame Ethernet]
    IP[Paquet IP]
    TCP[Segment TCP\nPort 179]
    BGP[Message BGP\nOPEN / UPDATE / KEEPALIVE]
    AS[Informations BGP\nASN, AS_PATH, attributs]

    E --> IP --> TCP --> BGP --> AS
```

**Lecture :**

- Ethernet transporte IP ;
- IP transporte TCP ;
- TCP transporte BGP ;
- BGP transporte les informations de routage inter-AS.

---

## 9. Les principaux messages BGP

BGP repose notamment sur les messages suivants :

| Message      | Rôle                              |
| ------------ | --------------------------------- |
| OPEN         | ouverture de session BGP          |
| KEEPALIVE    | maintien de la session            |
| UPDATE       | annonce ou retrait de routes      |
| NOTIFICATION | signalement d’erreur et fermeture |

---

## 10. Logique d’établissement d’une session BGP

```{mermaid}
sequenceDiagram
    participant R1 as Routeur entreprise
    participant ISP as Routeur FAI

    R1->>ISP: TCP 179
    ISP-->>R1: TCP 179 établi
    R1->>ISP: BGP OPEN
    ISP->>R1: BGP OPEN
    R1->>ISP: KEEPALIVE
    ISP->>R1: KEEPALIVE
    R1->>ISP: UPDATE
    ISP->>R1: UPDATE
```

Pour qu’une session BGP fonctionne, il faut notamment :

- une connectivité IP ;
- un voisin correctement déclaré ;
- le bon numéro d’AS du voisin.

---

## 11. Exemple de voisinage eBGP

```{mermaid}
flowchart LR
    R1[R1\nAS 65000\n172.16.1.1/30] <-->|eBGP| ISP1[ISP1\nAS 65100\n172.16.1.2/30]
```

Exemple de configuration :

```text
router bgp 65000
 neighbor 172.16.1.2 remote-as 65100
```

Cela signifie :

- le routeur local appartient à **l’AS 65000** ;
- le voisin `172.16.1.2` appartient à **l’AS 65100**.

---

## 12. Rôle de la commande `network`

Exemple :

```text
router bgp 65000
 network 10.1.2.0 mask 255.255.255.0
```

Cette commande demande à BGP d’annoncer ce préfixe **si la route existe déjà dans la table de routage**.

**Idée clé :**
BGP n’invente pas une route.
Il annonce un réseau déjà connu localement.

---

## 13. Exemple d’architecture avec deux FAI

```{mermaid}
flowchart LR
    subgraph ENT[AS 65000 - Entreprise]
        R1[R1\nSortie principale]
        R2[R2\nSortie secondaire]
        R3[R3\nInterne]
        R1 ---|OSPF| R2
        R2 ---|OSPF| R3
        R1 ---|OSPF| R3
    end

    ISP1[ISP1\nAS 65100]
    ISP2[ISP2\nAS 65200]
    NET1[203.0.113.0/24]
    NET2[198.51.100.0/24]

    R1 -->|eBGP| ISP1 --> NET1
    R2 -->|eBGP| ISP2 --> NET2
```

Cette architecture permet :

- une sortie principale ;
- une sortie de secours ;
- une première approche de la résilience WAN.

---

## 14. OSPF et BGP : comparaison rapide

| Critère         | OSPF                        | BGP                  |
| --------------- | --------------------------- | -------------------- |
| Usage principal | routage interne             | routage externe      |
| Domaine         | à l’intérieur d’un AS       | entre AS             |
| Logique         | meilleure route interne     | politique de routage |
| Position        | cœur du réseau d’entreprise | bordure du réseau    |
| Transport       | directement sur IP          | sur TCP 179          |

---

## 15. Attributs BGP : première idée

BGP prend ses décisions à partir d’**attributs**.

Parmi les plus connus :

- **AS_PATH** ;
- **NEXT_HOP** ;
- **LOCAL_PREF** ;
- **MED**.

Dans une première approche, il faut retenir surtout :

- BGP ne choisit pas une route seulement sur la distance ;
- il applique une **politique de décision**.

---

## 16. AS_PATH

L’attribut **AS_PATH** contient la liste des AS traversés.

Exemple :

```text
203.0.113.0/24   AS_PATH: 65100
198.51.100.0/24  AS_PATH: 65200
```

Si une route traverse plusieurs AS :

```text
AS_PATH: 65200 65150 65100
```

Cela sert notamment à :

- connaître l’origine d’une route ;
- détecter certaines boucles ;
- contribuer au choix du chemin.

---

## 17. Pourquoi BGP est utile pour la redondance WAN

Avec deux sorties WAN, BGP permet :

- d’établir deux voisinages externes ;
- de recevoir ou annoncer des routes par deux chemins ;
- de définir une sortie principale et une sortie secondaire.

```{mermaid}
flowchart LR
    ENT[Entreprise\nAS 65000]
    ISP1[ISP1\nAS 65100]
    ISP2[ISP2\nAS 65200]

    ENT -->|Chemin préféré| ISP1
    ENT -->|Secours| ISP2
```

---

## 18. Rôle respectif d’OSPF et de BGP dans une entreprise

```{mermaid}
flowchart LR
    subgraph LAN[Entreprise]
        R1[R1]
        R2[R2]
        R3[R3]
        SW[LAN / VLAN / OSPF]
        SW --- R1
        SW --- R2
        SW --- R3
    end

    FAI1[FAI 1]
    FAI2[FAI 2]

    R1 -->|eBGP| FAI1
    R2 -->|eBGP| FAI2
```

- **OSPF** diffuse les routes internes dans l’entreprise ;
- **BGP** gère les échanges avec les réseaux extérieurs.

---

## 19. Exemple de flux de décision

1. Le routeur interne veut joindre un réseau externe.
2. La route sortante dépend de la politique BGP.
3. La sortie choisie est transmise au routeur de bordure.
4. Le trafic emprunte le lien WAN correspondant.

```{mermaid}
flowchart LR
    PC[Poste interne] --> RINT[Routeur interne]
    RINT -->|OSPF| REDGE[Routeur de bordure]
    REDGE -->|BGP| ISP[FAI]
    ISP --> NET[Réseau externe]
```

---

## 20. Vérifications de base sur Cisco

Quelques commandes utiles :

```text
show ip bgp summary
show ip bgp
show ip route bgp
show running-config | section router bgp
```

À vérifier :

- voisinage **Established** ;
- préfixes appris ;
- préfixes annoncés ;
- cohérence de l’AS du voisin.

---

## 21. Lecture de `show ip bgp summary`

Exemple attendu :

```text
Neighbor        V    AS MsgRcvd MsgSent State/PfxRcd
172.16.1.2      4 65100      25      22        1
```

Points à lire :

- **Neighbor** : IP du voisin BGP ;
- **AS** : AS du voisin ;
- **State/PfxRcd** : session établie et nombre de préfixes reçus.

Si la session n’est pas établie, on voit un état comme :

- Idle ;
- Active ;
- Connect ;
- OpenSent ;
- OpenConfirm.

---

## 22. Bonnes pratiques de base

- utiliser une numérotation d’AS cohérente ;
- documenter les rôles des routeurs de bordure ;
- séparer clairement routage interne et routage externe ;
- vérifier l’adressage des liens WAN ;
- contrôler le bon AS du voisin ;
- tester la résilience en simulant une panne.

---

## 23. À retenir

- **BGP** est un protocole de routage **externe**.
- Il échange des routes **entre AS**.
- **eBGP** relie des voisins de **numéros d’AS différents**.
- Le numéro d’AS est un **identifiant logique de domaine de routage**.
- Les informations BGP sont transportées dans des **messages applicatifs**, au-dessus de **TCP 179**.
- En entreprise, **OSPF** gère l’interne et **BGP** la bordure WAN.
- BGP est particulièrement utile quand il existe **plusieurs sorties externes**.

---

## 24. Questions de révision

1. Quelle différence entre OSPF et BGP ?
2. Qu’est-ce qu’un AS ?
3. Quelle différence entre iBGP et eBGP ?
4. Où se situe BGP dans l’encapsulation réseau ?
5. Pourquoi BGP utilise-t-il TCP ?
6. Que transporte l’attribut AS_PATH ?
7. Pourquoi une entreprise multi-homée a-t-elle intérêt à utiliser BGP ?
8. Pourquoi BGP est-il dit orienté “politique de routage” ?

---

## 25. Synthèse finale

BGP intervient lorsque le réseau dépasse le simple routage interne.

Il permet à une entreprise de dialoguer avec des réseaux extérieurs en tenant compte :

- de l’origine des routes ;
- des voisins externes ;
- des politiques de sortie ;
- des besoins de redondance.

Dans une architecture moderne :

- **OSPF** structure l’interne ;
- **BGP** gère l’extérieur ;
- les deux se complètent pour former une architecture WAN robuste et lisible.

# CM — OSPF et ECMP

## 1. Pourquoi un protocole de routage interne ?

Dans un réseau d’entreprise composé de plusieurs routeurs, les routes statiques deviennent rapidement difficiles à maintenir.

Un protocole de routage interne permet :

- d’échanger automatiquement les routes ;
- d’adapter la table de routage aux évolutions ;
- de réduire les erreurs manuelles ;
- de converger après une panne ou un changement de topologie.

**OSPF** répond à ce besoin dans de nombreuses architectures d’entreprise.

---

## 2. Définition d’OSPF

**OSPF** signifie **Open Shortest Path First**.

C’est un protocole de routage dynamique :

- **interne** à un système autonome ;
- à **état de liens** (_link-state_) ;
- fondé sur l’algorithme de **Dijkstra**.

OSPF construit une vision logique de la topologie, puis calcule les meilleurs chemins.

---

## 3. Positionnement d’OSPF

```{mermaid}
flowchart LR
    subgraph AS[AS entreprise]
        R1[Routeur 1]
        R2[Routeur 2]
        R3[Routeur 3]
        R4[Routeur 4]
        R1 --- R2
        R2 --- R3
        R3 --- R4
        R1 --- R4
    end
```

OSPF est utilisé **à l’intérieur** d’un réseau d’entreprise ou d’un système autonome.

Il ne sert pas à échanger des routes entre organisations distinctes. Pour cela, on utilise généralement **BGP**.

---

## 4. OSPF : protocole à état de liens

Dans un protocole à vecteur de distance, un routeur connaît surtout :

- une destination ;
- une métrique ;
- un prochain saut.

Dans un protocole à état de liens, un routeur apprend aussi :

- quels liens existent ;
- quels réseaux sont connectés ;
- quelle est la structure logique de la topologie.

Chaque routeur calcule ensuite localement son meilleur chemin.

---

## 5. Vue générale du fonctionnement

```{mermaid}
flowchart TD
    A[Découverte des voisins] --> B[Échange d’informations de topologie]
    B --> C[Base de données d’état de liens]
    C --> D[Calcul SPF]
    D --> E[Table de routage]
```

En simplifiant :

1. les routeurs découvrent leurs voisins ;
2. ils échangent des informations de topologie ;
3. ils construisent une base de données cohérente ;
4. ils calculent les meilleurs chemins ;
5. ils installent les routes dans leur table.

---

## 6. Les voisins OSPF

Deux routeurs OSPF reliés sur un même segment peuvent devenir **voisins**.

Pour cela, ils doivent notamment être cohérents sur :

- l’activation d’OSPF sur l’interface ;
- l’aire OSPF ;
- les paramètres de temporisation essentiels ;
- le type de réseau ;
- l’adressage compatible sur le lien.

La relation de voisinage permet ensuite l’échange des informations de topologie.

---

## 7. Les paquets Hello

OSPF utilise des paquets **Hello** pour :

- découvrir les voisins ;
- maintenir la relation de voisinage ;
- détecter la perte d’un voisin.

```{mermaid}
sequenceDiagram
    participant R1 as Routeur A
    participant R2 as Routeur B

    R1->>R2: Hello
    R2->>R1: Hello
    R1->>R2: Hello périodique
    R2->>R1: Hello périodique
```

Si les paquets Hello cessent d’être reçus pendant un certain délai, le voisin est considéré comme perdu.

---

## 8. OSPF et le modèle OSI

OSPF n’utilise pas TCP ni UDP.

C’est un protocole de routage directement transporté sur IP.

```{mermaid}
flowchart TD
    L7[Application utilisateur]
    L4[Transport\nTCP / UDP]
    L3[Couche réseau\nIP + OSPF]
    L2[Couche liaison\nEthernet]

    L7 --> L4 --> L3 --> L2
```

**Point important :**
OSPF fonctionne au niveau du **plan de contrôle**, directement sur IP.

---

## 9. La métrique OSPF : le coût

OSPF choisit les chemins à partir d’un **coût**.

Le coût d’un chemin est la somme des coûts des interfaces traversées.

En simplifiant :

- plus le coût est faible,
- plus le chemin est attractif.

Le coût dépend généralement de la bande passante de référence et de la bande passante de l’interface.

---

## 10. Exemple de calcul de chemin

```{mermaid}
flowchart LR
    R1[R1] -- coût 10 --> R2[R2]
    R2 -- coût 10 --> R4[R4]
    R1 -- coût 5 --> R3[R3]
    R3 -- coût 30 --> R4[R4]
```

Deux chemins existent entre R1 et R4 :

- R1 → R2 → R4 : coût total 20 ;
- R1 → R3 → R4 : coût total 35.

OSPF choisit donc le premier chemin.

---

## 11. La base de données d’état de liens

Chaque routeur OSPF maintient une **base de données d’état de liens**.

Elle contient une représentation logique de la topologie OSPF connue.

Cette base n’est pas la table de routage.

Il faut distinguer :

- la **base d’état de liens** : vision de la topologie ;
- la **table de routage** : chemins effectivement utilisés.

---

## 12. Dijkstra et SPF

OSPF applique l’algorithme **SPF** (_Shortest Path First_), dérivé de Dijkstra.

À partir de la topologie connue, chaque routeur calcule :

- le plus court chemin logique ;
- vers chaque destination ;
- selon la métrique OSPF.

```{mermaid}
flowchart TD
    T[Topologie OSPF connue] --> S[Calcul SPF]
    S --> R[Routes installées]
```

---

## 13. OSPF et les aires

OSPF peut être découpé en **aires**.

Une aire permet de :

- structurer le domaine OSPF ;
- limiter certaines diffusions d’informations ;
- améliorer l’évolutivité.

Dans une architecture simple, on utilise souvent une seule aire :

- **area 0**

```{mermaid}
flowchart LR
    subgraph Area0[Area 0]
        R1[R1]
        R2[R2]
        R3[R3]
    end
```

---

## 14. L’aire backbone

L’**aire 0** est l’aire centrale d’OSPF.

Dans une architecture multi-aires :

- les autres aires doivent être reliées logiquement à l’aire 0 ;
- l’aire 0 sert de colonne vertébrale au domaine OSPF.

Dans une approche pédagogique simple, retenir surtout :

- **area 0 = aire principale**

---

## 15. Interfaces passives

Une interface OSPF passive :

- annonce le réseau connecté ;
- mais n’envoie pas de paquets Hello ;
- et ne forme donc pas de voisinage OSPF.

Cette bonne pratique est utile sur :

- les réseaux utilisateurs ;
- les LAN où aucun voisin OSPF n’est attendu.

---

## 16. Pourquoi rendre certaines interfaces passives ?

```{mermaid}
flowchart LR
    R[Routeur] --> LAN[LAN utilisateurs]
    R --> T[Transit vers autre routeur]
```

Sur le LAN utilisateurs :

- le réseau doit souvent être annoncé ;
- mais aucun voisin OSPF n’est attendu.

Sur le transit inter-routeurs :

- le réseau doit être annoncé ;
- **et** le voisinage doit se former.

Donc :

- interface LAN → souvent **passive** ;
- interface transit → **non passive**.

---

## 17. Router ID et loopback

Chaque routeur OSPF possède un **router-id**.

C’est un identifiant logique du routeur dans le protocole.

Il est recommandé de le fixer explicitement, souvent à partir d’une **loopback**.

Pourquoi ?

- stabilité ;
- lisibilité ;
- indépendance vis-à-vis d’une interface physique.

---

## 18. OSPF sur sous-interfaces et trunks

OSPF peut fonctionner sur :

- des interfaces physiques ;
- des sous-interfaces 802.1Q ;
- des réseaux de transit transportés sur trunk.

Cela permet par exemple :

- de mutualiser une infrastructure physique ;
- de transporter plusieurs segments de transit ;
- de former des voisinages OSPF sur des sous-interfaces distinctes.

```{mermaid}
flowchart LR
    R1[Routeur A] ---|Trunk 802.1Q| SW[Switch de transit]
    SW ---|Trunk 802.1Q| R2[Routeur B]
```

---

## 19. OSPF et redondance

OSPF est particulièrement utile dans une architecture comportant :

- plusieurs routeurs ;
- plusieurs chemins ;
- des liens de secours.

En cas de perte d’un lien ou d’un voisin, le protocole recalcule les chemins.

```{mermaid}
flowchart LR
    R1[R1] --- R2[R2]
    R2 --- R4[R4]
    R1 --- R3[R3]
    R3 --- R4
```

Si un chemin tombe, OSPF peut basculer vers un autre chemin disponible.

---

## 20. Qu’est-ce que l’ECMP ?

**ECMP** signifie **Equal-Cost Multi-Path**.

Il s’agit de la capacité d’un routeur à installer **plusieurs chemins de coût égal** vers une même destination.

Autrement dit :

- plusieurs routes ;
- même métrique ;
- même destination ;
- utilisables simultanément.

---

## 21. Exemple d’ECMP

```{mermaid}
flowchart LR
    R1[R1] -- coût 10 --> R2[R2]
    R2 -- coût 10 --> R4[R4]
    R1 -- coût 10 --> R3[R3]
    R3 -- coût 10 --> R4[R4]
```

Vers R4, R1 dispose de deux chemins :

- R1 → R2 → R4 : coût total 20 ;
- R1 → R3 → R4 : coût total 20.

Les deux chemins ont le **même coût**.

OSPF peut donc installer les deux routes en **ECMP**.

---

## 22. Ce que permet l’ECMP

L’ECMP permet :

- une meilleure utilisation de plusieurs chemins disponibles ;
- une répartition de charge réseau ;
- une tolérance de panne plus rapide si un chemin disparaît.

**Point important :**
L’ECMP ne remplace pas un load balancer applicatif.
Il s’agit d’une logique de **routage**, pas d’une logique de service L7.

---

## 23. Répartition avec ECMP

Selon les équipements, la répartition peut reposer sur :

- du **per-packet** ;
- du **per-flow** ;
- plus souvent, une logique de hachage pour garder une certaine cohérence de flux.

```{mermaid}
flowchart TD
    F[Flux à router] --> H[Hachage / sélection]
    H --> C1[Chemin 1]
    H --> C2[Chemin 2]
```

En pratique, on évite souvent le vrai per-packet sur certains réseaux sensibles, pour ne pas désordonner les flux.

---

## 24. OSPF et ECMP : relation

OSPF peut produire de l’ECMP lorsque plusieurs chemins vers une destination ont exactement le même coût total.

OSPF ne “cherche” pas à équilibrer de manière arbitraire.
Il constate simplement qu’il existe plusieurs **meilleurs chemins équivalents**.

---

## 25. Exemple de topologie avec redondance et ECMP

```{mermaid}
flowchart LR
    A[Site A] --> R1[R1]
    R1 --> R2[R2]
    R1 --> R3[R3]
    R2 --> R4[R4]
    R3 --> R4
    R4 --> B[Site B]
```

Si les coûts sont équilibrés :

- R1 peut utiliser deux chemins de coût égal ;
- l’ECMP est possible ;
- le trafic peut être réparti entre les deux routes.

---

## 26. OSPF et convergence

La **convergence** désigne le temps nécessaire pour que les routeurs :

- détectent un changement ;
- recalculent la topologie ;
- mettent à jour leur table de routage.

OSPF converge après :

- perte d’un voisin ;
- perte d’un lien ;
- apparition d’un nouveau chemin.

Une topologie simple et bien structurée favorise une convergence plus lisible.

---

## 27. OSPF et bonnes pratiques

Quelques bonnes pratiques classiques :

- fixer le **router-id** ;
- utiliser une **loopback** ;
- rendre les interfaces LAN **passives** ;
- réserver les voisinages OSPF aux liens de transit ;
- utiliser un plan d’adressage lisible ;
- documenter les coûts si des ajustements sont faits.

---

## 28. Vérifications usuelles sur Cisco

Commandes fréquemment utilisées :

```text
show ip ospf neighbor
show ip ospf interface brief
show ip route ospf
show ip ospf
```

Ces commandes permettent de vérifier :

- les voisins ;
- les interfaces OSPF actives ;
- les routes apprises ;
- l’état général du processus OSPF.

---

## 29. Lecture d’un voisinage

Exemple attendu :

```text
Neighbor ID     Pri   State           Dead Time   Address     Interface
10.255.0.2        1   FULL/DR         00:00:32    10.0.0.2    Gi0/1
```

Éléments utiles :

- **Neighbor ID** : identifiant du voisin ;
- **State** : état du voisinage ;
- **Address** : adresse du voisin sur le lien ;
- **Interface** : interface locale concernée.

---

## 30. Ce qu’il faut retenir sur OSPF

- OSPF est un protocole de routage **interne**.
- Il est de type **link-state**.
- Il repose sur les **Hello**, la base de topologie et le calcul **SPF**.
- Il choisit les chemins selon un **coût**.
- Il peut fonctionner sur interfaces physiques ou sous-interfaces.
- Il s’intègre bien aux architectures redondées.

---

## 31. Ce qu’il faut retenir sur ECMP

- ECMP signifie **Equal-Cost Multi-Path**.
- Il apparaît lorsque plusieurs chemins ont le **même coût**.
- Il permet d’utiliser plusieurs routes simultanément.
- Il améliore la souplesse et la résilience du routage.
- Il reste un mécanisme de **couche réseau**, pas un équilibrage applicatif.

---

## 32. Synthèse générale

Dans une architecture d’entreprise :

- **OSPF** sert à échanger automatiquement les routes internes ;
- il maintient une vision logique de la topologie ;
- il choisit les meilleurs chemins à partir du coût ;
- et, lorsque plusieurs chemins sont équivalents, il peut produire de l’**ECMP**.

```{mermaid}
flowchart LR
    TOPO[Topologie interne] --> OSPF[OSPF]
    OSPF --> SPF[Calcul SPF]
    SPF --> RT[Table de routage]
    RT --> ECMP[ECMP si coûts égaux]
```

OSPF constitue ainsi une base solide pour construire un réseau :

- dynamique ;
- lisible ;
- redondé ;
- capable de converger après une panne.

---

## 33. Questions de révision

1. Quelle différence entre routage statique et routage dynamique ?
2. Pourquoi OSPF est-il qualifié de protocole à état de liens ?
3. À quoi servent les paquets Hello ?
4. Quelle différence entre base de topologie et table de routage ?
5. Que représente le coût OSPF ?
6. Pourquoi rendre certaines interfaces passives ?
7. Quel est l’intérêt d’un router-id fixe ?
8. Qu’est-ce que l’ECMP ?
9. À quelle condition OSPF peut-il installer plusieurs chemins vers une même destination ?
10. Pourquoi l’ECMP ne remplace-t-il pas un load balancer applicatif ?

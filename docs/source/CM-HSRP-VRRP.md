# CM — Redondance de passerelle : HSRP, VRRP, GLBP et ouverture vers les approches modernes

## 1. Pourquoi une redondance de passerelle ?

Dans un réseau local, les hôtes utilisent une **passerelle par défaut** pour joindre les réseaux extérieurs à leur sous-réseau.

Si cette passerelle repose sur un **seul routeur** :

- la panne du routeur coupe l’accès au reste du réseau ;
- les VLAN restent présents ;
- mais les hôtes ne savent plus sortir de leur segment local.

Ce type de panne correspond à un **SPOF** (_Single Point of Failure_).

---

## 2. Le problème de la passerelle unique

```{mermaid}
flowchart LR
    PC1[Hôte VLAN A] --> GW[Passerelle unique]
    PC2[Hôte VLAN A] --> GW
    PC3[Hôte VLAN A] --> GW
    GW --> NET[Autres réseaux]
```

Tant que la passerelle est disponible :

- les hôtes sortent normalement du VLAN.

Si la passerelle tombe :

- les hôtes gardent leur adresse IP ;
- le switch continue à fonctionner ;
- mais la sortie du VLAN est perdue.

---

## 3. Principe général des FHRP

Les protocoles de redondance de premier saut sont appelés **FHRP** (_First Hop Redundancy Protocols_).

Leur objectif est de présenter aux hôtes :

- une **passerelle virtuelle unique** ;
- alors que plusieurs routeurs existent en arrière-plan.

Les trois technologies classiques à connaître sont :

- **HSRP** ;
- **VRRP** ;
- **GLBP**.

---

## 4. Idée commune à HSRP, VRRP et GLBP

```{mermaid}
flowchart LR
    PC1[Hôte 1] --> VIP[IP virtuelle de passerelle]
    PC2[Hôte 2] --> VIP
    PC3[Hôte 3] --> VIP

    VIP --> R1[Routeur 1]
    VIP --> R2[Routeur 2]
```

Les hôtes ne pointent pas vers l’adresse d’un routeur physique.
Ils utilisent une **IP virtuelle**.

Ensuite, selon le protocole :

- un routeur prend le rôle principal ;
- un autre prend le secours ;
- ou plusieurs routeurs partagent la charge.

---

## 5. Vocabulaire de base

| Terme                    | Signification                                        |
| ------------------------ | ---------------------------------------------------- |
| Passerelle physique      | adresse IP réelle d’un routeur                       |
| Passerelle virtuelle     | adresse IP utilisée par les hôtes                    |
| Routeur actif / maître   | routeur qui traite effectivement le trafic           |
| Routeur standby / backup | routeur prêt à prendre le relais                     |
| Préemption               | reprise du rôle principal par le routeur prioritaire |

---

## 6. Exemple de logique de fonctionnement

```{mermaid}
flowchart LR
    subgraph VLAN[VLAN utilisateurs]
        H1[Hôte 1]
        H2[Hôte 2]
        H3[Hôte 3]
    end

    H1 --> VIP[10.1.2.254\nPasserelle virtuelle]
    H2 --> VIP
    H3 --> VIP

    VIP --> R1[R1\nActif]
    VIP -. secours .-> R2[R2\nStandby]
```

Les hôtes utilisent toujours la même passerelle virtuelle.
Le protocole choisit quel routeur la porte effectivement.

---

## 7. HSRP : définition

**HSRP** signifie **Hot Standby Router Protocol**.

C’est un protocole Cisco de redondance de premier saut.

Il met en œuvre :

- une **IP virtuelle** ;
- un **routeur actif** ;
- un **routeur standby**.

Dans une topologie simple :

- le routeur actif traite le trafic ;
- le standby surveille et prend le relais en cas de panne.

---

## 8. HSRP : logique visuelle

```{mermaid}
flowchart LR
    PC[Hôte] --> VIP[Passerelle virtuelle]
    VIP --> RA[Routeur actif]
    VIP -. secours .-> RS[Routeur standby]
    RA --> WAN[Autres réseaux]
```

**Point clé :**
les hôtes n’ont pas besoin de changer leur passerelle si le routeur actif tombe.

---

## 9. HSRP : éléments de configuration

Dans une configuration HSRP, on retrouve généralement :

- un **numéro de groupe** ;
- une **IP virtuelle** ;
- une **priorité** ;
- la **préemption**.

Exemple logique :

```text
interface g0/1.12
 ip address 10.1.2.252 255.255.255.0
 standby 12 ip 10.1.2.254
 standby 12 priority 110
 standby 12 preempt
```

---

## 10. HSRP : actif, standby, priorité

| Élément  | Rôle                                      |
| -------- | ----------------------------------------- |
| Active   | routeur qui traite le trafic              |
| Standby  | routeur de secours                        |
| Priority | niveau de préférence pour devenir actif   |
| Preempt  | autorise le retour du routeur prioritaire |

Le routeur avec la priorité la plus élevée devient généralement **actif**.

---

## 11. HSRP : bascule

```{mermaid}
sequenceDiagram
    participant H as Hôte
    participant R1 as Routeur actif
    participant R2 as Routeur standby

    H->>R1: trafic vers passerelle virtuelle
    R1-->>H: trafic normal
    Note over R1: panne
    R2->>R2: prise de rôle actif
    H->>R2: trafic vers la même passerelle virtuelle
```

La bascule n’impose pas de reconfigurer les hôtes.

---

## 12. HSRP et le TD

Dans une architecture de laboratoire avec redondance de passerelle, HSRP est souvent le choix le plus simple à introduire car :

- l’environnement est Cisco ;
- le modèle actif / standby est lisible ;
- la logique d’IP virtuelle est facile à tester ;
- la simulation de panne met immédiatement en évidence l’intérêt de la technologie.

---

## 13. VRRP : définition

**VRRP** signifie **Virtual Router Redundancy Protocol**.

Comme HSRP, il fournit :

- une passerelle virtuelle ;
- un routeur principal ;
- un routeur de secours.

La grande différence d’approche est que **VRRP est un standard**, alors que HSRP est historiquement associé à Cisco.

---

## 14. VRRP : logique générale

```{mermaid}
flowchart LR
    H[Hôtes VLAN] --> VIP[Passerelle virtuelle VRRP]
    VIP --> M[Routeur maître]
    VIP -. secours .-> B[Routeur backup]
```

La logique de fonctionnement est très proche de HSRP :

- un **maître** traite le trafic ;
- un **backup** prend le relais.

---

## 15. HSRP et VRRP : points communs

| Caractéristique      | HSRP                     | VRRP                     |
| -------------------- | ------------------------ | ------------------------ |
| Passerelle virtuelle | oui                      | oui                      |
| Routeur principal    | oui                      | oui                      |
| Routeur de secours   | oui                      | oui                      |
| Bascule automatique  | oui                      | oui                      |
| Objectif             | redondance de passerelle | redondance de passerelle |

---

## 16. HSRP et VRRP : différence principale

| Critère       | HSRP                | VRRP                              |
| ------------- | ------------------- | --------------------------------- |
| Nature        | protocole Cisco     | protocole standard                |
| Terminologie  | active / standby    | master / backup                   |
| Usage typique | environnement Cisco | environnement multi-constructeurs |

Dans une infrastructure homogène Cisco, HSRP est souvent choisi pour sa simplicité pédagogique.

---

## 17. GLBP : définition

**GLBP** signifie **Gateway Load Balancing Protocol**.

C’est un protocole Cisco qui ajoute une idée supplémentaire :

- la **redondance** ;
- **et** une forme de **répartition de charge** entre plusieurs routeurs.

Là où HSRP et VRRP désignent principalement un routeur actif et un routeur de secours, GLBP peut faire participer plusieurs routeurs au transfert effectif des flux.

---

## 18. GLBP : logique générale

```{mermaid}
flowchart LR
    H1[Hôte 1] --> VIP[Passerelle virtuelle GLBP]
    H2[Hôte 2] --> VIP
    H3[Hôte 3] --> VIP

    VIP --> R1[R1]
    VIP --> R2[R2]
    VIP --> R3[R3]
```

Dans GLBP :

- une même passerelle virtuelle est vue par les hôtes ;
- plusieurs routeurs peuvent participer à la charge.

---

## 19. Pourquoi GLBP est différent

HSRP et VRRP privilégient une logique :

- **un routeur traite** ;
- un autre attend en secours.

GLBP ajoute une logique :

- **plusieurs routeurs peuvent être utilisés** ;
- tout en gardant une passerelle virtuelle unique.

Cela le rend intéressant dans certaines architectures, mais plus complexe à introduire qu’HSRP.

---

## 20. Comparaison synthétique

| Protocole | Type     | Redondance | Répartition de charge | Standard |
| --------- | -------- | ---------- | --------------------- | -------- |
| HSRP      | Cisco    | oui        | non                   | non      |
| VRRP      | standard | oui        | non                   | oui      |
| GLBP      | Cisco    | oui        | oui                   | non      |

---

## 21. Quand choisir HSRP ?

HSRP est pertinent lorsque :

- l’infrastructure est majoritairement Cisco ;
- on veut une redondance lisible ;
- on cherche une mise en œuvre simple ;
- l’objectif principal est la continuité de service, pas la répartition de charge.

---

## 22. Quand choisir VRRP ?

VRRP est pertinent lorsque :

- l’environnement est multi-constructeurs ;
- on préfère un protocole standard ;
- on cherche la même logique de redondance de passerelle qu’avec HSRP.

---

## 23. Quand choisir GLBP ?

GLBP est pertinent lorsque :

- l’environnement est Cisco ;
- on veut à la fois une passerelle redondée et une répartition de charge ;
- la complexité supplémentaire est acceptable.

---

## 24. Ce que voient les hôtes

Du point de vue d’un poste client, le comportement est simple :

- il reçoit une adresse IP ;
- il reçoit ou configure une passerelle ;
- cette passerelle est une **IP virtuelle**.

```{mermaid}
flowchart LR
    PC[Poste client] --> GW[Passerelle virtuelle]
    GW --> R1[Routeur 1]
    GW --> R2[Routeur 2]
```

Les hôtes n’ont pas à connaître le routeur réellement actif.

---

## 25. Flux et bascule

### Situation nominale

```{mermaid}
flowchart LR
    PC[Hôte] --> VIP[Passerelle virtuelle]
    VIP --> R1[R1 actif]
    R1 --> NET[Autres réseaux]
```

### Situation dégradée

```{mermaid}
flowchart LR
    PC[Hôte] --> VIP[Passerelle virtuelle]
    VIP --> R2[R2 prend le relais]
    R2 --> NET[Autres réseaux]
```

La passerelle ne change pas côté client.
Seul le routeur réellement utilisé change.

---

## 26. Lien avec le routage interne

Les protocoles FHRP ne remplacent pas les protocoles de routage.

Ils travaillent à un autre niveau :

- **HSRP / VRRP / GLBP** gèrent le **premier saut** pour les hôtes ;
- **OSPF** ou d’autres protocoles gèrent le **routage entre routeurs**.

```{mermaid}
flowchart LR
    PC[Hôte] --> FHRP[HSRP / VRRP / GLBP]
    FHRP --> OSPF[OSPF / routage interne]
    OSPF --> WAN[WAN / autres réseaux]
```

---

## 27. FHRP et modèle OSI

Comme les protocoles de routage, les FHRP appartiennent au **plan de contrôle**.

Ils ne remplacent pas :

- Ethernet ;
- IP ;
- TCP ;
- la logique applicative.

Ils apportent une intelligence de continuité au niveau de la passerelle.

---

## 28. Limites des FHRP classiques

Même si HSRP, VRRP et GLBP sont très utiles, ils restent fondés sur une logique assez classique :

- redondance locale ;
- passerelle virtuelle ;
- réaction aux pannes ;
- parfois répartition simple.

Ils ne prennent pas en charge, à eux seuls :

- la mesure avancée de qualité de lien ;
- la sélection applicative du meilleur chemin WAN ;
- l’orchestration centralisée multi-sites ;
- l’automatisation globale des politiques réseau.

---

## 29. Ouverture : vers les approches modernes

Dans les architectures récentes, la résilience et le choix de chemin ne reposent plus uniquement sur des protocoles locaux de redondance de passerelle.

On rencontre aussi :

- le **SDN** ;
- le **SD-WAN** ;
- les politiques centralisées ;
- la sélection dynamique des liens selon la qualité observée.

---

## 30. SDN : idée générale

Le **SDN** (_Software Defined Networking_) repose sur une séparation :

- **plan de données** ;
- **plan de contrôle**.

```{mermaid}
flowchart LR
    CTRL[Contrôle centralisé] --> SW1[Équipement réseau 1]
    CTRL --> SW2[Équipement réseau 2]
    CTRL --> SW3[Équipement réseau 3]
```

L’objectif est de centraliser davantage les décisions et la programmation du réseau.

---

## 31. SD-WAN : idée générale

Le **SD-WAN** applique une logique plus moderne aux liaisons WAN.

Il permet typiquement :

- de piloter plusieurs liens WAN ;
- de mesurer latence, perte, gigue ;
- de sélectionner un chemin selon le type d’application ;
- de centraliser les politiques de transport.

```{mermaid}
flowchart LR
    APP[Applications / flux] --> CTRL[Politique SD-WAN]
    CTRL --> L1[Lien WAN 1]
    CTRL --> L2[Lien WAN 2]
    CTRL --> L3[Lien WAN 3]
```

---

## 32. Différence d’esprit entre FHRP et SD-WAN

| Aspect             | FHRP classiques             | SD-WAN                                  |
| ------------------ | --------------------------- | --------------------------------------- |
| Portée             | locale / premier saut       | multi-sites / WAN                       |
| Objectif principal | continuité de passerelle    | pilotage global des liens               |
| Décision           | distribuée localement       | souvent centralisée                     |
| Critères           | priorité, état des routeurs | qualité de lien, application, politique |

---

## 33. Pourquoi parler de SDN et SD-WAN ici ?

Même si le laboratoire ne met pas en œuvre ces technologies :

- elles prolongent logiquement la réflexion sur la résilience ;
- elles montrent que la redondance moderne peut dépasser la simple bascule actif / secours ;
- elles introduisent une logique de sélection plus fine et plus centralisée.

Autrement dit :

- HSRP, VRRP et GLBP répondent à un besoin local très concret ;
- SDN et SD-WAN ouvrent vers des architectures plus globales et plus dynamiques.

---

## 34. Synthèse comparative

| Technologie | Niveau principal  | But                                 |
| ----------- | ----------------- | ----------------------------------- |
| HSRP        | passerelle locale | redondance de premier saut          |
| VRRP        | passerelle locale | redondance standardisée             |
| GLBP        | passerelle locale | redondance + répartition            |
| OSPF        | routage interne   | échange de routes dans l’entreprise |
| BGP         | routage externe   | échange de routes entre AS          |
| SDN         | contrôle réseau   | centralisation du pilotage          |
| SD-WAN      | transport WAN     | sélection intelligente des liens    |

---

## 35. À retenir

- Une passerelle unique crée un **SPOF**.
- Les protocoles **FHRP** permettent d’introduire une **passerelle virtuelle**.
- **HSRP** et **VRRP** fournissent surtout une logique actif / secours.
- **GLBP** ajoute une dimension de répartition de charge.
- Ces mécanismes complètent le routage, mais ne le remplacent pas.
- Les approches modernes comme **SDN** et **SD-WAN** prolongent cette logique de résilience avec davantage de centralisation et de pilotage.

---

## 36. Questions de révision

1. Pourquoi une passerelle unique constitue-t-elle un SPOF ?
2. Qu’est-ce qu’une IP virtuelle de passerelle ?
3. Quel est le rôle d’un routeur actif dans HSRP ?
4. Quelle différence entre HSRP et VRRP ?
5. Quel apport spécifique propose GLBP ?
6. Pourquoi les hôtes ne doivent-ils pas utiliser directement l’IP physique du routeur principal ?
7. En quoi les FHRP complètent-ils OSPF ?
8. Pourquoi SD-WAN n’est-il pas une simple copie de HSRP à grande échelle ?

---

## 37. Synthèse finale

La redondance de passerelle est une brique essentielle de la disponibilité d’un réseau local.

Les protocoles **HSRP**, **VRRP** et **GLBP** permettent de supprimer le point de défaillance que représente une passerelle unique.

Dans une architecture classique :

- les hôtes utilisent une **passerelle virtuelle** ;
- un ou plusieurs routeurs assurent le service en arrière-plan ;
- la continuité est maintenue en cas de panne.

Ces technologies s’inscrivent dans une famille plus large de solutions de résilience, prolongées aujourd’hui par des approches comme le **SDN** et le **SD-WAN**, qui apportent une vision plus globale et plus centralisée du pilotage réseau.

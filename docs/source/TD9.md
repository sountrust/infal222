# TD9 — Redondance WAN et découverte de l’eBGP avec deux FAI simulés

## Pré-requis

Les éléments suivants doivent être opérationnels :

- les VLAN locaux fonctionnent ;
- le routage interne entre **R1**, **R2** et **R3** fonctionne avec **OSPF** ;
- l’architecture issue du TD8 est en place :
  - `g0/0.x` : trunk local et passerelles VLAN ;
  - `g0/2.x` : transit inter-routeurs et voisinages OSPF ;
  - `g0/1` : interface WAN disponible sur les routeurs de bordure.

## 1. Objectif

Dans le TD8, la sortie vers l’extérieur reposait sur un seul routeur.

Cette architecture fonctionne, mais elle présente un **point de défaillance unique**.

Dans ce TD, deux routeurs Cisco 2911 supplémentaires jouent le rôle de **FAI simulés** afin de :

- introduire **BGP** comme protocole de routage externe ;
- distinguer **OSPF** et **BGP** ;
- comprendre **eBGP**, **AS** et la logique de politique de routage ;
- mettre en place une **double sortie WAN** ;
- observer une première logique de **secours** et de **résilience**.

## 2. Notions de cours

### 2.1 BGP

**BGP** (_Border Gateway Protocol_) est un protocole de routage utilisé pour échanger des routes **entre systèmes autonomes**.

Contrairement à **OSPF**, qui est un protocole de routage **interne** à une organisation, BGP est utilisé **au bord du réseau**, entre réseaux distincts.

Exemples classiques :

- entreprise ↔ fournisseur d’accès ;
- fournisseur ↔ fournisseur ;
- organisation ↔ organisation.

BGP ne sert pas seulement à apprendre des routes. Il permet aussi d’appliquer une **politique de routage** :

- choix d’un chemin principal ;
- choix d’un chemin secondaire ;
- préférence d’un voisin ;
- gestion d’une logique de secours.

### 2.2 AS

Un **AS** (_Autonomous System_, système autonome) est un ensemble de routeurs :

- administrés par une même entité ;
- présentant une politique de routage cohérente ;
- identifiés par un **numéro d’AS**.

Dans ce TD :

- **AS 65000** : entreprise ;
- **AS 65100** : ISP1 ;
- **AS 65200** : ISP2.

Le numéro d’AS n’est ni une adresse IP, ni une adresse MAC.
C’est une information propre au protocole **BGP**, portée dans les **messages BGP**.

### 2.3 iBGP et eBGP

- **iBGP** : échange BGP entre routeurs d’un même AS ;
- **eBGP** : échange BGP entre routeurs d’AS différents.

Dans ce TD, on met en place de l’**eBGP** :

- **R1** parle avec **ISP1** ;
- **R2** parle avec **ISP2** ;
- les voisins appartiennent à des **AS différents**.

### 2.4 ISP

**ISP** signifie _Internet Service Provider_, c’est-à-dire **fournisseur d’accès à Internet**.

Dans ce TD, **ISP1** et **ISP2** sont des **FAI simulés**.
Ils représentent deux réseaux extérieurs distincts reliés à l’entreprise.

### 2.5 Où se situe l’échange BGP ?

L’échange BGP a lieu :

- entre **R1** et **ISP1** ;
- entre **R2** et **ISP2**.

Ces échanges se font sur les liaisons WAN :

- `R1 g0/1 ↔ ISP1 g0/0`
- `R2 g0/1 ↔ ISP2 g0/0`

BGP fonctionne au-dessus de **TCP**, sur le **port 179**.

Les informations d’AS sont donc transportées dans les **messages BGP**, eux-mêmes encapsulés dans TCP, puis IP, puis dans une trame Ethernet.

### 2.6 Pourquoi les numéros 64xxx / 65xxx ?

Dans les laboratoires, on utilise souvent des **AS privés** pour éviter toute confusion avec des numéros publics.

La plage privée classique sur 16 bits est **64512 à 65534**.

Les choix suivants sont donc cohérents et lisibles :

- **65000** pour l’entreprise ;
- **65100** pour ISP1 ;
- **65200** pour ISP2.

Ce choix est une **convention de maquette**, pas une obligation absolue.

L’important est de respecter la logique suivante :

- même AS pour les routeurs d’une même entité ;
- AS différents pour des réseaux différents.

### 2.7 Pourquoi conserver OSPF en interne ?

**OSPF** reste utilisé entre **R1**, **R2** et **R3** pour le routage interne de l’entreprise :

- transport des routes VLAN ;
- transport des routes de transit ;
- diffusion éventuelle d’une route par défaut.

BGP n’est pas utilisé partout : il est ajouté **au bord du réseau**, là où l’entreprise échange des routes avec les FAI.

## 3. Architecture retenue

### 3.1 Équipements

- **R1, R2, R3** : routeurs de l’entreprise ;
- **ISP1** : premier FAI simulé ;
- **ISP2** : second FAI simulé ;
- switches locaux pour les VLAN ;
- switch de transit pour OSPF.

### 3.2 Rôles

| Équipement | Rôle                  |
| ---------- | --------------------- |
| R1         | Edge principal        |
| R2         | Edge secondaire       |
| R3         | Routeur interne       |
| ISP1       | FAI simulé principal  |
| ISP2       | FAI simulé secondaire |

### 3.3 Liaisons WAN

| Liaison   | Réseau          |
| --------- | --------------- |
| R1 ↔ ISP1 | `172.16.1.0/30` |
| R2 ↔ ISP2 | `172.16.2.0/30` |

### 3.4 AS utilisés

| Entité     |    AS |
| ---------- | ----: |
| Entreprise | 65000 |
| ISP1       | 65100 |
| ISP2       | 65200 |

## 4. Vue d’ensemble de l’architecture

```{mermaid}
flowchart LR
    subgraph ENT[AS 65000 - Entreprise]
        R1[R1\nEdge principal]
        R2[R2\nEdge secondaire]
        R3[R3\nInterne]
        ST[Switch de transit]
        R1 <-->|OSPF| ST
        R2 <-->|OSPF| ST
        R3 <-->|OSPF| ST
    end

    ISP1[ISP1\nAS 65100]
    ISP2[ISP2\nAS 65200]
    NET1[203.0.113.0/24]
    NET2[198.51.100.0/24]

    R1 <-->|eBGP| ISP1 --> NET1
    R2 <-->|eBGP| ISP2 --> NET2
```

## 5. Plan d’adressage

### 5.1 Liens entreprise ↔ FAI

| Équipement | Interface | Adresse IP   | Masque |
| ---------- | --------- | ------------ | ------ |
| R1         | `g0/1`    | `172.16.1.1` | `/30`  |
| ISP1       | `g0/0`    | `172.16.1.2` | `/30`  |
| R2         | `g0/1`    | `172.16.2.1` | `/30`  |
| ISP2       | `g0/0`    | `172.16.2.2` | `/30`  |

### 5.2 Réseaux externes simulés

| Équipement | Interface | Réseau simulé     | Adresse        |
| ---------- | --------- | ----------------- | -------------- |
| ISP1       | `g0/1`    | `203.0.113.0/24`  | `203.0.113.1`  |
| ISP2       | `g0/1`    | `198.51.100.0/24` | `198.51.100.1` |

Ces deux préfixes représentent des réseaux extérieurs annoncés par BGP.

## 6. Câblage

### Entreprise

- `g0/0.x` : VLAN locaux ;
- `g0/2.x` : transit OSPF interne.

### WAN

- `R1 g0/1 ↔ ISP1 g0/0`
- `R2 g0/1 ↔ ISP2 g0/0`

### Réseaux externes simulés

- `ISP1 g0/1` vers le réseau `203.0.113.0/24` ;
- `ISP2 g0/1` vers le réseau `198.51.100.0/24`.

## 7. Configuration des interfaces WAN

### Routeurs de l’entreprise

#### R1

```text
conf t
interface g0/1
 description WAN_TO_ISP1
 ip address 172.16.1.1 255.255.255.252
 no shutdown
end
wr mem
```

#### R2

```text
conf t
interface g0/1
 description WAN_TO_ISP2
 ip address 172.16.2.1 255.255.255.252
 no shutdown
end
wr mem
```

### Routeurs FAI

#### ISP1

```text
conf t
interface g0/0
 description TO_R1
 ip address 172.16.1.2 255.255.255.252
 no shutdown
interface g0/1
 description EXT_NET_1
 ip address 203.0.113.1 255.255.255.0
 no shutdown
end
wr mem
```

#### ISP2

```text
conf t
interface g0/0
 description TO_R2
 ip address 172.16.2.2 255.255.255.252
 no shutdown
interface g0/1
 description EXT_NET_2
 ip address 198.51.100.1 255.255.255.0
 no shutdown
end
wr mem
```

### Vérifications

```text
show ip interface brief
```

Depuis **R1** :

```text
ping 172.16.1.2
```

Depuis **R2** :

```text
ping 172.16.2.2
```

## 8. Mise en place de l’eBGP

### 8.1 Principe

Deux sessions eBGP sont mises en place :

- **R1 (AS 65000) ↔ ISP1 (AS 65100)**
- **R2 (AS 65000) ↔ ISP2 (AS 65200)**

```{mermaid}
flowchart LR
    R1[R1\nAS 65000] <-->|eBGP| ISP1[ISP1\nAS 65100]
    R2[R2\nAS 65000] <-->|eBGP| ISP2[ISP2\nAS 65200]
```

### 8.2 Configuration BGP

#### R1

```text
conf t
router bgp 65000
 neighbor 172.16.1.2 remote-as 65100
 network 10.1.2.0 mask 255.255.255.0
 network 10.1.3.0 mask 255.255.255.0
 network 10.1.99.0 mask 255.255.255.0
end
wr mem
```

#### ISP1

```text
conf t
router bgp 65100
 neighbor 172.16.1.1 remote-as 65000
 network 203.0.113.0 mask 255.255.255.0
end
wr mem
```

#### R2

```text
conf t
router bgp 65000
 neighbor 172.16.2.2 remote-as 65200
 network 10.2.2.0 mask 255.255.255.0
 network 10.2.3.0 mask 255.255.255.0
 network 10.2.99.0 mask 255.255.255.0
end
wr mem
```

#### ISP2

```text
conf t
router bgp 65200
 neighbor 172.16.2.1 remote-as 65000
 network 198.51.100.0 mask 255.255.255.0
end
wr mem
```

## 9. Vérification des voisinages BGP

Sur **R1**, **R2**, **ISP1** et **ISP2** :

```text
show ip bgp summary
```

Le voisinage doit apparaître à l’état **Established**.

## 10. Observation des routes BGP

### Sur R1

```text
show ip bgp
show ip route bgp
```

### Sur R2

```text
show ip bgp
show ip route bgp
```

Constats attendus :

- **R1** apprend le préfixe `203.0.113.0/24` ;
- **R2** apprend le préfixe `198.51.100.0/24`.

## 11. Route par défaut et logique de secours

Les routeurs internes de l’entreprise ne parlent pas directement BGP avec les FAI.

On conserve donc une logique hybride :

- **BGP** pour les échanges externes ;
- **OSPF** pour la diffusion interne.

### 11.1 Sortie principale sur R1

Sur **R1** :

```text
conf t
ip route 0.0.0.0 0.0.0.0 172.16.1.2
router ospf 1
 default-information originate
end
wr mem
```

### 11.2 Sortie de secours sur R2

Sur **R2** :

```text
conf t
ip route 0.0.0.0 0.0.0.0 172.16.2.2 200
end
wr mem
```

Ici :

- **R1** reste la sortie principale ;
- **R2** dispose d’une route par défaut flottante, avec une distance administrative plus élevée.

## 12. Logique globale de routage

```{mermaid}
flowchart LR
    PC[Poste interne] --> RI[Routeur interne]
    RI -->|OSPF + route par défaut| R1[R1 sortie principale]
    R1 -->|eBGP| ISP1

    RI -. secours .-> R2[R2 sortie secondaire]
    R2 -->|eBGP| ISP2
```

## 13. Vérifications côté entreprise

### Sur R1

```text
show ip bgp summary
show ip bgp
show ip route
show ip route bgp
show ip route | include 0.0.0.0
```

### Sur R2

```text
show ip bgp summary
show ip bgp
show ip route
show ip route bgp
show ip route | include 0.0.0.0
```

### Sur R3

```text
show ip route | include 0.0.0.0
show ip ospf neighbor
```

## 14. Tests de connectivité

Depuis un poste interne :

- test vers une passerelle distante interne ;
- test vers les réseaux externes simulés :
  - `203.0.113.1`
  - `198.51.100.1`

Depuis **R1** :

```text
ping 203.0.113.1
```

Depuis **R2** :

```text
ping 198.51.100.1
```

## 15. Test de résilience

### 15.1 Panne simulée du lien principal

Sur **R1** :

```text
conf t
interface g0/1
 shutdown
end
```

### 15.2 Vérifications

Sur **R1** :

```text
show ip bgp summary
show ip route | include 0.0.0.0
```

Sur **R2** :

```text
show ip bgp summary
show ip route | include 0.0.0.0
```

Sur **R3** :

```text
show ip route | include 0.0.0.0
```

### 15.3 Analyse

Observer :

- la perte du voisinage eBGP entre **R1** et **ISP1** ;
- le maintien d’une seconde sortie WAN ;
- la différence entre une architecture à sortie unique et une architecture redondée.

### 15.4 Remise en service

Sur **R1** :

```text
conf t
interface g0/1
 no shutdown
end
```

## 16. Synthèse

Dans ce TD :

- l’entreprise conserve **OSPF** pour son routage interne ;
- deux routeurs 2911 supplémentaires jouent le rôle de **FAI simulés** ;
- **R1** et **R2** établissent des sessions **eBGP** avec ces FAI ;
- les notions de **BGP**, **eBGP**, **AS** et de **politique de routage** sont introduites ;
- l’architecture évolue vers une logique de **double sortie WAN** ;
- la notion de **résilience** apparaît concrètement.

Ce TD constitue une première mise en œuvre de **BGP au bord du réseau**, en complément d’**OSPF** utilisé à l’intérieur de l’entreprise.

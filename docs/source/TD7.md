# TD7 — Phase C/D : Interconnexion des 3 infrastructures, OSPF et ECMP

## Pré-requis

Chaque groupe a terminé la Phase B avec un plan d’adressage unique :

- VLAN 2 : `10.g.2.0/24` — passerelle `10.g.2.254`
- VLAN 3 : `10.g.3.0/24` — passerelle `10.g.3.254`
- VLAN 99 : `10.g.99.0/24` — passerelle `10.g.99.254`

Les routeurs sont des **Cisco 2911** et les switches des **2960 L2**.

Les trois routeurs seront interconnectés en **liaisons Ethernet directes**.

Convention utilisée dans le TD :

- **R1** pour le groupe 1
- **R2** pour le groupe 2
- **R3** pour le groupe 3

## Objectifs

Cette phase a deux objectifs principaux :

- interconnecter les trois infrastructures pour permettre l’échange automatique des routes ;
- mettre en évidence la logique **ECMP** lorsqu’il existe plusieurs chemins de coût égal.

À l’issue du TD, les trois groupes doivent former une infrastructure interconnectée dans laquelle :

- **OSPF** diffuse les réseaux VLAN de chaque groupe ;
- les postes peuvent joindre les réseaux distants ;
- certains réseaux sont atteignables par **deux next-hops OSPF** ;
- la coupure d’un lien inter-routeur n’interrompt pas durablement la connectivité.

## 1. Topologie et plan d’adressage inter-routeurs

### 1.1 Topologie retenue

Les trois routeurs sont interconnectés en triangle :

- lien **R1 ↔ R2**
- lien **R2 ↔ R3**
- lien **R1 ↔ R3**

```{mermaid}
flowchart LR
    R1[R1\nGroupe 1] --- R2[R2\nGroupe 2]
    R2 --- R3[R3\nGroupe 3]
    R1 --- R3
```

Cette topologie permet :

- la redondance de chemin ;
- la formation de deux voisinages par routeur ;
- l’introduction d’**ECMP** lorsque les coûts OSPF sont ajustés.

### 1.2 Adressage des liens point à point

Les liens inter-routeurs utilisent des réseaux `/30`.

| Lien  | Réseau           | IP côté 1          | IP côté 2          |
| ----- | ---------------- | ------------------ | ------------------ |
| R1–R2 | `10.255.12.0/30` | R1 = `10.255.12.1` | R2 = `10.255.12.2` |
| R1–R3 | `10.255.13.0/30` | R1 = `10.255.13.1` | R3 = `10.255.13.2` |
| R2–R3 | `10.255.23.0/30` | R2 = `10.255.23.1` | R3 = `10.255.23.2` |

### 1.3 Loopbacks pour le router-id OSPF

| Routeur | Loopback0       |
| ------- | --------------- |
| R1      | `10.255.0.1/32` |
| R2      | `10.255.0.2/32` |
| R3      | `10.255.0.3/32` |

La loopback sert d’identifiant logique stable pour OSPF.

## 2. Vue d’ensemble de l’architecture

Chaque routeur conserve son rôle local de passerelle VLAN pour son groupe, tout en échangeant ses routes avec les deux autres via OSPF.

```{mermaid}
flowchart LR
    subgraph G1[Groupe 1]
        SW1[Switch G1]
        LAN1[VLAN 2 / VLAN 3 / VLAN 99]
        SW1 --- LAN1
        R1[R1]
        SW1 <-->|Trunk| R1
    end

    subgraph G2[Groupe 2]
        SW2[Switch G2]
        LAN2[VLAN 2 / VLAN 3 / VLAN 99]
        SW2 --- LAN2
        R2[R2]
        SW2 <-->|Trunk| R2
    end

    subgraph G3[Groupe 3]
        SW3[Switch G3]
        LAN3[VLAN 2 / VLAN 3 / VLAN 99]
        SW3 --- LAN3
        R3[R3]
        SW3 <-->|Trunk| R3
    end

    R1 ---|10.255.12.0/30| R2
    R1 ---|10.255.13.0/30| R3
    R2 ---|10.255.23.0/30| R3
```

## 3. Câblage et configuration IP des liens inter-routeurs

### 3.1 Câblage

Relier les interfaces inter-routeurs selon les ports disponibles sur les 2911.

Chaque lien doit être un **lien Ethernet direct entre deux routeurs**.

Avant toute configuration, identifier les interfaces disponibles :

```text
show ip interface brief
```

### 3.2 Configuration des interfaces inter-routeurs

Les exemples suivants utilisent `g0/1` et `g0/2`. Adapter les noms si le câblage réel est différent.

#### R1

```text
conf t
interface g0/1
 description LINK_TO_R2
 ip address 10.255.12.1 255.255.255.252
 no shutdown
!
interface g0/2
 description LINK_TO_R3
 ip address 10.255.13.1 255.255.255.252
 no shutdown
end
wr mem
```

#### R2

```text
conf t
interface g0/1
 description LINK_TO_R1
 ip address 10.255.12.2 255.255.255.252
 no shutdown
!
interface g0/2
 description LINK_TO_R3
 ip address 10.255.23.1 255.255.255.252
 no shutdown
end
wr mem
```

#### R3

```text
conf t
interface g0/1
 description LINK_TO_R1
 ip address 10.255.13.2 255.255.255.252
 no shutdown
!
interface g0/2
 description LINK_TO_R2
 ip address 10.255.23.2 255.255.255.252
 no shutdown
end
wr mem
```

### 3.3 Vérification avant OSPF

Avant d’activer le routage dynamique, vérifier que les liens IP fonctionnent.

Depuis **R1** :

```text
ping 10.255.12.2
ping 10.255.13.2
```

Depuis **R2** :

```text
ping 10.255.12.1
ping 10.255.23.2
```

Depuis **R3** :

```text
ping 10.255.13.1
ping 10.255.23.1
```

## 4. Configuration des loopbacks

### R1

```text
conf t
interface loopback0
 ip address 10.255.0.1 255.255.255.255
end
wr mem
```

### R2

```text
conf t
interface loopback0
 ip address 10.255.0.2 255.255.255.255
end
wr mem
```

### R3

```text
conf t
interface loopback0
 ip address 10.255.0.3 255.255.255.255
end
wr mem
```

### Vérification

```text
show ip interface brief | include Loopback0
```

## 5. OSPF : échange de routes entre les 3 groupes

### 5.1 Objectif

OSPF doit permettre de :

- former les voisinages sur les liens inter-routeurs ;
- annoncer les réseaux VLAN de chaque groupe ;
- éviter tout voisinage OSPF côté LAN utilisateur.

### 5.2 Bonnes pratiques appliquées

Sur les trois routeurs :

- router-id fixé sur **Loopback0** ;
- `passive-interface default` ;
- `no passive-interface` uniquement sur les liens inter-routeurs.

### 5.3 Logique de diffusion OSPF

```{mermaid}
flowchart LR
    subgraph R1A[R1]
        N1[VLAN 10.1.2.0/24]
        N2[VLAN 10.1.3.0/24]
        N3[VLAN 10.1.99.0/24]
    end

    subgraph R2A[R2]
        N4[VLAN 10.2.2.0/24]
        N5[VLAN 10.2.3.0/24]
        N6[VLAN 10.2.99.0/24]
    end

    subgraph R3A[R3]
        N7[VLAN 10.3.2.0/24]
        N8[VLAN 10.3.3.0/24]
        N9[VLAN 10.3.99.0/24]
    end

    R1A <-->|OSPF| R2A
    R2A <-->|OSPF| R3A
    R1A <-->|OSPF| R3A
```

Chaque routeur annonce ses réseaux locaux, puis apprend ceux des deux autres.

### 5.4 Configuration OSPF

#### R1

```text
conf t
router ospf 1
 router-id 10.255.0.1
 passive-interface default
 no passive-interface g0/1
 no passive-interface g0/2
!
 network 10.255.0.1 0.0.0.0 area 0
 network 10.255.12.0 0.0.0.3 area 0
 network 10.255.13.0 0.0.0.3 area 0
 network 10.1.2.0 0.0.0.255 area 0
 network 10.1.3.0 0.0.0.255 area 0
 network 10.1.99.0 0.0.0.255 area 0
end
wr mem
```

#### R2

```text
conf t
router ospf 1
 router-id 10.255.0.2
 passive-interface default
 no passive-interface g0/1
 no passive-interface g0/2
!
 network 10.255.0.2 0.0.0.0 area 0
 network 10.255.12.0 0.0.0.3 area 0
 network 10.255.23.0 0.0.0.3 area 0
 network 10.2.2.0 0.0.0.255 area 0
 network 10.2.3.0 0.0.0.255 area 0
 network 10.2.99.0 0.0.0.255 area 0
end
wr mem
```

#### R3

```text
conf t
router ospf 1
 router-id 10.255.0.3
 passive-interface default
 no passive-interface g0/1
 no passive-interface g0/2
!
 network 10.255.0.3 0.0.0.0 area 0
 network 10.255.13.0 0.0.0.3 area 0
 network 10.255.23.0 0.0.0.3 area 0
 network 10.3.2.0 0.0.0.255 area 0
 network 10.3.3.0 0.0.0.255 area 0
 network 10.3.99.0 0.0.0.255 area 0
end
wr mem
```

## 6. Vérifications OSPF

Sur chaque routeur :

```text
show ip ospf neighbor
show ip route ospf
show ip ospf interface brief
```

### Résultats attendus

- chaque routeur voit **2 voisins OSPF** ;
- les routes OSPF vers les réseaux des deux autres groupes sont installées ;
- seules les interfaces inter-routeurs forment des voisinages.

### Lecture du voisinage

```{mermaid}
flowchart TD
    A[show ip ospf neighbor] --> B[2 voisins visibles]
    B --> C[Adjacence FULL]
    C --> D[Topologie cohérente]
```

## 7. Tests de bout en bout

Depuis un poste du **groupe 1 VLAN 2** :

- ping vers une machine du **groupe 2 VLAN 2** ;
- ping vers une machine du **groupe 3 VLAN 3** ;
- ping vers les passerelles distantes si autorisé :
  - `10.2.2.254`
  - `10.3.3.254`

Ces tests valident le fait que le routage inter-groupes fonctionne bien au niveau IP.

## 8. ECMP avec OSPF

### 8.1 Objectif

Créer, pour un routeur donné, deux chemins de **coût égal** vers un même réseau distant.

Dans la topologie triangle, on peut forcer cette situation en ajustant les coûts OSPF sur les liens inter-routeurs.

Exemple visé depuis **R1** vers les réseaux du groupe 2 :

- chemin direct : `R1 → R2`
- chemin indirect : `R1 → R3 → R2`
- coût total identique

### 8.2 Principe ECMP

```{mermaid}
flowchart LR
    R1[R1] -- coût 20 --> R2[R2]
    R1 -- coût 10 --> R3[R3]
    R3 -- coût 10 --> R2
```

Dans cet exemple :

- chemin direct `R1 → R2` : coût 20 ;
- chemin indirect `R1 → R3 → R2` : coût 10 + 10 = 20.

Les deux chemins sont donc équivalents.

OSPF peut installer les deux routes : c’est le principe de **l’ECMP**.

## 9. Réglage des coûts OSPF

### Plan commun de coûts

| Lien  | Coût à appliquer |
| ----- | ---------------: |
| R1–R2 |               20 |
| R1–R3 |               10 |
| R2–R3 |               10 |

### Configuration des coûts

#### R1

```text
conf t
interface g0/1
 ip ospf cost 20
!
interface g0/2
 ip ospf cost 10
end
wr mem
```

#### R2

```text
conf t
interface g0/1
 ip ospf cost 20
!
interface g0/2
 ip ospf cost 10
end
wr mem
```

#### R3

```text
conf t
interface g0/1
 ip ospf cost 10
!
interface g0/2
 ip ospf cost 10
end
wr mem
```

## 10. Vérification de l’ECMP

Sur **R1**, vérifier une route vers un réseau du groupe 2, par exemple :

```text
show ip route 10.2.2.0
```

Résultat attendu :

- deux **next-hops OSPF** ;
- deux chemins installés vers le même réseau.

Faire le même type de contrôle sur les autres routeurs :

```text
show ip route 10.1.2.0
show ip route 10.3.2.0
```

Si disponible sur l’IOS :

```text
show ip cef 10.2.2.0
```

Cette commande permet d’observer la logique de répartition CEF sur plusieurs next-hops.

## 11. Visualisation logique de l’ECMP

```{mermaid}
flowchart LR
    SRC[R1] -->|Chemin 1| NH1[R2]
    SRC -->|Chemin 2| NH2[R3]
    NH1 --> DST[10.2.2.0/24]
    NH2 --> DST
```

Le réseau distant est atteignable par deux chemins de coût égal.

## 12. Démonstration de résilience

### 12.1 Objectif

Montrer que :

- l’ECMP améliore l’utilisation des chemins disponibles ;
- OSPF maintient la connectivité après la perte d’un lien ;
- le routage converge vers le chemin restant.

### 12.2 Procédure

1. lancer un ping continu depuis **R1** vers une IP du groupe 2 :

```text
ping 10.2.2.254 repeat 1000
```

2. couper le lien direct **R1 → R2** :

```text
conf t
interface g0/1
 shutdown
end
```

3. observer :

- le trafic continue après convergence ;
- le chemin indirect via **R3** reste disponible ;
- la route ECMP devient une route à chemin unique.

4. vérifier :

```text
show ip ospf neighbor
show ip route 10.2.2.0
```

5. remettre le lien :

```text
conf t
interface g0/1
 no shutdown
end
```

6. vérifier le retour du multipath :

```text
show ip route 10.2.2.0
```

## 13. Schéma logique de résilience

```{mermaid}
flowchart LR
    R1[R1] -. lien coupé .-x R2[R2]
    R1 --> R3[R3]
    R3 --> R2
    R2 --> NET[Réseau du groupe 2]
```

Après coupure du lien direct, le trafic peut continuer par le chemin restant.

## 14. Recette finale de validation

Chaque routeur doit pouvoir valider les éléments suivants.

### 14.1 Voisins OSPF

```text
show ip ospf neighbor
```

Résultat attendu : **2 voisins visibles**.

### 14.2 Routes OSPF vers les autres groupes

```text
show ip route ospf
```

Résultat attendu : routes apprises vers les réseaux des deux autres groupes.

### 14.3 ECMP actif sur au moins un réseau

```text
show ip route <reseau_distant>
```

Résultat attendu : au moins un réseau distant possède **2 next-hops**.

### 14.4 Continuité de service après coupure

Après coupure d’un lien inter-routeur :

- le trafic reste possible après convergence ;
- la route se rabat sur le chemin restant ;
- le voisinage et la table de routage reflètent la nouvelle topologie.

## 15. Synthèse

Dans cette phase :

- les trois groupes sont interconnectés en triangle ;
- OSPF diffuse automatiquement les réseaux VLAN de chaque groupe ;
- les postes peuvent joindre des réseaux extérieurs à leur groupe ;
- l’ECMP apparaît lorsque deux chemins ont le même coût ;
- la coupure d’un lien inter-routeur n’interrompt pas durablement la connectivité.

Cette architecture constitue une base solide pour introduire ensuite des évolutions plus avancées :

- trunk de transit ;
- sortie WAN ;
- NAT centralisé ;
- routage externe.

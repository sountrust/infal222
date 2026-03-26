# TD6 — Phase B : Préparation d’une infrastructure cohérente (3 groupes, sans overlap)

## Version « best practice » avec VLAN natif dédié

## Contexte

Trois groupes ont réalisé la même architecture de base lors du TD précédent :

- mêmes VLAN ;
- mêmes logiques de configuration ;
- mêmes principes de routage inter-VLAN.

Avant d’interconnecter les infrastructures pour mettre en place **OSPF** et **ECMP**, il faut rendre l’adressage **unique par groupe** et appliquer une méthode de travail commune.

L’objectif est de conserver une architecture homogène, lisible et prête à être reliée aux autres groupes.

## Objectifs

- éviter tout **overlap d’adresses IP** entre les 3 groupes ;
- conserver une logique VLAN identique pour tous ;
- introduire une bonne pratique de sécurité : **VLAN natif non utilisé** ;
- produire 3 infrastructures prêtes à être interconnectées.

## Vue d’ensemble de l’architecture

```{mermaid}
flowchart LR
    PC2[Poste VLAN 2] --> SW[Switch 2960]
    PC3[Poste VLAN 3] --> SW
    ADM[Management VLAN 99] --> SW
    SW <-->|Trunk 802.1Q\nVLAN 2,3,99,999\nNatif = 999| R[Routeur 2911]
    R --> V2[Passerelle VLAN 2\n10.g.2.254]
    R --> V3[Passerelle VLAN 3\n10.g.3.254]
    R --> V99[Passerelle VLAN 99\n10.g.99.254]
```

L’interface routeur ↔ switch fonctionne en **router-on-a-stick** :

- une interface physique côté routeur ;
- plusieurs sous-interfaces 802.1Q ;
- un trunk côté switch.

Le **VLAN 999** est utilisé comme **VLAN natif de sécurité**. Il ne transporte aucun trafic utilisateur ni management.

## 1. Attribution des groupes et conventions communes

### 1.1 Affectation

Chaque binôme choisit ou reçoit un identifiant de groupe :

- **Groupe 1**
- **Groupe 2**
- **Groupe 3**

Dans la suite du TD, on notera cet identifiant **g**.

### 1.2 Conventions communes

Ces conventions sont identiques pour tous les groupes.

| Élément                    | Convention retenue                    |
| -------------------------- | ------------------------------------- |
| VLAN utilisateurs          | 2 et 3                                |
| VLAN management            | 99                                    |
| VLAN natif trunk           | 999                                   |
| Rôle du VLAN 999           | VLAN natif non utilisé, « blackhole » |
| Réseau privé global        | 10.0.0.0/8                            |
| Passerelle des VLAN        | `.254` sur le routeur                 |
| IP de management du switch | VLAN 99                               |
| Lien switch ↔ routeur      | trunk 802.1Q                          |
| Routage inter-VLAN         | router-on-a-stick                     |

## 2. Plan d’adressage sans overlap

Pour le **groupe g** avec `g = 1`, `2` ou `3` :

| VLAN | Usage      | Réseau         | Passerelle routeur |
| ---: | ---------- | -------------- | ------------------ |
|    2 | LAN 1      | `10.g.2.0/24`  | `10.g.2.254`       |
|    3 | LAN 2      | `10.g.3.0/24`  | `10.g.3.254`       |
|   99 | Management | `10.g.99.0/24` | `10.g.99.254`      |

### IP de management du switch

| Équipement         | Adresse recommandée | Passerelle    |
| ------------------ | ------------------- | ------------- |
| Switch du groupe g | `10.g.99.2/24`      | `10.g.99.254` |

## 3. Principe de non-chevauchement

Le groupe est distingué par l’octet **g**.

Exemple :

| Groupe | VLAN 2        | VLAN 3        | VLAN 99        |
| -----: | ------------- | ------------- | -------------- |
|      1 | `10.1.2.0/24` | `10.1.3.0/24` | `10.1.99.0/24` |
|      2 | `10.2.2.0/24` | `10.2.3.0/24` | `10.2.99.0/24` |
|      3 | `10.3.2.0/24` | `10.3.3.0/24` | `10.3.99.0/24` |

Ainsi, chaque groupe garde la même logique de configuration tout en évitant tout conflit d’adressage lors de l’interconnexion future.

## 4. Schéma logique de préparation multi-groupes

```{mermaid}
flowchart LR
    subgraph G1[Infrastructure groupe 1]
        SW1[Switch G1]
        R1[Routeur G1]
        SW1 <-->|Trunk| R1
    end

    subgraph G2[Infrastructure groupe 2]
        SW2[Switch G2]
        R2[Routeur G2]
        SW2 <-->|Trunk| R2
    end

    subgraph G3[Infrastructure groupe 3]
        SW3[Switch G3]
        R3[Routeur G3]
        SW3 <-->|Trunk| R3
    end

    G1 -. futur OSPF / ECMP .- G2
    G2 -. futur OSPF / ECMP .- G3
    G1 -. futur OSPF / ECMP .- G3
```

À ce stade, les trois infrastructures restent **séparées**.
Le TD prépare l’architecture pour une interconnexion future.

## 5. Sauvegarde et état initial

Avant toute modification, relever l’état initial des équipements.

### 5.1 Routeur 2911

Exécuter et conserver les sorties suivantes :

```text
show running-config
show ip interface brief
show ip dhcp binding
show ip dhcp pool
show ip route
```

### 5.2 Switch 2960

Exécuter et conserver les sorties suivantes :

```text
show running-config
show vlan brief
show interfaces trunk
show ip interface brief
```

## 6. Migration par groupe

Chaque groupe adapte sa propre infrastructure en appliquant la même méthode.

## 6.1 Routeur 2911 — Routage inter-VLAN (router-on-a-stick)

Sur l’interface trunk vers le switch, adapter le numéro d’interface si nécessaire.

Exemple avec `g0/0` :

```text
conf t
!
interface g0/0
 no shutdown
!
interface g0/0.2
 encapsulation dot1Q 2
 ip address 10.g.2.254 255.255.255.0
!
interface g0/0.3
 encapsulation dot1Q 3
 ip address 10.g.3.254 255.255.255.0
!
interface g0/0.99
 encapsulation dot1Q 99
 ip address 10.g.99.254 255.255.255.0
!
interface g0/0.999
 encapsulation dot1Q 999 native
 ! VLAN natif “blackhole” : pas d’adresse IP
end
wr mem
```

### Vérification

```text
show ip interface brief
```

## 6.2 Routeur 2911 — DHCP (un pool par VLAN)

Supprimer les anciens pools si nécessaire, puis créer les nouveaux.

```text
conf t
!
ip dhcp excluded-address 10.g.2.1 10.g.2.50
ip dhcp excluded-address 10.g.3.1 10.g.3.50
!
no ip dhcp pool VLAN2
ip dhcp pool VLAN2
 network 10.g.2.0 255.255.255.0
 default-router 10.g.2.254
!
no ip dhcp pool VLAN3
ip dhcp pool VLAN3
 network 10.g.3.0 255.255.255.0
 default-router 10.g.3.254
end
wr mem
```

### Vérification

```text
show ip dhcp pool
show ip dhcp binding
```

## 6.3 Switch 2960 — Création des VLAN

Créer les VLAN nécessaires si ce n’est pas déjà fait.

```text
conf t
vlan 2
 name VLAN2
vlan 3
 name VLAN3
vlan 99
 name MGMT
vlan 999
 name NATIVE_BLACKHOLE
end
wr mem
```

### Vérification

```text
show vlan brief
```

## 6.4 Switch 2960 — Trunk vers le routeur

Adapter le port trunk selon votre câblage. Exemple avec `f0/24`.

```text
conf t
interface f0/24
 switchport mode trunk
 switchport trunk allowed vlan 2,3,99,999
 switchport trunk native vlan 999
 no shutdown
end
wr mem
```

### Vérification

```text
show interfaces trunk
```

## 6.5 Switch 2960 — IP de management (SVI VLAN 99)

```text
conf t
interface vlan 99
 ip address 10.g.99.2 255.255.255.0
 no shutdown
exit
ip default-gateway 10.g.99.254
end
wr mem
```

### Vérification

```text
show ip interface brief
ping 10.g.99.254
```

## 7. Rôle du VLAN natif 999

Le VLAN natif du trunk est fixé à **999**.

Il ne doit transporter :

- ni trafic utilisateur ;
- ni trafic management ;
- ni service applicatif.

Son rôle est de servir de **VLAN de sécurité** ou **VLAN blackhole**.

```{mermaid}
flowchart LR
    SW[Switch] <-->|Trunk 802.1Q| R[Routeur]
    SW --> V2[VLAN 2 : utilisateurs]
    SW --> V3[VLAN 3 : utilisateurs]
    SW --> V99[VLAN 99 : management]
    SW --> V999[VLAN 999 : natif, non utilisé]
```

Cette pratique améliore la lisibilité et limite les mauvaises affectations du VLAN natif.

## 8. Renouvellement DHCP côté postes

Sur chaque poste :

- renouveler l’adresse IP ;
- vérifier que l’adresse reçue correspond au **bon VLAN** et au **bon groupe**.

Exemples attendus :

- poste du VLAN 2 → adresse en `10.g.2.0/24` ;
- poste du VLAN 3 → adresse en `10.g.3.0/24`.

## 9. Recette de validation

### 9.1 Tests DHCP

Vérifier que :

- un poste du **VLAN 2** reçoit une adresse en `10.g.2.0/24` avec passerelle `10.g.2.254` ;
- un poste du **VLAN 3** reçoit une adresse en `10.g.3.0/24` avec passerelle `10.g.3.254`.

### 9.2 Tests de connectivité

Depuis un poste du VLAN 2 :

- ping `10.g.2.254` ;
- ping un poste du VLAN 3 si le scénario du TD l’autorise.

Depuis un poste du VLAN 3 :

- ping `10.g.3.254`.

Depuis le switch :

- ping `10.g.99.254`.

### 9.3 Contrôle côté routeur

```text
show ip interface brief
show ip dhcp binding
show ip route
```

## 10. Schéma de validation fonctionnelle

```{mermaid}
flowchart LR
    H2[Poste VLAN 2\nDHCP 10.g.2.x] --> SW[Switch]
    H3[Poste VLAN 3\nDHCP 10.g.3.x] --> SW
    SW <-->|Trunk VLAN 2,3,99,999| R[Routeur]
    SW --> M[SVI VLAN 99\n10.g.99.2]
    R --> GW2[10.g.2.254]
    R --> GW3[10.g.3.254]
    R --> GW99[10.g.99.254]
```

## 11. État « prêt pour interconnexion OSPF / ECMP »

L’infrastructure du groupe est considérée prête si :

- les **VLAN 2, 3 et 99** fonctionnent ;
- le **DHCP** distribue correctement sur les VLAN 2 et 3 ;
- le switch est joignable sur `10.g.99.2` ;
- aucune adresse du groupe ne chevauche celles des autres groupes ;
- le trunk utilise le **VLAN natif 999** non utilisé.

## 12. Synthèse

À la fin de cette phase, chaque groupe dispose :

- d’une architecture VLAN cohérente ;
- d’un adressage unique ;
- d’un management fonctionnel ;
- d’un trunk configuré selon une bonne pratique de sécurité ;
- d’une base prête à être interconnectée aux deux autres groupes.

Le TD prépare ainsi la transition vers une architecture plus riche, dans laquelle plusieurs routeurs échangeront dynamiquement leurs routes.

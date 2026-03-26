# TD8 — Phase E : WAN simulé, sortie centralisée, NAT et route par défaut via OSPF

## Pré-requis

Les phases précédentes sont terminées :

- VLAN et adressage par groupe fonctionnels ;
- OSPF opérationnel entre **R1**, **R2** et **R3** via le switch de transit ;
- architecture de transit par sous-interfaces en place ;
- connectivité inter-groupes validée.

Le réseau « Internet » est simulé en circuit fermé avec un PC.

Convention retenue :

- **R1 = edge**
- **R2 et R3 = routeurs internes**

## Objectif

Cette phase introduit une sortie WAN centralisée.

L’idée est la suivante :

- un seul routeur assure la sortie vers l’extérieur ;
- les autres routeurs n’ont plus de route par défaut propre ;
- le **NAT** est centralisé sur le routeur de bordure ;
- la route par défaut est diffusée aux autres routeurs via **OSPF**.

## 1. Vue d’ensemble de l’architecture

```{mermaid}
flowchart LR
    subgraph ENT[Infrastructure interne]
        R1[R1\nRouteur edge]
        R2[R2\nRouteur interne]
        R3[R3\nRouteur interne]
        ST[Switch de transit]
        R1 <-->|OSPF| ST
        R2 <-->|OSPF| ST
        R3 <-->|OSPF| ST
    end

    PC[PC Internet simulé\n223.0.0.2] <-->|WAN simulé| R1
```

Le trafic interne doit sortir par **R1**, qui devient le point unique d’accès au WAN simulé.

## 2. Choix de l’edge et du PC « Internet »

### 2.1 Edge

Le routeur **R1** devient le routeur edge.

Il assure :

- la sortie unique vers le WAN simulé ;
- le NAT centralisé ;
- l’annonce de la route par défaut à l’ensemble du réseau interne.

### 2.2 PC « Utilisateur Internet »

Le PC « Internet » est connecté à l’interface WAN de **R1**.

Il ne représente pas Internet complet, mais un **réseau externe simulé**.

## 3. Logique de fonctionnement

```{mermaid}
flowchart LR
    LAN[Poste interne] --> RINT[Routeur interne]
    RINT -->|OSPF + default route| R1[R1 edge]
    R1 -->|NAT + sortie WAN| PC[PC Internet simulé]
```

Chemin logique du trafic :

1. le poste envoie vers sa passerelle locale ;
2. le routeur interne utilise la route par défaut apprise via OSPF ;
3. le trafic atteint **R1** ;
4. **R1** traduit l’adresse privée via NAT ;
5. le paquet sort vers le réseau externe simulé.

## 4. Nettoyage sur R2 et R3

### Objectif

R2 et R3 ne doivent plus avoir :

- de route par défaut propre ;
- de NAT local ;
- d’ancienne interface WAN active.

Ils redeviennent des routeurs internes dépendant de **R1** pour la sortie WAN.

### 4.1 Suppression de la route par défaut

#### Sur R2

```text
show ip route | include 0.0.0.0
conf t
no ip route 0.0.0.0 0.0.0.0 223.0.0.2
end
wr mem
```

#### Sur R3

```text
show ip route | include 0.0.0.0
conf t
no ip route 0.0.0.0 0.0.0.0 223.0.0.2
end
wr mem
```

### 4.2 Suppression du NAT local

#### Sur R2

```text
show run | include ip nat
conf t
no ip nat inside source list NAT_INTERNET_VLAN2 interface g0/1 overload
no ip nat inside source list NAT_INTERNET_VLAN3 interface g0/1 overload
no ip access-list standard NAT_INTERNET_VLAN2
no ip access-list standard NAT_INTERNET_VLAN3
end
wr mem
```

#### Sur R3

```text
show run | include ip nat
conf t
no ip nat inside source list NAT_INTERNET_VLAN2 interface g0/1 overload
no ip nat inside source list NAT_INTERNET_VLAN3 interface g0/1 overload
no ip access-list standard NAT_INTERNET_VLAN2
no ip access-list standard NAT_INTERNET_VLAN3
end
wr mem
```

### 4.3 Mise hors service de l’ancienne interface WAN

#### Sur R2

```text
conf t
interface g0/1
 shutdown
end
wr mem
```

#### Sur R3

```text
conf t
interface g0/1
 shutdown
end
wr mem
```

### 4.4 Vérification sur R2 et R3

```text
show ip route | include 0.0.0.0
show run | include ip nat
```

## 5. Mise en place du WAN simulé sur R1

### 5.1 Configuration du PC « Internet »

Configurer le PC comme suit :

| Paramètre  | Valeur          |
| ---------- | --------------- |
| Adresse IP | `223.0.0.2`     |
| Masque     | `255.255.255.0` |
| Passerelle | `223.0.0.1`     |

### 5.2 Configuration de l’interface WAN sur R1

Le WAN simulé est connecté sur **`g0/1`**.

```text
conf t
interface g0/1
 description WAN_SIM_TO_PC_INTERNET
 ip address 223.0.0.1 255.255.255.0
 ip nat outside
 no shutdown
end
wr mem
```

### 5.3 Test WAN

```text
ping 223.0.0.2
```

Le ping doit réussir avant toute mise en place du NAT centralisé.

## 6. Route par défaut sur R1

### Objectif

R1 doit utiliser le PC « Internet » comme prochain saut par défaut.

### Configuration sur R1

```text
conf t
ip route 0.0.0.0 0.0.0.0 223.0.0.2
end
wr mem
```

### Vérification

```text
show ip route | include 0.0.0.0
```

## 7. NAT centralisé sur R1

### Objectif

Tout le trafic issu des réseaux internes `10.0.0.0/8` doit sortir par **R1**, avec traduction d’adresse vers l’interface WAN.

### 7.1 Déclarer les interfaces inside sur R1

Les interfaces LAN locales de **R1** et les sous-interfaces de transit doivent être considérées comme **inside**.

```text
conf t
interface g0/0.2
 ip nat inside
interface g0/0.3
 ip nat inside
interface g0/0.99
 ip nat inside
interface g0/2.12
 ip nat inside
interface g0/2.13
 ip nat inside
end
wr mem
```

### 7.2 ACL NAT globale et PAT

```text
conf t
ip access-list standard NAT_INTERNET_ALL
 permit 10.0.0.0 0.255.255.255
exit
ip nat inside source list NAT_INTERNET_ALL interface g0/1 overload
end
wr mem
```

### 7.3 Vérification NAT

```text
show ip nat statistics
```

## 8. Schéma logique du NAT centralisé

```{mermaid}
flowchart LR
    SRC[Trafic source 10.0.0.0/8] --> IN[Interfaces NAT inside]
    IN --> R1[R1]
    R1 --> OUT[g0/1 NAT outside]
    OUT --> EXT[223.0.0.2]
```

Le NAT permet aux réseaux privés internes d’accéder au réseau externe simulé en utilisant l’adresse de sortie du routeur edge.

## 9. Annonce de la route par défaut via OSPF

### Objectif

R2 et R3 doivent apprendre dynamiquement la route par défaut depuis **R1**.

### 9.1 Sur R1 : annoncer la default route

```text
conf t
router ospf 1
 default-information originate
end
wr mem
```

### 9.2 Vérification sur R2 et R3

#### Sur R2

```text
show ip route | include 0.0.0.0
```

#### Sur R3

```text
show ip route | include 0.0.0.0
```

Le résultat attendu est une route par défaut apprise dynamiquement via OSPF.

## 10. Schéma logique de diffusion de la route par défaut

```{mermaid}
flowchart LR
    R1[R1\nDefault route locale] -->|default-information originate| OSPF[OSPF interne]
    OSPF --> R2[R2]
    OSPF --> R3[R3]
```

## 11. Tests de bout en bout

### 11.1 Test depuis un PC interne

Depuis un PC de n’importe quel groupe :

- ping vers `223.0.0.2`

### 11.2 Vérification NAT sur R1

Pendant les pings, sur **R1** :

```text
show ip nat translations
```

### 11.3 Vérifications OSPF

Sur **R1** :

```text
show ip ospf neighbor
```

Sur **R2** et **R3** :

```text
show ip ospf neighbor
```

## 12. Lecture fonctionnelle de la phase

```{mermaid}
sequenceDiagram
    participant PC as PC interne
    participant RI as Routeur interne
    participant R1 as R1 edge
    participant EXT as PC Internet simulé

    PC->>RI: paquet vers 223.0.0.2
    RI->>R1: envoi via route par défaut OSPF
    R1->>R1: NAT inside -> outside
    R1->>EXT: paquet traduit
    EXT-->>R1: réponse
    R1-->>RI: retour
    RI-->>PC: réponse finale
```

## 13. Contrôles finaux

### R1

```text
show ip route | include 0.0.0.0
show ip nat statistics
show ip nat translations
show ip ospf neighbor
ping 223.0.0.2
```

### R2

```text
show ip route | include 0.0.0.0
show ip ospf neighbor
ping 223.0.0.2
```

### R3

```text
show ip route | include 0.0.0.0
show ip ospf neighbor
ping 223.0.0.2
```

## 14. Synthèse

Dans cette phase :

- **R1** devient la sortie unique vers le WAN simulé ;
- **R2** et **R3** n’utilisent plus de WAN ni de NAT local ;
- le **NAT** est centralisé sur **R1** ;
- la **route par défaut** est propagée par **OSPF** ;
- l’interconnexion interne reste assurée par le switch de transit et les sous-interfaces OSPF.

Cette architecture prépare une réflexion sur la redondance WAN et les politiques de sortie qui seront abordées dans les phases suivantes.

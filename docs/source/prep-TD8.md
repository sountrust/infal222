# PREP-TD8 — Migration de l’interconnexion OSPF vers un trunk de transit

## Objectif

Jusqu’à présent, les routeurs étaient interconnectés par des liaisons Ethernet directes.
Cette architecture fonctionne, mais elle mobilise plusieurs interfaces physiques.

Dans cette phase préparatoire, l’architecture évolue afin de :

- remplacer les liaisons directes inter-routeurs par un **switch de transit** ;
- transporter les réseaux d’interconnexion sur un **trunk 802.1Q** ;
- faire fonctionner **OSPF sur des sous-interfaces** ;
- conserver la connectivité entre les groupes ;
- libérer une interface physique sur **R1** pour la future connexion WAN.

## Pré-requis

Les éléments suivants doivent être opérationnels :

- VLAN locaux de chaque groupe ;
- passerelles configurées sur les routeurs ;
- OSPF fonctionnel entre **R1**, **R2** et **R3** ;
- tests **LAN ↔ LAN** validés.

## 1. Principe de la migration

L’interconnexion inter-routeurs reposait jusqu’ici sur trois liaisons physiques directes.

Le besoin de la phase suivante impose de libérer une interface physique sur **R1** pour une future sortie WAN.

La solution retenue consiste à :

- conserver les trunks locaux vers les switches de groupe ;
- remplacer les liaisons inter-routeurs directes par un **switch de transit dédié** ;
- porter les réseaux d’interconnexion sur des **VLAN de transit** ;
- faire transiter OSPF sur des **sous-interfaces 802.1Q**.

## 2. Nouvelle architecture

Chaque routeur conserve :

- une interface pour le trunk local vers le switch du groupe ;
- une interface pour rejoindre le switch de transit.

Les interconnexions logiques entre routeurs sont désormais portées par trois VLAN de transit :

- **VLAN 12** : interconnexion **R1 ↔ R2**
- **VLAN 13** : interconnexion **R1 ↔ R3**
- **VLAN 23** : interconnexion **R2 ↔ R3**

Les réseaux IP restent inchangés :

- `10.255.12.0/30`
- `10.255.13.0/30`
- `10.255.23.0/30`

Le changement porte donc sur l’architecture **physique et logique de transport**, pas sur le plan d’adressage IP.

```{mermaid}
flowchart LR
    subgraph G1[Groupe 1]
        SW1[Switch G1]
        R1[R1]
        SW1 <-->|Trunk local| R1
    end

    subgraph G2[Groupe 2]
        SW2[Switch G2]
        R2[R2]
        SW2 <-->|Trunk local| R2
    end

    subgraph G3[Groupe 3]
        SW3[Switch G3]
        R3[R3]
        SW3 <-->|Trunk local| R3
    end

    ST[Switch de transit]

    R1 <-->|Trunk transit| ST
    R2 <-->|Trunk transit| ST
    R3 <-->|Trunk transit| ST
```

## 3. Plan d’adressage du transit

### VLAN 12 — R1 ↔ R2

- R1 : `10.255.12.1/30`
- R2 : `10.255.12.2/30`

### VLAN 13 — R1 ↔ R3

- R1 : `10.255.13.1/30`
- R3 : `10.255.13.2/30`

### VLAN 23 — R2 ↔ R3

- R2 : `10.255.23.1/30`
- R3 : `10.255.23.2/30`

### Tableau récapitulatif

| VLAN de transit | Liaison logique | Adresse côté 1   | Adresse côté 2   |
| --------------- | --------------- | ---------------- | ---------------- |
| 12              | R1 ↔ R2         | `10.255.12.1/30` | `10.255.12.2/30` |
| 13              | R1 ↔ R3         | `10.255.13.1/30` | `10.255.13.2/30` |
| 23              | R2 ↔ R3         | `10.255.23.1/30` | `10.255.23.2/30` |

## 4. Câblage retenu

Un **switch de transit** dédié est ajouté à l’architecture.

Convention utilisée :

- **R1** : `g0/2` vers le switch de transit
- **R2** : `g0/2` vers le switch de transit
- **R3** : `g0/2` vers le switch de transit

Les trunks locaux vers les switches de groupe restent inchangés.

## 5. Observation de l’existant

Avant toute modification, relever l’état actuel de l’interconnexion OSPF.

Sur chaque routeur :

```text
show ip ospf neighbor
show ip route ospf
show ip ospf interface brief
show ip interface brief
```

L’objectif est d’identifier :

- les interfaces actuellement utilisées pour OSPF ;
- les voisinages existants ;
- les routes apprises par OSPF.

## 6. Préparation du switch de transit

### 6.1 Création des VLAN de transit

```text
conf t
vlan 12
 name TRANSIT_R1_R2
vlan 13
 name TRANSIT_R1_R3
vlan 23
 name TRANSIT_R2_R3
end
wr mem
```

### 6.2 Configuration des trunks vers les routeurs

Exemple de raccordement :

- `fa0/1` vers R1
- `fa0/2` vers R2
- `fa0/3` vers R3

```text
conf t
interface range fa0/1 - 3
 switchport mode trunk
 switchport trunk allowed vlan 12,13,23
 no shutdown
end
wr mem
```

### 6.3 Vérification

```text
show vlan brief
show interfaces trunk
```

```{mermaid}
flowchart LR
    R1[R1 g0/2] <-->|802.1Q| ST[Switch de transit]
    R2[R2 g0/2] <-->|802.1Q| ST
    R3[R3 g0/2] <-->|802.1Q| ST
    ST --> V12[VLAN 12]
    ST --> V13[VLAN 13]
    ST --> V23[VLAN 23]
```

## 7. Suppression de l’ancienne interconnexion

Les anciennes liaisons inter-routeurs directes ne sont plus utilisées.

On retire donc leur adressage IP et on les met hors service.

Les interfaces LAN locales, les sous-interfaces VLAN et les loopbacks ne doivent pas être modifiées.

### R1

```text
conf t
interface g0/1
 no ip address
 shutdown
interface g0/2
 no ip address
 shutdown
end
wr mem
```

### R2

```text
conf t
interface g0/1
 no ip address
 shutdown
interface g0/2
 no ip address
 shutdown
end
wr mem
```

### R3

```text
conf t
interface g0/1
 no ip address
 shutdown
interface g0/2
 no ip address
 shutdown
end
wr mem
```

À ce stade, les voisinages OSPF inter-routeurs disparaissent temporairement.

Ce comportement est normal.

### Vérification

```text
show ip ospf neighbor
show ip route ospf
```

## 8. Mise en place des sous-interfaces de transit

Les nouvelles interconnexions logiques sont maintenant portées par les VLAN 12, 13 et 23.

### R1

```text
conf t
interface g0/2
 no shutdown
interface g0/2.12
 encapsulation dot1Q 12
 ip address 10.255.12.1 255.255.255.252
interface g0/2.13
 encapsulation dot1Q 13
 ip address 10.255.13.1 255.255.255.252
end
wr mem
```

### R2

```text
conf t
interface g0/2
 no shutdown
interface g0/2.12
 encapsulation dot1Q 12
 ip address 10.255.12.2 255.255.255.252
interface g0/2.23
 encapsulation dot1Q 23
 ip address 10.255.23.1 255.255.255.252
end
wr mem
```

### R3

```text
conf t
interface g0/2
 no shutdown
interface g0/2.13
 encapsulation dot1Q 13
 ip address 10.255.13.2 255.255.255.252
interface g0/2.23
 encapsulation dot1Q 23
 ip address 10.255.23.2 255.255.255.252
end
wr mem
```

### Vérification

```text
show ip interface brief
```

## 9. Adaptation de la configuration OSPF

OSPF ne doit plus fonctionner sur les anciennes interfaces physiques d’interconnexion.

Les voisinages doivent désormais se former sur les **sous-interfaces de transit**.

Les interfaces LAN locales restent annoncées dans OSPF, tout en restant **passives**.

### R1

```text
conf t
router ospf 1
 passive-interface default
 no passive-interface g0/2.12
 no passive-interface g0/2.13
end
wr mem
```

### R2

```text
conf t
router ospf 1
 passive-interface default
 no passive-interface g0/2.12
 no passive-interface g0/2.23
end
wr mem
```

### R3

```text
conf t
router ospf 1
 passive-interface default
 no passive-interface g0/2.13
 no passive-interface g0/2.23
end
wr mem
```

Les commandes `network` déjà présentes restent valides tant que les réseaux annoncés restent les mêmes :

- loopbacks ;
- réseaux de transit ;
- VLAN locaux.

## 10. Vérification du rétablissement d’OSPF

Sur chaque routeur :

```text
show ip ospf neighbor
show ip ospf interface brief
show ip route ospf
```

Le résultat attendu est le suivant :

- les voisinages OSPF sont de nouveau établis ;
- les routes OSPF vers les autres groupes réapparaissent ;
- les VLAN distants sont de nouveau atteignables.

```{mermaid}
flowchart TD
    A[Anciennes liaisons directes supprimées] --> B[Création des sous-interfaces de transit]
    B --> C[Réactivation OSPF sur g0/2.x]
    C --> D[Voisinages rétablis]
    D --> E[Routes OSPF de nouveau présentes]
```

## 11. Tests de connectivité

Depuis un poste d’un groupe, vérifier la connectivité vers les autres groupes.

Exemples :

- depuis un PC du groupe 1 VLAN 2 vers un PC du groupe 2 VLAN 2 ;
- depuis un PC du groupe 1 VLAN 2 vers un PC du groupe 3 VLAN 3 ;
- vers les passerelles distantes :
  - `10.2.2.254`
  - `10.3.3.254`

Ces tests doivent confirmer que le changement d’architecture n’a pas modifié le résultat fonctionnel attendu.

## 12. Comparaison avant / après

### Avant migration

```{mermaid}
flowchart LR
    R1[R1] --- R2[R2]
    R1 --- R3[R3]
    R2 --- R3[R3]
```

### Après migration

```{mermaid}
flowchart LR
    R1[R1 g0/2.x] <-->|Trunk transit| ST[Switch de transit]
    R2[R2 g0/2.x] <-->|Trunk transit| ST
    R3[R3 g0/2.x] <-->|Trunk transit| ST
```

Le résultat logique est conservé, mais l’architecture physique devient plus souple et prépare la suite.

## 13. Synthèse

Au départ, l’interconnexion OSPF reposait sur des liaisons physiques directes entre routeurs.

Après migration :

- l’interconnexion repose sur un **switch de transit** ;
- les échanges OSPF passent par un **trunk** ;
- les liens logiques sont portés par des **sous-interfaces 802.1Q** ;
- les réseaux de transit restent identiques ;
- la connectivité entre groupes est conservée.

Cette nouvelle architecture prépare la suite du travail en libérant une interface physique sur **R1** pour la future sortie WAN.

## 14. Commandes de contrôle à connaître

### Switch de transit

```text
show vlan brief
show interfaces trunk
```

### Routeurs

```text
show ip interface brief
show ip ospf neighbor
show ip ospf interface brief
show ip route ospf
```

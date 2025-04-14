# INFAL 222 – Jour 1
## Architecture réseau convergente, SDN et résilience distribuée

---

## 🧭 Titre du cours
**Architecture réseau d’entreprise convergente**  
*INFAL 222 – Réseaux étendus – Jour 1*

---

## 🎯 Objectifs de la séance
- Comprendre ce qu’est une architecture réseau convergente
- Introduire le concept de Software Defined Network (SDN)
- Comparer un réseau centralisé et un réseau distribué
- Découvrir la notion de résilience réseau

---

## 📘 Définition – Convergence réseau
**Convergence** = Regroupement des flux **voix**, **vidéo** et **données** sur une même infrastructure IP.

✅ Avant : infrastructures séparées pour chaque service  
✅ Maintenant : mutualisation via Ethernet/IP avec segmentation logique (VLAN)

---

## 🛣 Métaphore de la convergence
> *Une autoroute avec des voies réservées :*  
> - 🚑 VoIP = ambulances (priorité haute)  
> - 🚌 Vidéo = bus (voie dédiée)  
> - 🚗 Données classiques = voitures (flux best effort)

---

## 🧪 Exemple : Ports réseau et convergence
```plaintext
[PC] <---> [Téléphone IP] <-- Port Access (VoIP + Data) --> [Switch PoE]
[Caméra IP] <------------------- Port dédié VLAN Cam --> [Switch PoE]
```

---

## 🛠 Comportement attendu
- Le **téléphone IP** intègre un mini-switch : il relie le PC et transmet les trames avec les bons tags VLAN
- La **caméra IP** utilise un port dédié dans un VLAN vidéosurveillance
- Les **trunks** sont réservés aux interconnexions (uplinks)

---

## ⚙️ Configuration : VoIP + Données (Cisco)
```cisco
interface FastEthernet0/1
 description Poste avec téléphone IP
 switchport access vlan 10       ! Données utilisateur
 switchport voice vlan 20        ! Téléphonie IP
 switchport mode access
 spanning-tree portfast
```

---

## ⚙️ Configuration : Caméra IP
```cisco
interface FastEthernet0/2
 description Caméra IP - VLAN Vidéo
 switchport access vlan 30
 switchport mode access
 spanning-tree portfast
```

---

## 🔁 Spanning Tree Protocol (STP)
- **STP** évite les boucles réseau (tempêtes de broadcast)
- Comportement par défaut : attend ~30 secondes avant d’activer un port

🎯 **Problème** : trop long pour des équipements comme un téléphone VoIP

---

## ⚡ Portfast et sécurité
```cisco
interface range FastEthernet0/1 - 24
 spanning-tree portfast
 spanning-tree bpduguard enable
```
- `portfast` : active immédiatement le port (utile pour les postes)
- `bpduguard` : protège des erreurs de câblage (ex. : switch branché par erreur)

---

## 🌪 Boucles & Tempêtes de Broadcast
- Une boucle = trames **broadcast** qui tournent en boucle sur plusieurs ports
- Résultat : saturation du réseau, effondrement
- **STP bloque dynamiquement un lien pour casser la boucle**

---

## 🌐 Protocoles utilisant le Broadcast
- **ARP** (résolution IP-MAC)
- **DHCP** (découverte et assignation IP)
- **RIP v1** (routage simple)
- **NetBIOS/SMB**, **CDP/LLDP** (découverte)

---

## 🔍 Rappel : fonctionnement de ARP
```plaintext
Host A : Qui a 192.168.1.10 ? (broadcast)
Host B : C’est moi ! MAC = 00:1B:44:11:3A:B7
```

- Requête envoyée en broadcast (FF:FF:FF:FF:FF:FF)
- Réponse en unicast

---

## ✅ Bénéfices de la convergence
- Mutualisation des câbles et équipements
- Meilleure visibilité et gestion
- Réduction des coûts
- Compatible avec QoS (priorisation)
- ⚠️ Exige une bonne conception initiale

---

*(la suite du document pourra continuer depuis cette structure visuelle claire avec des emojis, sections courtes et titres explicites)*

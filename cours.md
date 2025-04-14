# INFAL 222 - Jour 1
## Architecture réseau convergente, SDN et résilience distribuée

---

### Titre
**Architecture réseau d’entreprise convergente**  
Jour 1 - INFAL 222 - Réseaux étendus

---

### Objectifs du jour
- Comprendre ce qu’est une architecture réseau convergente
- Introduire le Software Defined Network (SDN)
- Distinguer un réseau centralisé d’un réseau distribué
- Appréhender la notion de résilience

---

### DÉFINITION : convergence réseau
**Convergence** = regroupement des flux **voix**, **vidéo** et **données** sur une même infrastructure IP

✅ Avant : infrastructures séparées pour chaque type de service  
✅ Aujourd’hui : mutualisation via Ethernet/IP avec segmentation logique

---

### DÉFINITION : suite
**Métaphore :** comme une autoroute avec des voies prioritaires : 
- les ambulances (VoIP) passent en premier, 
- les bus (vidéo) ont leur file dédiée, 
- les voitures (données classiques) attendent s’il le faut

**Technique :** utilisation de VLANs (VoIP, Data, Surveillance) pour distinguer les services

---

### EXEMPLE : Ports réseau et convergence
```
[PC] <---> [Téléphone IP] <-- Port Access (VoIP + Data) --> [Switch PoE]
[Caméra IP] <------------------- Port dédié VLAN Cam --> [Switch PoE]
```
---

### EXEMPLE : suite

- Le **téléphone IP** intègre un switch Ethernet : le PC et le téléphone partagent un port via 2 VLANs (Data et VoIP)
- La **caméra IP** est connectée sur un port dédié (PoE), souvent dans un VLAN séparé (sécurité ou vidéosurveillance)

**Remarque :** les trunks sont réservés aux liens inter-switch ou uplinks vers routeurs/contrôleurs

---

### CONFIG EXEMPLE : VoIP + Data sur un port
```cisco
interface FastEthernet0/1
 description Poste avec téléphone IP
 switchport access vlan 10       ! VLAN Data
 switchport voice vlan 20        ! VLAN VoIP
 switchport mode access
 spanning-tree portfast
```

---

### CONFIG EXEMPLE : suite
- VLAN 10 : données utilisateur
- VLAN 20 : téléphonie IP (Cisco CallManager, etc.)
- Le téléphone sépare les trames et applique les bons tags

---

### CONFIG EXEMPLE : Caméra IP sur VLAN dédié
```cisco
interface FastEthernet0/2
 description Caméra IP - VLAN Vidéosurveillance
 switchport access vlan 30
 switchport mode access
 spanning-tree portfast
```
---

### CONFIG EXEMPLE : suite

- VLAN 30 : réservé à la vidéosurveillance
- Ce port alimente uniquement une caméra IP
- Généralement couplé à une stratégie QoS ou ACL spécifique sur le réseau

---

### CONTEXTE : Spanning Tree Protocol (STP)
**STP** est un protocole qui empêche les boucles de commutation dans un réseau Ethernet.

- Sans STP, une boucle physique provoque une tempête de broadcast
- Le switch attend que STP stabilise la topologie avant d’activer un port (jusqu’à 30 secondes !)

**Problème :** trop long pour un poste client ou un téléphone VoIP

---

### SPANNING-TREE PORTFAST
**portfast** : active immédiatement un port access sans attendre le calcul STP

- Utilisation : ports connectés à des hôtes finaux (PC, téléphones, caméras)
- Interdit sur des ports trunk/interconnexion (risque de boucle !)

---

### BONNES PRATIQUES

```cisco
interface range FastEthernet0/1 - 24
 spanning-tree portfast
 spanning-tree bpduguard enable
```
- **bpduguard** protège contre une erreur de câblage (ex. : si un switch est branché sur un port portfast)

---

### BOUCLES DE COMMUTATION ET BROADCAST STORM
**Boucle de commutation** : se produit quand deux ports forment un chemin redondant non contrôlé entre switches

- Les trames de type **broadcast** sont inondées sur tous les ports
- Dans une boucle, elles circulent **à l’infini**, saturant les liens et les CPUs des équipements
- Résultat : effondrement du réseau (tempête de broadcast)

**STP** permet de bloquer dynamiquement un lien pour casser la boucle

---

### PROTOCOLES UTILISANT LE BROADCAST
Les broadcasts sont indispensables à certains protocoles, en particulier au niveau 2 et 3 :

- **ARP** : résolution des adresses IP en adresses MAC
- **DHCP Discover / Request** : recherche de serveur d’adresses
- **Routing Information Protocol (RIPv1)** : envois périodiques de tables
- **NetBIOS/SMB** : découverte de services Windows
- **CDP/LLDP** (si configurés en mode écoute large)

---

### RAPPEL : Fonctionnement de ARP
**ARP (Address Resolution Protocol)**

- Objectif : associer une adresse IP à une adresse MAC (niveau 2)
- Fonctionne par **broadcast ARP Request** (destinée à FF:FF:FF:FF:FF:FF)
- Le destinataire répond en unicast avec son adresse MAC

---

### EXEMPLE
```
Host A : Qui a 192.168.1.10 ? (broadcast)
Host B : C’est moi ! Mon MAC est 00:1B:44:11:3A:B7
```

ARP est une source fréquente de broadcast, mais essentielle au fonctionnement IP

---

### BÉNÉFICES DE LA CONVERGENCE
- Mutualisation des équipements et des câbles
- Réduction des coûts d’infrastructure
- Meilleure gestion centralisée
- Gestion fine via la QoS (prochaine séance)
- ⚠️ Demande une conception réseau rigoureuse

---

### INTRODUCTION : Software Defined Networking (SDN)
**Définition :** Le SDN (réseau défini par logiciel) est un paradigme qui sépare le plan de contrôle (logique) du plan de données (acheminement).

- L’équipement réseau devient « programmable »
- Le contrôle est centralisé via un contrôleur SDN
- Il peut concerner **les switches comme les routeurs**, selon les besoins

---

### Contexte d’émergence
- Années 2010, besoin d'agilité dans les datacenters, virtualisation croissante
- Difficulté à gérer les configurations manuelles à grande échelle

**Acteurs clés :** OpenFlow, Cisco ACI, VMware NSX, Juniper Contrail

---

### PRÉREQUIS : Mise en place du SDN
**Mise en situation pédagogique :**
Vous venez de recevoir une pile de routeurs et de switches pour un nouveau site. Objectif : déployer une infrastructure SDN.

**Question :** Peut-on simplement les brancher et contrôler tout à distance ?

---

### Réponse : Non
Il faut d’abord :
1. **Accéder à chaque équipement individuellement**
2. **Appliquer une configuration minimale (masterisation)**
3. **Assurer leur connectivité au contrôleur SDN (IP, VLAN, routage, sécurité)**

---

### EXEMPLE DE MASTERISATION
Objectif : préparer chaque équipement pour être piloté à distance.

```text
- Configuration IP fixe sur interface de gestion
- Ajout d'une route par défaut ou passerelle
- Activation du protocole de gestion (SSH, API REST, etc.)
```

---

### EXEMPLE  CISCO
```cisco
interface vlan 1
 ip address 192.168.100.10 255.255.255.0
!
ip default-gateway 192.168.100.1
ip ssh version 2
username admin secret cisco123
```

Cette base permet au contrôleur ou à un script de prendre la main à distance.

---

### PRISE DE CONTRÔLE VIA API
Une fois l’équipement accessible :
- Le contrôleur SDN ou un outil d’automatisation peut **pousser des configurations**.
- Cela passe souvent par des **API REST** utilisant **JSON**.

---

### EXEMPLE
```http
POST /api/node/mo/uni/tn-Prod/app-Web.json
{
  "fvAp": {
    "attributes": {
      "name": "WebApp"
    }...
```
Ici, le contrôleur configure dynamiquement un tenant ou une politique réseau (Cisco ACI, par ex).

---

### Contrôle des switches via SDN
Le SDN permet de piloter les switches :

- Création et affectation de VLANs
- Activation/désactivation de ports
- Configuration des politiques QoS
- Application d’ACL dynamiques (filtrage par profil utilisateur)

**Exemple d’utilisation :** déployer automatiquement un VLAN VoIP avec priorité haute dès qu’un téléphone est détecté.

---

### Contrôle des routeurs via SDN
Le SDN pilote aussi les fonctions avancées des routeurs :

- Politique de routage (OSPF, BGP)
- Encapsulation (VXLAN, MPLS, GRE)
- Routage basé sur l’application ou le contexte utilisateur

**Exemple :** forcer le trafic voix vers un lien WAN spécifique avec un chemin de secours automatique

---

### Supervision des services par le SDN
Le SDN permet une **orchestration complète** de services réseau :

- Load-balancing applicatif
- Firewalling dynamique (contrôle basé sur utilisateur, appli ou heure)
- Routage applicatif ou contextuel

**Bénéfice :** centraliser toutes les politiques réseau et sécurité dans une seule interface contrôleur.

---

### Centralisé vs Distribué (1/2)

| Modèle       | Description                                                                 | Exemples concrets                                 |
|--------------|-----------------------------------------------------------------------------|---------------------------------------------------|
| **Centralisé** | Une seule entité prend les décisions (contrôle, configuration, routage)     | - Contrôleur SDN unique<br>- Serveur DHCP central<br>- Réseau d’entreprise classique |
| **Distribué** | L’intelligence est répartie entre plusieurs nœuds, chacun autonome           | - Routage BGP entre FAI<br>- DNS hiérarchique<br>- Systèmes de microservices |

---

### Centralisé vs Distribué (2/2)

**Périmètre :**
- **Infrastructure** : commutateurs, routeurs, datacenters
- **Plan de contrôle** : routage, sécurité, QoS
- **Plan de service** : distribution applicative, données, cache

**Intérêt pédagogique :** comprendre quand la centralisation est simple et efficace, et quand la distribution est nécessaire pour la résilience, la scalabilité et l’adaptabilité

---

### POURQUOI DISTRIBUER ? (1/2)

- Résilience accrue : la panne d’un nœud n’interrompt pas le fonctionnement global
- Performance : les données et décisions sont plus proches des utilisateurs

---

### POURQUOI DISTRIBUER ? (2/2)

- Scalabilité horizontale : on ajoute des nœuds sans impacter le système global
- Tolérance aux pannes : indispensable dans les grandes infrastructures

---

### Exemple technique : DNS (1/2)

- DNS centralisé : chaque requête va à un serveur maître → charge + latence

- DNS distribué : chaque région/FAI dispose de serveurs en cache → rapide, tolérant aux pannes

---

### Réseaux maillés (1/2)

**Définition :** tous les nœuds sont connectés à plusieurs autres, ce qui permet un acheminement dynamique.

- Chaque nœud peut relayer le trafic d’un autre
- Le routage s’adapte aux défaillances

---

### Réseaux maillés (2/2)

- Utilisé dans : IoT, Wi-Fi maillé (Google Nest), réseaux militaires

**Exemple logiciel :**
- Service Mesh dans les microservices (ex : Istio avec Kubernetes)

---

### Schéma : topologie distribuée
```
   [Service A]---+
                  |
[User]---[Edge]---[Backbone]---[Datacenter]
                  |
   [Service B]---+
```
Chaque site ou service peut fonctionner indépendamment et assurer la continuité de service

---

### Résilience réseau (1/2)

**Définition :** capacité du réseau à maintenir ses services malgré des pannes, coupures ou attaques.

**Mécanismes clés :**
- Redondance des équipements et des chemins (liens multiples, HSRP/VRRP)
- Routage dynamique avec recalcul automatique (OSPF, BGP)

---

### Résilience réseau (2/2)

- Load-balancing entre services ou accès WAN
- Réplication des services ou données sur plusieurs sites (cloud hybride, edge)

**Exemples :**
- Dans un campus, si un switch de distribution tombe, le second prend le relais
- Dans un réseau d’entreprise multi-sites, un tunnel VPN de secours est activé si le principal tombe

**Métaphore :** comme une ville équipée de générateurs de secours et de routes alternatives :
si une ligne électrique ou une route est coupée, une autre prend automatiquement le relais.


---

### Transition vers QoS (Jour 2)
**Problématique :** tous les flux ne se valent pas !
- VoIP : sensible à la latence
- Vidéo : sensible à la gigue
- Fichiers : tolèrent les délais

**La QoS permettra :**
- de différencier les traitements,
- d’implémenter une politique de priorisation efficace

**Question de réflexion :** si tout le monde lance un appel Teams et regarde Netflix, qui doit être prioritaire ?

### Annexe – Approfondissement sur le routage et l'encapsulation dans le SDN

---

### 🧭 Qu’est-ce qu’un protocole de routage ?
Un protocole de routage permet à un routeur de **décider par quel chemin** envoyer les paquets IP vers une destination donnée.
Le SDN supervise ces choix automatiquement, selon des politiques métier.

---

### 📡 OSPF expliqué simplement
- **OSPF** fonctionne **à l’intérieur** d’un réseau (Intra-entreprise).
- Il construit une **carte complète du réseau** (état de liens).
- Comme un GPS local, il choisit la **route la plus rapide** automatiquement.
- Il peut recalculer un autre chemin en cas de panne (convergence rapide).

---

### 🌍 BGP : le GPS de l’Internet
- **BGP** relie **différents réseaux** (ex : Orange ↔ SFR).
- Il choisit les routes selon des **critères commerciaux ou techniques** (coût, performance).
- Il fonctionne **à très grande échelle**, comme un GPS entre pays.
- Le SDN peut influer sur ses choix en cas de besoin (failover, QOS).

---

### 🔄 VLAN – Segmenter un réseau local
- Permet de **séparer logiquement les machines** sur un même câble.
- Exemple : RH et Compta dans des VLANs distincts → communication impossible sans routage.
- Limité à **4096 VLANs**.

---

### 📦 VXLAN – Transporter des VLANs sur IP
- VXLAN encapsule un réseau **dans un autre réseau IP** (UDP).
- Cela permet de **connecter deux VLANs éloignés** via un backbone IP.
- Utilisé dans **NSX-T** pour connecter des VMs comme si elles étaient sur le même switch.
- Capacité : jusqu’à **16 millions de réseaux isolés** (vs 4096 pour VLAN).

---

### 🌀 GRE et MPLS
- **GRE** : tunnel simple point à point → relie deux sites distants via Internet.
- **MPLS** : réseau à base de labels pour **accélérer et prioriser** le traitement des paquets.
- Très utilisé par les opérateurs pour les clients multisites.



# 🧑‍🏫 Organisation pédagogique – Simulation VXLAN & VPN (Projet INFAL 222)

## 🎯 Objectif final
Mettre en œuvre une infrastructure réseau simulée interconnectée via VPN (Stormshield) et VXLAN (VyOS) entre deux baies distinctes (Proxmox + EVE-NG), hébergeant des VMs dans un même réseau logique.

---

## 🧩 Répartition des groupes

> La classe est divisée en **2 demi-groupes**, chacun reproduisant **une infrastructure miroir** :

- **Baie A** : Proxmox A + EVE-NG A + Stormshield A
- **Baie B** : Proxmox B + EVE-NG B + Stormshield B

Chaque demi-groupe est divisé en **3 ateliers techniques** :

| Atelier        | Rôle dans le projet                          | Outils utilisés                |
|----------------|----------------------------------------------|-------------------------------|
| **Atelier 1**  | Déploiement & gestion de Proxmox + EVE-NG   | Serveur physique Proxmox      |
| **Atelier 2**  | Configuration de VyOS pour VXLAN            | VyOS (via GNS3 localement)    |
| **Atelier 3**  | Configuration de Stormshield pour VPN       | Stormshield physique          |

---

## 🛠️ Étapes pédagogiques par atelier

### 🔧 Atelier 1 – Proxmox + EVE-NG

1. Installer et configurer **Proxmox** sur la baie
2. Déployer EVE-NG comme VM dédiée
3. Vérifier l’accès SSH + Web UI
4. Préparer les ressources réseau (bridges, trunk, etc.)

### 🌐 Atelier 2 – VyOS + VXLAN (local sur GNS3)

1. Installer **GNS3** localement (sur les postes élèves)
2. Télécharger l’image ISO **VyOS open source**
3. Créer une topologie GNS3 simple :
   - 2 VyOS → tunnel VXLAN
   - 2 TinyCore Linux VMs (ou Alpine) sur chaque VyOS
4. Valider la communication dans le **même sous-réseau VXLAN**

> Cette configuration sera ensuite transposée dans EVE-NG.

### 🛡️ Atelier 3 – Stormshield (VPN inter-baie)

1. Connexion via console/port série si nécessaire
2. Configuration des **zones LAN, WAN, DMZ**
3. Activation du **serveur DHCP** côté LAN
4. Création d’un tunnel **VPN site-à-site** entre les 2 équipements
5. Test de connectivité (ping entre baies)

---

## 🧬 Intégration finale

Chaque moitié de classe devra, une fois l’ensemble fonctionnel :

1. **Déployer VyOS sur EVE-NG** dans chaque baie
2. Simuler deux VMs clientes (TinyCore/Alpine) sur chaque infra
3. Configurer VXLAN entre les VyOS
4. Faire passer la communication inter-VM **au travers du VPN Stormshield**
5. Vérifier :
   - Réseau commun logique (ex. : 192.168.50.0/24)
   - Visibilité entre VMs (ping)
   - Étanchéité en cas de désactivation du VPN

---

## ✅ Livrables attendus

- Schéma global de l’architecture (VXLAN + VPN)
- Configurations commentées (VyOS + Stormshield)
- Journal de test & ping (screenshots ou fichiers texte)
- Synthèse par groupe (1 page par atelier)

---

## 🧠 Compétences mobilisées

- Compréhension des protocoles VPN (IPsec, tunnels)
- Configuration réseau de niveau 2 et 3 (VLAN, routage, VXLAN)
- Manipulation d’un firewall matériel (Stormshield)
- Simulation d’environnements distribués complexes

---

Tu peux maintenant démarrer les ateliers en parallèle pendant que les serveurs sont configurés 🔄


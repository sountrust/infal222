![Docs](https://github.com/<utilisateur>/<nom-du-depot>/actions/workflows/docs-pages.yml/badge.svg)

# INFAL 222 – Administration avancée des réseaux étendus

Bienvenue sur le dépôt de ressources du cours **INFAL 222**.

Ce cours a pour objectif de vous familiariser avec l’administration avancée des réseaux étendus d’entreprise, en articulant progressivement :

- la conception d’une architecture réseau local convergée ;
- la segmentation logique par VLAN et le routage inter-VLAN ;
- l’interconnexion de plusieurs sites ou groupes via un protocole de routage interne ;
- la mise en place d’une sortie WAN, du NAT et de la diffusion de la route par défaut ;
- la résilience, la redondance et les premières notions de routage externe avec **eBGP** ;
- l’ouverture vers le **SDN**, la supervision, la centralisation et les architectures distribuées.

> Ce dépôt contient des supports de cours, travaux dirigés, exercices, corrigés et ressources d’évaluation, en accès progressif.

---

## 📁 Structure du dépôt

```text
.
├── README.md                 # Présentation du dépôt
├── cours.md                  # Contenu principal du cours
├── INFALL222-jour1.pptx      # Slides PowerPoint de la 1re séance
├── exo_convergence.md        # Exercice sur l’architecture convergente
├── exo_sdn.md                # Exercice d’introduction au SDN
├── cor_convergence.md        # Corrigé – architecture convergente
├── cor_sdn.md                # Corrigé – exercice SDN
├── TD5.pdf                   # Router-on-a-stick, VLAN et routage inter-VLAN
├── TD6.pdf                   # Segmentation et consolidation de l’architecture locale
├── TD7.pdf                   # Routage OSPF entre les routeurs internes
├── PREP-TD8.pdf              # Migration vers un trunk de transit pour préparer le WAN
├── TD8.pdf                   # WAN simulé, NAT centralisé et route par défaut via OSPF
├── TD9.pdf                   # Redondance WAN et découverte de l’eBGP avec deux FAI simulés
└── corriges/                 # Corrigés, grilles et ressources enseignants
```

> Les noms de fichiers peuvent évoluer selon le format réellement déposé (`.md`, `.pdf`, `.docx`, `.pptx`).

---

## 🧑‍🎓 Public visé

Ce cours s’adresse à des étudiants de **niveau 3e année**, disposant déjà de bases sur :

- l’adressage IPv4 ;
- les VLAN ;
- les principes de commutation et de routage ;
- l’usage d’équipements Cisco en environnement pédagogique.

---

## 🧠 Objectifs pédagogiques

À l’issue du cours, vous devez être capables de :

- comprendre les enjeux d’une infrastructure réseau convergée ;
- distinguer les rôles respectifs de la commutation, du routage interne et du routage externe ;
- mettre en œuvre une architecture locale segmentée par VLAN ;
- configurer un routage inter-VLAN de type _router-on-a-stick_ ;
- établir un routage dynamique interne avec **OSPF** ;
- faire évoluer une architecture pour intégrer un **WAN simulé** ;
- centraliser une sortie Internet avec **NAT** et route par défaut ;
- introduire la redondance WAN et les premières notions de **BGP / eBGP** ;
- identifier les principes de résilience, de continuité de service et de secours ;
- comprendre les apports du **SDN**, des approches centralisées et des architectures distribuées.

---

## 🧪 Progression pédagogique

Le dépôt suit une logique de montée en complexité :

1. **Architecture convergente et fondamentaux**
   - convergence voix / vidéo / données ;
   - segmentation logique ;
   - introduction au SDN ;
   - centralisation, distribution, supervision.

2. **Architecture locale d’entreprise**
   - VLAN ;
   - trunks 802.1Q ;
   - routage inter-VLAN ;
   - bonnes pratiques de structuration des interfaces.

3. **Interconnexion et routage interne**
   - réseaux de transit ;
   - OSPF ;
   - loopback et router-id ;
   - interfaces passives et voisinages.

4. **Évolution d’architecture et accès WAN**
   - migration vers un trunk de transit ;
   - WAN simulé ;
   - NAT centralisé ;
   - injection d’une route par défaut.

5. **Redondance et routage externe**
   - double sortie WAN ;
   - FAI simulés ;
   - eBGP ;
   - AS ;
   - première approche de la résilience et des politiques de routage.

---

## 📌 Usage pédagogique

Les ressources du dépôt sont conçues pour un usage combiné :

- **cours** pour les notions et les schémas d’architecture ;
- **TD** pour la mise en œuvre progressive ;
- **QCM** pour la vérification des connaissances et compétences ;
- **corrigés** pour l’auto-évaluation ou l’accompagnement enseignant.

Selon les activités, les documents peuvent être lus directement en `.md` ou diffusés sous des formats exportés (`.pdf`, `.pptx`, `.docx`).

Certaines ressources peuvent être réservées à l’enseignant selon l’organisation retenue.

---

## 📜 Licence

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

Ce contenu est publié sous la licence **Creative Commons BY-NC-SA 4.0**.
Vous pouvez l’utiliser, le modifier et le partager **à des fins non commerciales**, en citant l’auteur et en conservant la même licence.

## Documentation en ligne

Le support de cours est publié en HTML via GitHub Pages.

- **Consulter le cours en ligne** : [Documentation HTML](https://<utilisateur>.github.io/<nom-du-depot>/)
- **Téléchargements** : les artefacts HTML et PDF sont disponibles dans l’onglet **Actions** du dépôt après chaque build.

---

## ✉️ Contact

Pour toute question ou remarque pédagogique : **[paul@sountrust.fr](mailto:paul@sountrust.fr)**

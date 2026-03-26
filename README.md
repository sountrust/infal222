![Build Docs](https://github.com/sountrust/infal222/actions/workflows/docs-pages.yml/badge.svg)

# INFAL 222 — Administration avancée des réseaux étendus

Bienvenue sur le dépôt du cours **INFAL 222**.

Ce dépôt contient les **sources Markdown** du cours, des CM, des TD et des exercices. La documentation est publiée en **HTML via GitHub Pages**, ce qui permet une consultation plus confortable qu’un ensemble de fichiers binaires lourds à maintenir.

## Accès rapide

- **Documentation en ligne** : [https://sountrust.github.io/infal222/](https://sountrust.github.io/infal222/)
- **Page du dépôt** : [https://github.com/sountrust/infal222](https://github.com/sountrust/infal222)
- **Workflow de publication** : `.github/workflows/docs-pages.yml`

## Organisation du contenu

Le dépôt suit une logique de progression pédagogique :

- fondamentaux de l’architecture réseau convergée ;
- segmentation logique par VLAN et routage inter-VLAN ;
- interconnexion et routage interne avec **OSPF** ;
- préparation et mise en place d’un **WAN simulé** ;
- redondance WAN et découverte de **BGP / eBGP** ;
- redondance locale de passerelle avec **HSRP** ;
- ouverture vers les approches modernes de pilotage réseau.

## Lecture rapide depuis GitHub

### Supports généraux

- [Cours principal](cours.md)
- [CM — OSPF et ECMP](CM-OSPF.md)
- [CM — BGP](CM-BGP.md)
- [CM — HSRP, VRRP, GLBP, SDN et SD-WAN](CM-HSRP-VRRP.md)

### Travaux dirigés

- [TD6 — Préparation d’une infrastructure cohérente](TD6.md)
- [TD7 — Interconnexion, OSPF et ECMP](TD7.md)
- [PREP-TD8 — Migration vers un trunk de transit](PREP-TD8.md)
- [TD8 — WAN simulé, NAT centralisé et route par défaut via OSPF](TD8.md)
- [TD9 — Redondance WAN et découverte de l’eBGP](TD9.md)
- [TD10 — Refonte du plan VLAN, mutualisation et HSRP](TD10.md)

### Exercices et compléments

- [Exercice — Architecture convergente](exo_convergence.md)
- [Exercice — Introduction au SDN](exo_sdn.md)
- [Lab — VXLAN, datacenter et SDN](lab_vxlan_dc_sdn.md)

## Structure du dépôt

```text
.
├── README.md
├── cours.md
├── CM-BGP.md
├── CM-OSPF.md
├── CM-HSRP-VRRP.md
├── TD6.md
├── TD7.md
├── PREP-TD8.md
├── TD8.md
├── TD9.md
├── TD10.md
├── exo_convergence.md
├── exo_sdn.md
├── lab_vxlan_dc_sdn.md
├── docs/
│   ├── requirements.txt
│   ├── Makefile
│   ├── source/
│   │   ├── conf.py
│   │   └── index.md
│   └── build/   # ignoré par git
└── .github/
    └── workflows/
        └── docs-pages.yml
```

## Public visé

Ce cours s’adresse à des étudiants de **niveau 3e année**, disposant déjà de bases en :

- adressage IPv4 ;
- VLAN ;
- commutation et routage ;
- équipements Cisco en environnement pédagogique.

## Objectifs pédagogiques

À l’issue du cours, les étudiants doivent être capables de :

- comprendre les enjeux d’une infrastructure réseau convergée ;
- distinguer commutation, routage interne et routage externe ;
- mettre en œuvre une architecture VLAN cohérente ;
- configurer un routage inter-VLAN de type _router-on-a-stick_ ;
- établir un routage dynamique interne avec **OSPF** ;
- comprendre la logique **ECMP** et la résilience de chemin ;
- intégrer un **WAN simulé** avec route par défaut et **NAT** ;
- découvrir les principes de **BGP / eBGP** et des **AS** ;
- mettre en place une redondance de passerelle avec **HSRP** ;
- situer ces mécanismes par rapport aux approches modernes comme **SDN** et **SD-WAN**.

## Choix de publication

Le dépôt ne contient plus de documents binaires générés.

Le choix retenu est le suivant :

- **les sources Markdown sont versionnées** ;
- **la documentation HTML est générée automatiquement** ;
- **la consultation principale se fait via GitHub Pages** ;
- GitHub reste également un point d’entrée pratique pour lire directement les fichiers `.md`.

Cette approche simplifie la maintenance du dépôt, évite la duplication des formats et garde une source de vérité unique.

## Bonne pratique retenue pour un cours sur GitHub

La pratique adoptée ici est la suivante :

- utiliser le `README.md` comme **porte d’entrée courte et claire** ;
- proposer à la fois :
  - un accès direct aux **fichiers Markdown** dans le dépôt ;
  - un accès à la **documentation HTML** pour une lecture structurée ;

- conserver dans Git uniquement les **sources** et non les exports binaires générés.

Autrement dit :

- **GitHub** sert à lire rapidement les sources et à suivre le contenu ;
- **GitHub Pages** sert à consulter le cours dans une forme plus confortable.

## Licence

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

Ce contenu est publié sous la licence **Creative Commons BY-NC-SA 4.0**.
Vous pouvez l’utiliser, le modifier et le partager **à des fins non commerciales**, en citant l’auteur et en conservant la même licence.

## Contact

Pour toute question ou remarque pédagogique : [paul@sountrust.fr](mailto:paul@sountrust.fr)

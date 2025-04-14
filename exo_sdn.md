## 🔍 Exercice – Intégrer un contrôleur SDN dans un réseau existant

### 🎯 Objectif pédagogique
Comprendre comment une infrastructure réseau traditionnelle peut évoluer vers une architecture centralisée pilotée par un **contrôleur SDN**, même avec des équipements non compatibles à 100 %.

---

### 🏢 Contexte
Votre entreprise fonctionne avec des équipements classiques :
- 🔌 Switches Cisco 2960
- 🌐 Routeurs Cisco 2900

La direction souhaite améliorer :
- La gestion du réseau
- La supervision globale
- L’automatisation de certaines tâches

💡 Le SDN offrirait une **vision centralisée** et plus dynamique du réseau, sans devoir remplacer tous les équipements d’un coup.

---

### 🧩 Mission
Proposez une **stratégie d’intégration SDN progressive**, adaptée à cette infrastructure existante. L’objectif est de commencer à centraliser la supervision et certaines tâches automatisables.

Répondez aux points suivants en menant une petite recherche documentaire :

---

### 📋 Questions-guides

1. 🧠 **Quel type de contrôleur SDN conviendrait ?**
   - Recherchez des logiciels (open-source ou non) pouvant servir de point de gestion réseau.

2. 🔍 **Vos équipements sont-ils compatibles ?**
   - Consultez leurs spécifications (interfaces d’administration, protocoles disponibles : SSH, SNMP, etc.)

3. 📊 **Quelles données peut-on déjà superviser ?**
   - Donnez quelques exemples d’infos accessibles sans modification majeure.

4. ⚙️ **Peut-on automatiser certaines tâches ?**
   - Renseignez-vous sur les outils utilisables sans SDN complet (scripts, Ansible, etc.)

5. 🧱 **Quelles seraient les étapes d’une transition douce ?**
   - Imaginez un plan simple : test local, supervision, automatisation, puis intégration réelle

---

### 📝 Travail attendu
Un **court dossier (1 à 2 pages)** contenant :
- 🖥 Le nom d’un contrôleur SDN proposé
- 📌 Une brève description de ses fonctions
- 🧩 Un aperçu des limitations avec votre matériel actuel
- 🛠 Un plan en 2 ou 3 étapes pour intégrer ce SDN
- 🗺 Un schéma réseau illustratif (topologie avant/après ou mixte)
- 🔗 Quelques liens vers les ressources consultées

---

### 💡 Pistes pour vos recherches
- Sites officiels de projets : OpenDaylight, Floodlight, Ryu, Cisco DNA Center
- Blogs, forums techniques, retours d’expérience
- Tutoriels d’automatisation avec équipements Cisco

🔎 *Mots-clés utiles :* "SDN Cisco traditionnels", "OpenFlow sur switch classique", "gestion switch Cisco via Ansible"

---

### 🚀 Finalité pédagogique
Ce travail vous initie aux **principes du SDN** appliqués à un contexte réel, avec des contraintes matérielles. Il vous prépare à penser réseau de manière **modulaire, automatisable et évolutive**.

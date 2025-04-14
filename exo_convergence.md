## 🧪 Exercice – Appliquer la convergence réseau dans un environnement réel

### 🎯 Objectif pédagogique
Comprendre comment les principes de convergence réseau (voix, vidéo, données) peuvent s’appliquer concrètement à une infrastructure complexe.

---

### 🏥 Contexte : réseau d’un hôpital moderne

Un hôpital utilise de nombreux systèmes connectés :
- 📞 Téléphones IP pour les appels internes
- 🎥 Caméras de vidéosurveillance
- 💻 Postes informatiques pour dossiers médicaux
- 📶 Bornes Wi-Fi pour visiteurs et personnel
- 🖥 Serveurs d’imagerie médicale (scanner, IRM)

Tous ces flux doivent cohabiter sur un même réseau tout en restant **sécurisés**, **isolés** et **priorisés** selon leur importance.

---

### 📋 Mission
En vous appuyant sur les concepts vus en cours, proposez **une architecture réseau convergente adaptée à un hôpital**, en répondant aux points suivants :

1. 🧩 **Quels VLANs créer ?**
   - Pour quels types d’équipements ?
   - Quels bénéfices de cette séparation logique ?

2. 🔌 **Connexion des équipements**
   - Comment connecter un **téléphone IP + PC** sur un même port ?
   - Quel traitement pour les **caméras IP** ?
   - Et pour les **postes utilisateurs** ?

3. ⚙️ **Paramétrage des ports physiques**
   - Quels ports nécessitent **PoE**, **portfast**, ou des mécanismes de **sécurité** ?

4. 🔧 **Protocoles ou fonctions associés**
   - Citez ceux étudiés en cours : ex. `STP`, `portfast`, `BPDU Guard`, `VLAN voix`, `ARP

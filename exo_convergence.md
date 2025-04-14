### 🧪 **Exercice – Appliquer la convergence réseau dans un environnement réel**

---

#### 🎯 **Objectif pédagogique**
> 💡 *Comprendre concrètement comment les principes de convergence réseau (voix, vidéo, données) peuvent être appliqués dans une infrastructure moderne.*

---

### 🏥 **Contexte : Infrastructure réseau d’un hôpital**

Un hôpital moderne intègre de nombreux systèmes connectés :

- 📞 Téléphones IP pour les médecins et services internes
- 🎥 Caméras de vidéosurveillance
- 💻 Postes informatiques pour les dossiers patients
- 📶 Bornes Wi-Fi pour visiteurs et personnel
- 🖥 Serveurs d’imagerie médicale (IRM, scanner)

> 📌 *Ces flux doivent cohabiter sur une même infrastructure tout en étant isolés, sécurisés et parfois prioritaires.*

---

### 📋 **Consigne**

En vous appuyant sur les notions vues en cours, **proposez une architecture réseau convergente** adaptée à un hôpital, en répondant aux points suivants :

1. 🧩 **Quels types de VLANs prévoiriez-vous ?**
   - Pour quels usages ?
   - Pourquoi les séparer ?

2. 🔌 **Comment connecteriez-vous les équipements suivants ?**
   - Téléphone IP + PC sur un même port
   - Caméras IP
   - Postes utilisateurs classiques

3. ⚙️ **Quels ports nécessitent un paramétrage particulier** *(PoE, portfast, sécurité)* ?

4. 🔧 **Quels protocoles ou configurations vus en cours pourraient s’appliquer ici ?**
   - Exemple : `STP`, `Portfast`, `BPDU Guard`, `ARP`, `VLAN voix`

5. 🖊 **Quel schéma logique pourriez-vous dessiner pour illustrer cette convergence ?**
   *(à main levée ou avec un outil libre)*

---

### 📝 **Travail attendu**

Un court document *(1 page max)* ou une **diapositive** contenant :

- 🗺 Un **schéma réseau simple**
- 🛠 Des **annotations techniques** montrant comment la convergence est assurée *(ex : nom des VLANs, types d’équipements)*
- 🧠 Des **mots-clés issus du cours** soulignés dans les réponses *(ex : `portfast`, `VLAN 20 Voix`)*

---

### 🧠 **Objectif final**
> 🔍 *Ce travail vous permettra de faire le lien entre les **configurations techniques** et les **besoins concrets** d’un environnement sensible.*
> 
> Il prépare la réflexion pour la configuration **QoS** à venir.

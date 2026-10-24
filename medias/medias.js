// Catalogue des médias du cahier de révisions.
//
// Chaque média indique :
//   - fichier    : chemin depuis le dossier medias/ ;
//   - moments    : quand il peut apparaître (bonne, rate, serie, succes, bravo, courage) ;
//   - theme      : "chats", "blocs" (style Minecraft) ou "tous" ;
//   - age        : âge minimum, sur l'échelle PEGI (3, 7, 12, 16, 18) ;
//   - etiquettes : contenus sensibles (sexuel, nsfw, violence, grossier, peur).
// L'espace parent bloque les médias au-dessus de l'âge maximum choisi ou portant
// une étiquette interdite. Un média SANS âge est traité comme réservé aux 18 ans et plus.
//
// Pour ajouter un GIF ou un son : déposer le fichier dans medias/images ou
// medias/sons, puis ajouter une ligne ci-dessous.
window.MEDIAS = {
  images: [
    { fichier: "images/chat_danse.gif", moments: ["bonne", "serie"], theme: "chats", age: 3, etiquettes: [] },
    { fichier: "images/chat_lunettes.gif", moments: ["bonne", "serie", "bravo"], theme: "chats", age: 3, etiquettes: [] },
    { fichier: "images/chat_trophee.gif", moments: ["succes", "bravo"], theme: "chats", age: 3, etiquettes: [] },
    { fichier: "images/chat_triste.gif", moments: ["rate", "courage"], theme: "chats", age: 3, etiquettes: [] },
    { fichier: "images/bloc_diamant.gif", moments: ["bonne", "serie"], theme: "blocs", age: 3, etiquettes: [] },
    { fichier: "images/bloc_coffre.gif", moments: ["succes", "bravo"], theme: "blocs", age: 3, etiquettes: [] },
    { fichier: "images/bloc_coeurs.gif", moments: ["rate", "courage"], theme: "blocs", age: 3, etiquettes: [] },
  ],
  sons: [
    { fichier: "sons/ding.wav", moments: ["bonne"], theme: "tous", age: 3, etiquettes: [] },
    { fichier: "sons/pop.wav", moments: ["bonne"], theme: "tous", age: 3, etiquettes: [] },
    { fichier: "sons/xp.wav", moments: ["bonne"], theme: "blocs", age: 3, etiquettes: [] },
    { fichier: "sons/miaou.wav", moments: ["bonne", "bravo"], theme: "chats", age: 3, etiquettes: [] },
    { fichier: "sons/bonk.wav", moments: ["rate"], theme: "tous", age: 3, etiquettes: [] },
    { fichier: "sons/womp.wav", moments: ["rate", "courage"], theme: "tous", age: 3, etiquettes: [] },
    { fichier: "sons/niveau.wav", moments: ["serie"], theme: "tous", age: 3, etiquettes: [] },
    { fichier: "sons/fanfare.wav", moments: ["succes", "bravo"], theme: "tous", age: 3, etiquettes: [] },
  ],
  // Légendes façon mème ; {n} = nombre de bonnes réponses d'affilée.
  textes: {
    bonne: ["Miaou-gnifique !", "Calcul miné !", "+10 XP", "Le chat approuve", "Diamant trouvé !", "Trop fort !", "Exact !"],
    rate: ["Oups…", "Presque !", "Le chat a renversé le calcul", "Respawn…", "-1 cœur", "On réessaie ?"],
    serie: ["Série de {n} !", "Combo ×{n}", "{n} d'affilée !"],
    succes: ["Succès débloqué !"],
    bravo: ["GG !", "Champion !", "Niveau suivant !"],
    courage: ["La prochaine sera la bonne", "Même les chats ratent leur saut"],
  },
};

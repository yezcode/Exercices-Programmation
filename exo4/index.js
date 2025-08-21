// une variable pour récuperer depuis mon fichier html, le composant qui porte l'id 'nom'
const url = "http://graven.yt/citations.json";
let btn = document.getElementById("btn");
let avatar = document.getElementById("avatar");
let citation = document.getElementById("citation");
let text = document.getElementById("nom");
let citations = [];

// faire l'evenement lors d'un click bouton
btn.addEventListener("click", updatePage);

// recuperer toutes les citations depuis le lien graven.yt/citations.json
fetch(url).then((data) => {
  data.json().then((data) => {
    citations = data;

    // affichage de citations
    console.log(citations);
  });
});

function updatePage() {
  // choix au hasard d'une citation parmis la liste
  let random = Math.floor(Math.random() * (citations.length - 0));
  let randomCitation = citations[random];

  // modification
  text.innerText = randomCitation["nom"];
  citation.innerText = randomCitation["citation"];
  avatar.setAttribute("src", randomCitation["image"]);
}

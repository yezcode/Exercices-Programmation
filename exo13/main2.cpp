#include <iostream>
#include <random>

using namespace std;

// créer une classe qui va representer le concept d'arme
class Arme
{

public:
    // constructeur
    // Arme massue = Arme("Massue", 45, 3)
    Arme(string n, int a, int d)
    {
        nom = n;
        attaque = a;
        durabilite = d;
    }

    // creer une methode getNom()
    string getNom()
    {
        return nom;
    }

    int getAttaque()
    {
        return attaque;
    }

    void info()
    {
        // afficher le nom de l'arme
        cout << "Le nom de l'arme est : " << nom << " attaque :" << attaque << endl;
    }

private:
    // je definit les caracteristiques propre à chaque arme
    string nom;
    int attaque;
    int durabilite;
};

int main()
{

    cout << "Bienvenue à toi jeune combattant" << endl;
    cout << "Quel est ton pseudo ?" << endl;

    // je recolte le pseudo de la personne
    string pseudo;
    cin >> pseudo;

    cout << "Hey ! " << pseudo << !"Quelle arme souhaites tu pour combattre ?" << endl;
    cout << "Armes possible \n(1: Arc) \n(2:Lame) \n(3:Massue)" << endl;

    // une variable choix arme
    int choixArme;
    cin >> choixArme;

    // le tableau contenant les armes
    Arme armes[] = {
        Arme("Arc", 15, 10),            // premiere arme
        Arme("Lame tranchante", 30, 5), // deuxieme arme
        Arme("Massue", 23, 5)           // troisieme arme
    };

    // je veux recuperer l'arme que le combattant à choisi du numero
    Arme armeChoisi = armes[choixArme - 1];

    // variables
    int vieJoueur = 100;
    int attaqueJoueur = 10 + armeChoisi.getAttaque();
    int vieKraken = 400;
    int attaqueKraken = 1200;

    cout << "Très bien " << pseudo << " ! à l'attaque !" << endl;

    // simulons une attaque
    vieKraken -= attaqueJoueur * 5;

    cout << "Le kraken subit 5x attaques du joueur : " << vieKraken << " pv" << endl;

    // tant que la kraken est vivant
    while (vieKraken > 0 && vieJoueur > 0)
    {
        // lancé un premier dé
        random_device rd;
        // choisir un nombre au hasard entre 1 et 6
        uniform_int_distribution<int> dist(1, 6);

        int resultat_de = dist(rd);

        // verifier si le resultat du dé est impair ?
        if (resultat_de % 2 == 0)
        {
            // resultat est pair
            cout << "Attaque ratée !" << endl;

            // que le resultat vaut 6
            if (resultat_de == 6)
            {
                cout << "Attaque du kraken attention ! " << endl;
                vieJoueur -= attaqueKraken;
                cout << "Le combattant a désormais " << vieJoueur << " pv" << endl;
            }
        }
        else
        {
            // resultat impair
            // enlever les points de vie à mon kraken
            // simulons une attaque
            vieKraken -= attaqueJoueur;
            cout << "Attaque ok ! " << vieKraken << " pv" << endl;
        }
    }

    if (vieKraken <= 0)
    {
        // kraken est mort
        cout << "L’ennemi a été vaincu !! Bravo !" << endl;
    }
    else
    {
        // joueur qui est mort
        cout << "Les ténèbres l’emportent… Vous êtes mort ! " << endl;
    }
}
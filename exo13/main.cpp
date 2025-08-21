#include <iostream>
#include <random>

using namespace std;

int main()
{
    cout << "Bienvenue à toi jeune combattant" << endl;
    cout << "Quel est ton pseudo ?" << endl;

    // variables
    int vieJoueur = 100;
    int attaqueJoueur = 56;
    int vieKraken = 400;
    int attaqueKraken = 35;

    // je recolte le pseudo de la personne
    string pseudo;
    cin >> pseudo;

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

#Equipe :
#Cioiu Ioana Dumitrina
#Fainaru Ioana Gabriela
#Jugarean Carmen

#Theme : Simulateur traffique aeroportuaire

#Solution : 

Le programme est composee de 4 processeurs et 2 memoires , ca veut dire 4 piste et 2 tableaux affichant les departs et les arrives des avions. Pour que le programme fonctionne, les processus de depart et arrive doivent etre syncronisee . Dans une piste , l'avion qui veut atterir doit attendre que l'avion qui se trouve deja sur la piste decolle . 
Sur l'interface graphique, on voit le deroulement du processus donc on observe le pourcentage du depart / arrivee .Les tableaux sont compose de trois colonnes la premiere c'est avec le nom du compagnie aerienne et l'ID de chaque vol , la deuxieme concerne la priorite de chaque avion, et la derniere le temps estimee pour la duree du processus entier.Nous avons, aussi, un glisseur qui augment ou diminue la vitesse de simulation.

 Le button start permet de commencer la simulation, et pour l'arret on a le button stop. Pour voir l'interface graphique du programme,on ouvre le command prompt de windows (cmd), avec la commande "python tema1_main.py".
 
#Explication du code :
 La prioritee de l'aterissage est 0 et pour le depart est 1. Si 2 avions on la meme prioritee, l'avion qui va decoler le premier c'est l'avion avec la pile la plus grande. Quand la piste est libre, l'avion qui est entrain d'attendre a le droit d'atterir. Dans le fichier "Simulation2.py" on a la liste des companies aeriennes,on a definie le nombre de pistes , l'horologe.
 
 La fonction "getattr" prend l'attribut d'un objet en utilisant une chaine a la place d'un identificateur pour identifier l'atribut. On a creer ici le model graphique et encore le demarage de la simulation. Dans le fichier "Modellmpl.py", l'avion emmet un signal quand il atterit ou decole. Dans le ligne 43, on sorte la liste d'avions dans les tableaux et la fonction "Key = projection[Ncol]" sort les donnees qui se trouvent derriere l'action du click gauche du souris. Dans le fichier Plane.py le pourcentage du chaque piste est donnee par le raport entre maxLandingTime,self.LandingTime sur self._maxLandingTime. On genere l'ID du chaque avion avec des numeros aleatoires prises entre 0 et 2839(dans ce cas). Dans le ligne 38 , le programme une proprietee aleatoire,un nombre entier entre 0 et 3. En conclusion, en main , dans la ligne 12 les coordonnees 10,1000,4 represent le maxNumber d'avions , le TimerTick qui represent la duree de chaque action, et le nombre de pistes.

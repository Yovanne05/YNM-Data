export type Utilisateur = {
  idUtilisateur: number;
  nom: string;
  prenom: string;
  age: number;
  paysResidance: string;
  email: string;
  numero: number;
  statutAbonnement: 'Actif' | 'Résilié';
}

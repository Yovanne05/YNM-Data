export type Utilisateur = {
  idUtilisateur: number;
  age: number;
  nom: string;
  prenom: string;
  email: string;
  numero: number;
  paysResidance: string;
  statutAbonnement: 'Actif' | 'Resilié';
}

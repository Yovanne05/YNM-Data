import { Component, Input } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss'
})
export class HeaderComponent {
@Input() title: string = "Neftlix";

@Input() links: { label: string, path: string }[] = [
  { label: 'Tableau de Bord', path: 'dashboard' },
  { label: 'Tables', path: 'tables' },
  { label: 'Utilisateurs', path: 'users' },
  { label: 'Abonnements', path: 'subscriptions' },
  { label: 'Évaluations', path: 'evaluations' },
]
}

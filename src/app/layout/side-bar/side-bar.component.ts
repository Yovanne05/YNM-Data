import { Component, Input } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-side-bar',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './side-bar.component.html',
  styleUrl: './side-bar.component.scss'
})
export class SideBarComponent {
@Input() title: string = "Netflix";

@Input() links: { label: string, path: string}[] = [
  { label: 'Dashboard', path: 'dashboard' },
  { label: 'Tables', path: 'tables' },
  { label: 'Gestion des Utilisateurs', path: 'users' },
  { label: 'Gestion des Données', path: 'data-management' },
  { label: 'Paramètres API', path: 'api-settings' },
  { label: 'Logs', path: 'logs' },
  { label: 'Documentation', path: 'documentation' }
]
}

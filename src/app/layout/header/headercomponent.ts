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
@Input() title: string = "Netflix";

@Input() links: { label: string, path: string}[] = [
  { label: 'Tables', path: 'tables' },
  { label: 'Analyses', path: 'analysis' },
  { label: 'Logs', path: 'logs' },
]
}

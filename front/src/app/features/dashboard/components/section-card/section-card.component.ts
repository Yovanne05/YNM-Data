import {Component, Input} from '@angular/core';
import {RouterLink} from "@angular/router";
import {MatIcon} from "@angular/material/icon";

@Component({
  selector: 'app-section-card',
  standalone: true,
  imports: [
    RouterLink,
    MatIcon
  ],
  templateUrl: './section-card.component.html',
  styleUrl: './section-card.component.scss'
})
export class SectionCardComponent {
  @Input() icon!: string;
  @Input() title!: string;
  @Input() description!: string;
  @Input() route!: string;
}

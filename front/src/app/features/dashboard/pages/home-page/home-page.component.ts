import { Component } from '@angular/core';
import {SectionCardComponent} from "../../components/section-card/section-card.component";

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [
    SectionCardComponent
  ],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.scss'
})
export class HomePageComponent {

}

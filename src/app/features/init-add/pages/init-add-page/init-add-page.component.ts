import { Component } from '@angular/core';
import { InitDbComponent } from '../../components/init-db/init-db.component';

@Component({
  selector: 'app-init-add-page',
  standalone: true,
  imports: [InitDbComponent],
  templateUrl: './init-add-page.component.html',
  styleUrl: './init-add-page.component.scss'
})
export class InitAddPageComponent {

}

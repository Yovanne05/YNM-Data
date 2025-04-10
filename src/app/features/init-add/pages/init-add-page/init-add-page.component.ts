import { Component } from '@angular/core';
import { InitDbComponent } from '../../components/init-db/init-db.component';
import { AddSampleComponent } from "../../components/add-sample/add-sample.component";

@Component({
  selector: 'app-init-add-page',
  standalone: true,
  imports: [InitDbComponent, AddSampleComponent],
  templateUrl: './init-add-page.component.html',
  styleUrl: './init-add-page.component.scss'
})
export class InitAddPageComponent {

}

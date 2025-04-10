import { Component, inject } from '@angular/core';
import { InitDbService } from '../../../../services/transactional/init-db.service';
import {MatIcon} from "@angular/material/icon";

@Component({
  selector: 'app-add-sample',
  standalone: true,
  imports: [
    MatIcon
  ],
  templateUrl: './add-sample.component.html',
  styleUrl: './add-sample.component.scss'
})
export class AddSampleComponent {
  private readonly initDbService = inject(InitDbService);

  add_sample_data(): void {
    this.initDbService.add_sample_data().subscribe();
  }
}

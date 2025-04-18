import { Component, inject } from '@angular/core';
import { InitDbService } from '../../../../services/transactional/init-db.service';
import {MatIcon} from "@angular/material/icon";

@Component({
  selector: 'app-init-db',
  standalone: true,
  imports: [
    MatIcon
  ],
  templateUrl: './init-db.component.html',
  styleUrl: './init-db.component.scss'
})
export class InitDbComponent {
  private readonly initDbService = inject(InitDbService);

  reset_db(): void {
    this.initDbService.reset_db().subscribe();
  }
}

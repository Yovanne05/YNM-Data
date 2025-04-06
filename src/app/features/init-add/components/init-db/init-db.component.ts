import { Component, inject } from '@angular/core';
import { InitDbService } from '../../../../services/init-db.service';

@Component({
  selector: 'app-init-db',
  standalone: true,
  imports: [],
  templateUrl: './init-db.component.html',
  styleUrl: './init-db.component.scss'
})
export class InitDbComponent {
  private readonly initDbService = inject(InitDbService);

  reset_db(): void {
    this.initDbService.reset_db().subscribe();
  }
}

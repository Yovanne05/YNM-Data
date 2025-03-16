import { Component } from '@angular/core';
import { TableNavBarComponent } from "../../components/table-nav-bar/table-nav-bar.component";

@Component({
  selector: 'app-table-list-page',
  standalone: true,
  imports: [TableNavBarComponent],
  templateUrl: './table-list-page.component.html',
  styleUrl: './table-list-page.component.scss',
})
export class TableListPageComponent{

}

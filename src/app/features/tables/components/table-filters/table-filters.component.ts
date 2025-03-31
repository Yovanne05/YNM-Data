import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormGroup, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-table-filters',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './table-filters.component.html',
  styleUrls: ['./table-filters.component.scss']
})
export class TableFiltersComponent {
  @Input() filters: any[] = [];
  @Input() filterForm!: FormGroup;
  @Output() filterSubmit = new EventEmitter<void>();
  @Output() filterReset = new EventEmitter<void>();

  onSubmit() {
    this.filterSubmit.emit();
  }

  onReset() {
    this.filterForm.reset();
    this.filterReset.emit();
  }
}

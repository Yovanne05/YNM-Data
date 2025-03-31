import { Component, EventEmitter, Input, Output } from '@angular/core';
import { FormGroup, FormControl, ReactiveFormsModule } from '@angular/forms';
import { ActionMenuComponent } from "../action-menu/action-menu.component";
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-table-row',
  standalone: true,
  templateUrl: './table-row.component.html',
  styleUrls: ['./table-row.component.scss'],
  imports: [ActionMenuComponent, CommonModule, ReactiveFormsModule]
})
export class TableRowComponent {
  @Input() item: any;
  @Input() columns: string[] = [];
  @Input() isEditing = false;
  @Input() editForm?: FormGroup;
  @Output() edit = new EventEmitter<void>();
  @Output() delete = new EventEmitter<void>();
  @Output() save = new EventEmitter<void>();
  @Output() cancel = new EventEmitter<void>();

  getValue(key: string): any {
    return this.item[key];
  }

  getFormControl(column: string): FormControl {
    if (!this.editForm?.contains(column)) {
      console.warn(`FormControl for column '${column}' not found`);
      return new FormControl('');
    }
    return this.editForm.get(column) as FormControl;
  }
}

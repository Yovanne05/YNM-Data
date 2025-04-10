import { Component, EventEmitter, inject, Input, Output } from '@angular/core';
import { FormControl, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CsvImportService } from '../../../../services/transactional/csv-import.service';
import {MatIcon} from "@angular/material/icon";

@Component({
  selector: 'app-import-data',
  standalone: true,
  imports: [ReactiveFormsModule, MatIcon],
  templateUrl: './import-data.component.html',
  styleUrl: './import-data.component.scss'
})
export class ImportDataComponent {
  fichierCSV!: File;
  private readonly csvImportService = inject(CsvImportService);
  showImport: boolean = false;
  @Input() tableName!: string;
  showErrorMessage: boolean = false;

  dataForm = new FormGroup({
    fichierImport: new FormControl('', [Validators.required]),
  })

  ngOnChanges(): void {
    if (this.showImport == false) {
      this.showErrorMessage = false;
    }
  }

  onSubmit(): void {
    this.showErrorMessage = false;
    if (this.dataForm.valid) {
      this.csvImportService.sendCSVData(this.fichierCSV, this.tableName).subscribe({
        next: () => {
          this.showImport = false;
        },
        error: (err) => {
          this.showErrorMessage = true;
        }
      });
    }
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.fichierCSV = input.files[0];
    }
  }
}

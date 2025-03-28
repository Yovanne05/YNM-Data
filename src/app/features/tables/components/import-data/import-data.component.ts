import { Component, inject } from '@angular/core';
import { FormControl, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CsvImportService } from '../../../../services/csv-import.service';

@Component({
  selector: 'app-import-data',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './import-data.component.html',
  styleUrl: './import-data.component.scss'
})
export class ImportDataComponent {
  fichierCSV!: File;
  private readonly csvImportService = inject(CsvImportService);
  
  dataForm = new FormGroup({
    fichierImport: new FormControl('', [Validators.required]),
  })

  onSubmit(): void {
    if (this.dataForm.valid) {
      this.csvImportService.sendCSVData(this.fichierCSV).subscribe();
    }
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.fichierCSV = input.files[0];
    }
  }
}

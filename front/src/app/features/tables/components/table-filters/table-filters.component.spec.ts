import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TableFiltersComponent } from './table-filters.component';

describe('TableFiltersComponent', () => {
  let component: TableFiltersComponent;
  let fixture: ComponentFixture<TableFiltersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TableFiltersComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TableFiltersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

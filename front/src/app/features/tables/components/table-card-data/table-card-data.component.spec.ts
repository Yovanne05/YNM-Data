import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TableCardDataComponent } from './table-card-data.component';

describe('TableCardDataComponent', () => {
  let component: TableCardDataComponent;
  let fixture: ComponentFixture<TableCardDataComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TableCardDataComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TableCardDataComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

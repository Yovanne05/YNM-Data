import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TableCardInfoComponent } from './table-card-info.component';

describe('TableCardInfoComponent', () => {
  let component: TableCardInfoComponent;
  let fixture: ComponentFixture<TableCardInfoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TableCardInfoComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TableCardInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

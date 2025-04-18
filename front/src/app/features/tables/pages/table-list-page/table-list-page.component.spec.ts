import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TableListPageComponent } from './table-list-page.component';

describe('TableListPageComponent', () => {
  let component: TableListPageComponent;
  let fixture: ComponentFixture<TableListPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TableListPageComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TableListPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

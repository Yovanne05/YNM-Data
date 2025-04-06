import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InitDbComponent } from './init-db.component';

describe('InitDbComponent', () => {
  let component: InitDbComponent;
  let fixture: ComponentFixture<InitDbComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InitDbComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(InitDbComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

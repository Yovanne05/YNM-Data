import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InitAddPageComponent } from './init-add-page.component';

describe('InitAddPageComponent', () => {
  let component: InitAddPageComponent;
  let fixture: ComponentFixture<InitAddPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InitAddPageComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(InitAddPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

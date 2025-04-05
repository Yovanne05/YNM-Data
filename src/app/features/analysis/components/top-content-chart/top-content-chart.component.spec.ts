import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TopContentChartComponent } from './top-content-chart.component';

describe('TopContentChartComponent', () => {
  let component: TopContentChartComponent;
  let fixture: ComponentFixture<TopContentChartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TopContentChartComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(TopContentChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewingTrendsChartComponent } from './viewing-trends-chart.component';

describe('ViewingTrendsChartComponent', () => {
  let component: ViewingTrendsChartComponent;
  let fixture: ComponentFixture<ViewingTrendsChartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewingTrendsChartComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ViewingTrendsChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

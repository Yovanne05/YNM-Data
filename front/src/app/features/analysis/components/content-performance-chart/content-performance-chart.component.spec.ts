import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ContentPerformanceChartComponent } from './content-performance-chart.component';

describe('ContentPerformanceChartComponent', () => {
  let component: ContentPerformanceChartComponent;
  let fixture: ComponentFixture<ContentPerformanceChartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ContentPerformanceChartComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ContentPerformanceChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

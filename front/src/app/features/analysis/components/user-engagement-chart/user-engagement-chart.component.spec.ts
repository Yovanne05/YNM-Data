import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UserEngagementChartComponent } from './user-engagement-chart.component';

describe('UserEngagementChartComponent', () => {
  let component: UserEngagementChartComponent;
  let fixture: ComponentFixture<UserEngagementChartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserEngagementChartComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(UserEngagementChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

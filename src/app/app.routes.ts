import { AnalysisCardComponent } from './features/analysis/pages/analysis-card/analysis-card.component';
import { Routes } from '@angular/router';
import { NotFoundComponent } from './shared/pages/not-found/not-found.component';
import { TableListPageComponent } from './features/tables/pages/table-list-page/table-list-page.component';
import { DashboardPageComponent } from './features/dashboard/pages/dashboard-page/dashboard-page.component';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full',
  },
  {
    path: 'home',
    component: DashboardPageComponent
  },
  {
    path: 'tables',
    component: TableListPageComponent
  },
  {
    path: 'analysis',
    component: AnalysisCardComponent
  },
  {
    path: '**',
    redirectTo: '404'
  },
  {
    path: '404',
    component: NotFoundComponent
  }
];

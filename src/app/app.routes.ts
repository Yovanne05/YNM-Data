import { AnalysisPageComponent } from './features/analysis/pages/analysis-page/analysis-page.component';
import { Routes } from '@angular/router';
import { NotFoundComponent } from './shared/pages/not-found/not-found.component';
import { TableListPageComponent } from './features/tables/pages/table-list-page/table-list-page.component';
import { HomePageComponent } from './features/dashboard/pages/home-page/home-page.component';
import { InitAddPageComponent } from './features/init-add/pages/init-add-page/init-add-page.component';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full',
  },
  {
    path: 'home',
    component: HomePageComponent
  },
  {
    path: 'tables',
    component: TableListPageComponent
  },
  {
    path: 'init-add',
    component: InitAddPageComponent
  },
  {
    path: 'analysis',
    component: AnalysisPageComponent
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

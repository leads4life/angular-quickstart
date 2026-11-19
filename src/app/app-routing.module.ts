import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AboutComponent } from './pages/about.component';
import { CateringComponent } from './pages/catering.component';
import { ContactComponent } from './pages/contact.component';
import { GalleryComponent } from './pages/gallery.component';
import { HomeComponent } from './pages/home.component';
import { MenuComponent } from './pages/menu.component';
import { OrderOnlineComponent } from './pages/order-online.component';
import { PrivateEventsComponent } from './pages/private-events.component';

const routes: Routes = [
  { path: '', component: HomeComponent, data: { title: 'Authentic Chinese Cuisine in Wellington, FL' } },
  { path: 'menu', component: MenuComponent, data: { title: 'Menu' } },
  { path: 'about', component: AboutComponent, data: { title: 'About Us' } },
  { path: 'private-events', component: PrivateEventsComponent, data: { title: 'Private Events' } },
  { path: 'order-online', component: OrderOnlineComponent, data: { title: 'Order Online' } },
  { path: 'catering', component: CateringComponent, data: { title: 'Catering' } },
  { path: 'gallery', component: GalleryComponent, data: { title: 'Gallery' } },
  { path: 'contact', component: ContactComponent, data: { title: 'Contact Us' } },
  { path: '**', redirectTo: '' },
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, {
      scrollPositionRestoration: 'enabled',
      anchorScrolling: 'enabled',
    }),
  ],
  exports: [RouterModule],
})
export class AppRoutingModule {}

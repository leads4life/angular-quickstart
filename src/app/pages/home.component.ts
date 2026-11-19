import { Component } from '@angular/core';
import { POPULAR } from '../site.data';

@Component({ selector: 'app-home', templateUrl: './home.component.html' })
export class HomeComponent {
  readonly popular = POPULAR;
  readonly features = [
    { icon: 'bowl', title: 'Dine In', text: 'Relax and enjoy full service dining', link: '/contact' },
    { icon: 'bag', title: 'Takeout', text: 'Your favorites, ready to go', link: '/order-online' },
    { icon: 'people', title: 'Private Events', text: 'A great setting for family and special occasions', link: '/private-events' },
  ];
}

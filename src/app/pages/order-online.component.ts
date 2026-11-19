import { Component } from '@angular/core';
import { SITE } from '../site.data';

@Component({ selector: 'app-order-online', templateUrl: './order-online.component.html' })
export class OrderOnlineComponent {
  readonly site = SITE;
  readonly steps = [
    { icon: 'monitor', title: 'Order Online', text: 'Quick and easy.' },
    { icon: 'bag', title: 'Takeout', text: 'Fresh and ready.' },
    { icon: 'car', title: 'Convenient', text: 'Pick up at your time.' },
  ];
}

import { Component } from '@angular/core';

@Component({ selector: 'app-about', templateUrl: './about.component.html' })
export class AboutComponent {
  readonly values = [
    { icon: 'leaf', title: 'Fresh Ingredients', text: 'Quality you can taste.' },
    { icon: 'pot', title: 'Authentic Recipes', text: 'Classic dishes, done right.' },
    { icon: 'heart', title: 'Warm Hospitality', text: 'Our guests are always welcome.' },
  ];
}

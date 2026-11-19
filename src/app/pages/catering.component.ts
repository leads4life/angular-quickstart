import { Component } from '@angular/core';

@Component({ selector: 'app-catering', templateUrl: './catering.component.html' })
export class CateringComponent {
  readonly events = ['Corporate Events', 'Family Celebrations', 'Holiday Parties', 'Special Occasions', 'Custom Menu Options'];
}

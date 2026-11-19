import { Component } from '@angular/core';

@Component({ selector: 'app-private-events', templateUrl: './private-events.component.html' })
export class PrivateEventsComponent {
  readonly occasions = ['Birthday & Anniversary Dinners', 'Business & Team Meals', 'Family Gatherings', 'Catering Options Available'];
}

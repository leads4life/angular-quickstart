import { Component } from '@angular/core';
import { MENU, SITE } from '../site.data';

@Component({ selector: 'app-menu', templateUrl: './menu.component.html' })
export class MenuComponent {
  readonly menu = MENU;
  readonly site = SITE;
  /** Organic photo shapes, cycled down the page (offset so pages open on different shapes). */
  readonly shapes = ['a', 'b', 'c'];
}

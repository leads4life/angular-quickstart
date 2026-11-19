import { Component } from '@angular/core';
import { MENU, SITE } from '../site.data';

@Component({ selector: 'app-menu', templateUrl: './menu.component.html' })
export class MenuComponent {
  readonly menu = MENU;
  readonly site = SITE;
}

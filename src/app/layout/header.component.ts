import { Component, HostListener } from '@angular/core';
import { NavigationEnd, Router } from '@angular/router';
import { filter } from 'rxjs/operators';
import { NAV, SITE } from '../site.data';

@Component({
  selector: 'app-header',
  template: `
    <header class="site-header" [class.is-solid]="solid || open">
      <div class="container header-inner">
        <a routerLink="/" class="header-logo" aria-label="Golden Wok home"><app-logo></app-logo></a>

        <button class="nav-toggle" type="button" (click)="open = !open"
          [attr.aria-expanded]="open" aria-controls="site-nav"
          [attr.aria-label]="open ? 'Close menu' : 'Open menu'">
          <app-icon [name]="open ? 'close' : 'menu'" size="28"></app-icon>
        </button>

        <nav id="site-nav" class="site-nav" [class.is-open]="open" aria-label="Main">
          <a *ngFor="let link of nav" [routerLink]="link.path" routerLinkActive="is-active"
             [routerLinkActiveOptions]="{ exact: link.path === '/' }">{{ link.label }}</a>
          <a class="btn btn--red btn--sm" routerLink="/order-online" routerLinkActive="is-current">
            <app-icon name="bag" size="18"></app-icon> Order Online
          </a>
        </nav>
      </div>
    </header>`,
})
export class HeaderComponent {
  readonly nav = NAV;
  readonly site = SITE;
  open = false;
  solid = false;

  constructor(router: Router) {
    router.events.pipe(filter((e) => e instanceof NavigationEnd)).subscribe(() => (this.open = false));
  }

  @HostListener('window:scroll')
  onScroll(): void {
    this.solid = window.scrollY > 40;
  }

  @HostListener('document:keydown.escape')
  onEscape(): void {
    this.open = false;
  }
}

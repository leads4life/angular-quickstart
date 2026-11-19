import { Component } from '@angular/core';
import { NAV, SITE } from '../site.data';

@Component({
  selector: 'app-footer',
  template: `
    <footer class="site-footer">
      <app-wave fill="var(--burgundy)" variant="b"></app-wave>
      <div class="container footer-grid">
        <a routerLink="/" class="footer-logo" aria-label="Golden Wok home"><app-logo [stacked]="true"></app-logo></a>

        <div class="footer-col">
          <a class="footer-line" [href]="site.mapsUrl" target="_blank" rel="noopener">
            <app-icon name="pin" size="22"></app-icon>
            <span>{{ site.street }}<br>{{ site.cityLine }}</span>
          </a>
          <a class="footer-line footer-phone" [href]="site.phoneHref">
            <app-icon name="phone" size="22"></app-icon><span>{{ site.phone }}</span>
          </a>
        </div>

        <div class="footer-col">
          <h2 class="footer-title"><app-icon name="clock" size="22"></app-icon> Hours</h2>
          <dl class="hours">
            <ng-container *ngFor="let h of site.hours"><dt>{{ h.days }}</dt><dd>{{ h.time }}</dd></ng-container>
          </dl>
        </div>

        <nav class="footer-col footer-nav" aria-label="Footer">
          <a *ngFor="let link of nav.slice(1)" [routerLink]="link.path">{{ link.label }}</a>
          <a routerLink="/order-online">Order Online</a>
        </nav>

        <div class="footer-col footer-social">
          <h2 class="footer-title">Follow Us</h2>
          <div class="social">
            <a [href]="site.facebookUrl" target="_blank" rel="noopener" aria-label="Facebook"><app-icon name="facebook" size="22"></app-icon></a>
            <a [href]="site.instagramUrl" target="_blank" rel="noopener" aria-label="Instagram"><app-icon name="instagram" size="22"></app-icon></a>
          </div>
        </div>
      </div>
      <p class="container footer-legal">© {{ year }} {{ site.name }} {{ site.tagline }}. All rights reserved.</p>
    </footer>`,
})
export class FooterComponent {
  readonly nav = NAV;
  readonly site = SITE;
  readonly year = new Date().getFullYear();
}

import { Component } from '@angular/core';
import { ViewportScroller } from '@angular/common';
import { Title } from '@angular/platform-browser';
import { ActivatedRoute, NavigationEnd, Router } from '@angular/router';
import { filter } from 'rxjs/operators';
import { SITE } from './site.data';

@Component({
  selector: 'app-root',
  template: `
    <a class="skip-link" href="#main" (click)="skipToMain($event)">Skip to content</a>
    <app-header></app-header>
    <main id="main" tabindex="-1"><router-outlet></router-outlet></main>
    <app-footer></app-footer>`,
})
export class AppComponent {
  title = 'golden-wok';

  constructor(router: Router, route: ActivatedRoute, titles: Title, scroller: ViewportScroller) {
    // Keep anchored sections clear of the fixed header.
    scroller.setOffset([0, 96]);

    router.events.pipe(filter((e) => e instanceof NavigationEnd)).subscribe(() => {
      let r = route;
      while (r.firstChild) {
        r = r.firstChild;
      }
      const page = r.snapshot.data['title'] as string | undefined;
      titles.setTitle(page ? `${page} | ${SITE.name} ${SITE.tagline}` : `${SITE.name} ${SITE.tagline}`);
    });
  }

  /** A plain "#main" href would resolve against <base href="/"> and leave the page. */
  skipToMain(e: Event): void {
    e.preventDefault();
    document.getElementById('main')?.focus();
  }
}

import { Component } from '@angular/core';

@Component({
  selector: 'app-not-found',
  template: `
    <app-page-hero eyebrow="Page Not Found" title="This Table Is" accent="Empty"
      lead="The page you were looking for isn’t on our menu. Let us seat you somewhere better."
      image="assets/img/dining-room.jpg" [blossom]="true" [wave]="false">
      <a class="btn btn--red" routerLink="/">Back to Home <app-icon name="arrow" size="18"></app-icon></a>
      <a class="btn btn--outline" routerLink="/menu">View Menu</a>
    </app-page-hero>`,
})
export class NotFoundComponent {}

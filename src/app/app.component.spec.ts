import { TestBed } from '@angular/core/testing';
import { FormsModule } from '@angular/forms';
import { RouterTestingModule } from '@angular/router/testing';
import { AppComponent } from './app.component';
import { FooterComponent } from './layout/footer.component';
import { HeaderComponent } from './layout/header.component';
import { IconComponent } from './shared/icon.component';
import { LogoComponent } from './shared/logo.component';
import { WaveComponent } from './shared/wave.component';
import { NAV } from './site.data';

describe('AppComponent', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RouterTestingModule, FormsModule],
      declarations: [AppComponent, HeaderComponent, FooterComponent, IconComponent, LogoComponent, WaveComponent],
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(AppComponent);
    expect(fixture.componentInstance).toBeTruthy();
  });

  it('renders every main nav link plus the Order Online button', () => {
    const fixture = TestBed.createComponent(AppComponent);
    fixture.detectChanges();
    const el = fixture.nativeElement as HTMLElement;
    const labels = Array.from(el.querySelectorAll('#site-nav a')).map((a) => a.textContent?.trim());
    for (const link of NAV) {
      expect(labels).toContain(link.label);
    }
    expect(labels).toContain('Order Online');
  });

  it('renders the footer with the phone number', () => {
    const fixture = TestBed.createComponent(AppComponent);
    fixture.detectChanges();
    const el = fixture.nativeElement as HTMLElement;
    expect(el.querySelector('.site-footer')?.textContent).toContain('(561) 555-6888');
  });
});
